"""Check a daily-budget review packet before handing it to the editor.

Reads research.json and the evidence/existing-content.json snapshot written by
start_day.py. Errors are things that would break an import or a house rule;
warnings are things the editor should see. Exits 1 if there are any errors.

Usage: python check_packet.py [--repo PATH] [--library PATH] [--date YYYY-MM-DD]
       python check_packet.py --packet PATH
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

# Fallbacks if the repo's source files can't be read. The repo is the authority.
SECTIONS = {'local', 'government', 'business', 'schools', 'community', 'outdoors'}
CATEGORIES = {'community', 'arts', 'music', 'family', 'food', 'sports', 'outdoors', 'meetings', 'classes'}
IMAGE_STATUSES = {'cleared', 'library', 'permission-needed', 'shoot', 'none'}
ITEM_STATUSES = {'ready', 'needs-check', 'hold'}
SOCIAL_IMAGE_HOSTS = ('facebook.com', 'fbcdn.net', 'fb.com', 'x.com', 'twitter.com', 'twimg.com', 'instagram.com', 'cdninstagram.com')
SLUG = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
TIME = re.compile(r'^([01]\d|2[0-3]):[0-5]\d$')
MOJIBAKE = re.compile('â€|Ã[\u0080-¿]|�')

errors, warnings = [], []


def error(where, message):
    errors.append(f'{where}: {message}')


def warn(where, message):
    warnings.append(f'{where}: {message}')


def keys_of(path, const):
    try:
        text = path.read_text(encoding='utf-8')
    except OSError:
        return None
    block = re.search(rf'export const {const} = \{{(.*?)\}}', text, re.S)
    return set(re.findall(r'^\s*(\w+):', block.group(1), re.M)) if block else None


def words(text):
    return {w for w in re.findall(r'[a-z0-9]+', (text or '').lower()) if len(w) > 2}


def similar(a, b):
    a, b = words(a), words(b)
    return len(a & b) / len(a | b) if a and b else 0


def is_url(value):
    return isinstance(value, str) and urlparse(value).scheme in ('http', 'https') and bool(urlparse(value).netloc)


def is_social(url):
    host = urlparse(url or '').netloc.lower()
    return any(host == h or host.endswith('.' + h) for h in SOCIAL_IMAGE_HOSTS)


def check_text(where, item, fields):
    for field in fields:
        if isinstance(item.get(field), str) and MOJIBAKE.search(item[field]):
            error(where, f'{field} has garbled characters (encoding damage); write files as UTF-8')


def check_image(where, image, media_ids, packet):
    if not isinstance(image, dict) or image.get('status') not in IMAGE_STATUSES:
        error(where, f'image.status must be one of {sorted(IMAGE_STATUSES)}')
        return
    status = image['status']
    if status == 'cleared':
        for field in ('source_url', 'license', 'credit', 'caption', 'alt'):
            if not image.get(field):
                error(where, f'cleared image needs {field}')
        if is_social(image.get('source_url')):
            error(where, 'cleared image comes from a social platform; those images need the owner\'s permission')
        if image.get('file') and not (packet / 'images' / image['file']).is_file():
            error(where, f"image file images/{image['file']} is missing")
    if status == 'library' and image.get('media_id') not in media_ids:
        error(where, 'library image needs a media_id that exists in the media library')
    if status == 'permission-needed' and not image.get('contact'):
        warn(where, 'permission-needed image has no contact to ask')
    alt = image.get('alt') or ''
    if len(alt) > 300:
        warn(where, 'alt text is over 300 characters')
    if re.match(r'(image|photo|picture) of', alt, re.I):
        warn(where, 'alt text starts with "image of"/"photo of"')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', default='.')
    parser.add_argument('--library')
    parser.add_argument('--date', default=date.today().isoformat())
    parser.add_argument('--packet')
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')

    repo = Path(args.repo).resolve()
    if args.packet:
        packet = Path(args.packet).resolve()
    else:
        library = Path(args.library or os.environ.get('FIRELANDS_PROJECT_DIR') or repo.parent.parent / 'Projects' / 'firelands-current')
        packet = (library / 'editorial' / args.date).resolve()
    sections = keys_of(repo / 'src' / 'lib' / 'news.ts', 'SECTIONS') or SECTIONS
    categories = keys_of(repo / 'src' / 'lib' / 'events.ts', 'CATEGORIES') or CATEGORIES

    try:
        research = json.loads((packet / 'research.json').read_text(encoding='utf-8'))
        existing = json.loads((packet / 'evidence' / 'existing-content.json').read_text(encoding='utf-8'))
    except FileNotFoundError as missing:
        sys.exit(f'Missing {missing.filename}. Run start_day.py, then write research.json.')
    except json.JSONDecodeError as bad:
        sys.exit(f'research.json is not valid JSON: {bad}')

    packet_date = research.get('date') or args.date
    article_slugs = {a['slug'] for a in existing['articles']}
    event_slugs = {e['slug'] for e in existing['events']}
    media_ids = {m['id'] for m in existing['media']}
    stories = research.get('stories') or []
    events = research.get('events') or []
    for key in ('date', 'stories', 'events', 'held_leads'):
        if key not in research:
            error('research.json', f'missing top-level "{key}"')
    if not (packet / 'review.md').is_file():
        error('review.md', 'missing; the editor reads this, not the JSON')

    seen = set()
    for i, story in enumerate(stories):
        where = f"story {story.get('key') or i}"
        for field in ('key', 'slug', 'status', 'section', 'community', 'headline', 'summary', 'body', 'source_urls', 'image'):
            if not story.get(field):
                error(where, f'missing {field}')
        check_text(where, story, ('headline', 'summary', 'body'))
        slug = story.get('slug') or ''
        if slug and (not SLUG.match(slug) or len(slug) > 120):
            error(where, f'slug "{slug}" must be lowercase words joined by hyphens, 120 characters or fewer')
        if slug in article_slugs:
            error(where, f'slug "{slug}" is already used by a published or draft story')
        if slug in seen:
            error(where, f'slug "{slug}" is used twice in this packet')
        seen.add(slug)
        if story.get('status') and story['status'] not in ITEM_STATUSES:
            error(where, f'status must be one of {sorted(ITEM_STATUSES)}')
        if story.get('section') and story['section'] not in sections:
            error(where, f"section must be one of {sorted(sections)}")
        if len(story.get('summary') or '') > 160:
            warn(where, 'summary is over 160 characters, so search results will cut it off')
        urls = story.get('source_urls') or []
        if not all(is_url(u) for u in urls):
            error(where, 'every source_urls entry must be an http(s) URL')
        body = story.get('body') or ''
        if urls and not any(u in body for u in urls):
            warn(where, 'the body links none of its source_urls; link the primary source in the story')
        if '[NEED:' in body and story.get('status') == 'ready':
            error(where, 'status is ready but the body still has [NEED: ...] gaps')
        if not (packet / 'drafts' / f"{story.get('key')}.md").is_file():
            warn(where, f"no drafts/{story.get('key')}.md with the newsroom output")
        for article in existing['articles']:
            if similar(story.get('headline'), article['headline']) >= 0.5:
                warn(where, f"headline looks close to existing story \"{article['headline']}\" ({article['slug']})")
        if story.get('image'):
            check_image(where, story['image'], media_ids, packet)

    seen = set()
    for i, event in enumerate(events):
        where = f"event {event.get('key') or i}"
        for field in ('key', 'slug', 'status', 'title', 'category', 'starts_on', 'venue', 'community', 'source_url', 'summary'):
            if not event.get(field):
                error(where, f'missing {field}')
        check_text(where, event, ('title', 'summary', 'description', 'venue', 'cost'))
        slug = event.get('slug') or ''
        if slug and (not SLUG.match(slug) or len(slug) > 120):
            error(where, f'slug "{slug}" must be lowercase words joined by hyphens, 120 characters or fewer')
        if slug in event_slugs or slug in seen:
            error(where, f'slug "{slug}" is already taken')
        seen.add(slug)
        if event.get('status') and event['status'] not in ITEM_STATUSES:
            error(where, f'status must be one of {sorted(ITEM_STATUSES)}')
        if event.get('category') and event['category'] not in categories:
            error(where, f'category must be one of {sorted(categories)}')
        for field in ('starts_on', 'ends_on'):
            value = event.get(field)
            if value:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    error(where, f'{field} must be YYYY-MM-DD')
        if (event.get('ends_on') or event.get('starts_on') or '9999') < packet_date:
            warn(where, 'event is already over')
        for field in ('start_time', 'end_time'):
            if event.get(field) and not TIME.match(event[field]):
                error(where, f'{field} must be 24-hour HH:MM or null')
        if event.get('source_url') and not is_url(event['source_url']):
            error(where, 'source_url must be an http(s) URL')
        for other in existing['events']:
            if other['starts_on'] == event.get('starts_on') and similar(event.get('title'), other['title']) >= 0.4:
                warn(where, f"may duplicate existing event \"{other['title']}\" on {other['starts_on']}")
        if event.get('image'):
            check_image(where, event['image'], media_ids, packet)

    story_images = {s.get('key'): (s.get('image') or {}).get('status') for s in stories}
    for key in research.get('featured') or []:
        if key not in story_images:
            error('featured', f'"{key}" is not a story key in this packet')
        elif story_images[key] not in ('cleared', 'library'):
            warn('featured', f'"{key}" has no usable lead photo')
    for update in research.get('updates') or []:
        if update.get('slug') not in article_slugs | event_slugs:
            error('updates', f"\"{update.get('slug')}\" is not an existing story or event")

    pictured = sum(1 for s in stories if (s.get('image') or {}).get('status') in ('cleared', 'library'))
    print(f'Packet: {packet}')
    print(f'{len(stories)} stories ({pictured} with a usable photo), {len(events)} events, '
          f"{len(research.get('updates') or [])} updates, {len(research.get('held_leads') or [])} held leads")
    for line in errors:
        print(f'ERROR   {line}')
    for line in warnings:
        print(f'WARNING {line}')
    if not errors and not warnings:
        print('No problems found.')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
