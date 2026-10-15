"""Open today's review packet and print what Firelands Current already has.

Read-only against the local D1 database. Creates the dated packet folders in the
project library, snapshots existing stories, events and media to
evidence/existing-content.json, and prints a briefing: section balance, recent
stories, upcoming events, reusable library photos, and recent stories in full as
style samples.

Usage: python start_day.py [--repo PATH] [--library PATH] [--date YYYY-MM-DD] [--style N]
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

D1_GLOB = '.wrangler/state/v3/d1/miniflare-D1DatabaseObject/*.sqlite'


def find_repo(path):
    repo = Path(path).resolve()
    if not (repo / 'docs' / 'news-sources.md').is_file():
        sys.exit(f'{repo} is not the firelands-current repository (no docs/news-sources.md). Pass --repo.')
    return repo


def find_library(repo, path):
    library = Path(path or os.environ.get('FIRELANDS_PROJECT_DIR') or repo.parent.parent / 'Projects' / 'firelands-current').resolve()
    if not (library / 'editorial').is_dir():
        sys.exit(f'Project library not found at {library}. Pass --library or set FIRELANDS_PROJECT_DIR.')
    return library


def open_database(repo):
    files = [p for p in repo.glob(D1_GLOB) if not p.name.endswith('metadata.sqlite')]
    if not files:
        sys.exit('No local D1 database under .wrangler/. Run `npm run db:migrate:local` in the repo first.')
    newest = max(files, key=lambda p: p.stat().st_mtime)
    db = sqlite3.connect(newest.resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    return db


def rows(db, sql):
    return [dict(r) for r in db.execute(sql)]


def day_of(ms):
    return datetime.fromtimestamp(ms / 1000).date() if ms else None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', default='.')
    parser.add_argument('--library')
    parser.add_argument('--date', default=date.today().isoformat())
    parser.add_argument('--style', type=int, default=3, help='recent stories to print in full')
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')

    today = date.fromisoformat(args.date)
    repo = find_repo(args.repo)
    library = find_library(repo, args.library)
    packet = library / 'editorial' / args.date
    for sub in ('evidence', 'drafts', 'images'):
        (packet / sub).mkdir(parents=True, exist_ok=True)

    db = open_database(repo)
    articles = rows(db, 'SELECT slug, headline, summary, body, section, community, status, featured, '
                        'published_at, lead_media_id FROM news_articles ORDER BY published_at DESC')
    events = rows(db, 'SELECT slug, title, category, starts_on, start_time, ends_on, end_time, venue, '
                      'community, status FROM events ORDER BY starts_on')
    media = rows(db, 'SELECT id, filename, alt, caption, credit, source, decorative, created_at '
                     'FROM media ORDER BY created_at DESC')
    db.close()

    snapshot = {'taken': datetime.now().isoformat(timespec='seconds'), 'date': args.date,
                'articles': articles, 'events': events, 'media': media}
    (packet / 'evidence' / 'existing-content.json').write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    published = [a for a in articles if a['status'] == 'published']
    print(f'Packet: {packet}')
    if (packet / 'research.json').exists():
        print('NOTE: research.json already exists here. Continue that packet instead of starting over.')
    print(f'Existing: {len(published)} published stories, {len(events)} events, {len(media)} library images\n')

    print('## Section balance (published stories, last 7 / 14 days)')
    sections = sorted({a['section'] for a in articles})
    for section in sections:
        recent = [day_of(a['published_at']) for a in published if a['section'] == section]
        week = sum(1 for d in recent if d and d > today - timedelta(days=7))
        fortnight = sum(1 for d in recent if d and d > today - timedelta(days=14))
        thin = '  <- thin' if week < 3 else ''
        print(f'- {section}: {week} / {fortnight}{thin}')

    print('\n## Stories from the last 21 days (date | section | photo | featured | headline | slug)')
    for a in published:
        d = day_of(a['published_at'])
        if not d or d <= today - timedelta(days=21):
            continue
        photo = 'photo' if a['lead_media_id'] else '-'
        featured = 'featured' if a['featured'] else '-'
        print(f"- {d} | {a['section']} | {photo} | {featured} | {a['headline']} | {a['slug']}")

    print('\n## Upcoming and current events (start | end | title | community | status)')
    for e in events:
        last = e['ends_on'] or e['starts_on']
        if last and last >= args.date:
            print(f"- {e['starts_on']} | {e['ends_on'] or '-'} | {e['title']} | {e['community'] or '-'} | {e['status']}")

    print('\n## Media library (id | credit | caption)')
    for m in media:
        caption = (m['caption'] or m['alt'] or m['filename'] or '').replace('\n', ' ')[:110]
        print(f"- {m['id']} | {(m['credit'] or '-')[:60]} | {caption}")

    print(f'\n## Style samples: the {args.style} newest published stories')
    for a in published[:args.style]:
        print(f"\n### {a['headline']}\nSection: {a['section']} | Community: {a['community']}\n"
              f"Summary: {a['summary']}\n\n{a['body']}")


if __name__ == '__main__':
    main()
