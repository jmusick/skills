"""Draft review.md from research.json, in the order references/packet.md gives.

Fills the mechanical parts (title, updates, best new stories, featured, calendar
additions, new sources, held leads) so they match research.json exactly. Text
only you can write is left as `_fill in_`; check_packet.py errors while any
remain. Refuses to overwrite an existing --out file unless --force.

Usage: python render_review.py [--repo PATH] [--library PATH] [--date YYYY-MM-DD] [--out FILE]
       python render_review.py --packet PATH [--out FILE]

Reads only. Prints the Markdown, or writes it as UTF-8 to --out (use --out on
Windows: redirecting stdout in PowerShell can change the encoding).
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

FILL = '_fill in_'
MONTHS = ['Jan.', 'Feb.', 'March', 'April', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']


def ap_date(iso, weekday=True):
    d = date.fromisoformat(iso)
    text = f'{MONTHS[d.month - 1]} {d.day}'
    return f'{d.strftime("%A")}, {text}' if weekday else text


def ap_clock(hhmm):
    try:
        h, m = (int(x) for x in hhmm.split(':'))
    except ValueError:
        return f'{hhmm} (not HH:MM; check_packet.py will flag it)', ''
    if (h, m) == (12, 0):
        return 'noon', ''
    if (h, m) == (0, 0):
        return 'midnight', ''
    mer = 'a.m.' if h < 12 else 'p.m.'
    h12 = h % 12 or 12
    return (f'{h12}:{m:02d}' if m else f'{h12}'), mer


def ap_time_range(start, end):
    if not start:
        return ''
    s, s_mer = ap_clock(start)
    if not end:
        return f'{s} {s_mer}'.strip()
    e, e_mer = ap_clock(end)
    if s_mer and s_mer == e_mer:
        return f'{s}-{e} {e_mer}'
    return f'{s} {s_mer} to {e} {e_mer}'.replace('  ', ' ').strip()


def ap_date_range(start, end):
    if not end or end == start:
        return ap_date(start)
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    if (a.year, a.month) == (b.year, b.month):
        return f'{ap_date(start)}-{b.day}'
    return f'{ap_date(start)} to {ap_date(end)}'


def cell(text):
    return (text or '').replace('|', '\\|').replace('\n', ' ').strip()


def link(text, url):
    if not url:
        return cell(text)
    return f"[{cell(text)}]({url.replace(' ', '%20').replace('(', '%28').replace(')', '%29')})"


def render(research):
    featured = research.get('featured') or []
    stories_by_key = {s.get('key'): s for s in research.get('stories', [])}
    try:
        d = date.fromisoformat(research.get('date', ''))
        title = f'{MONTHS[d.month - 1]} {d.day}, {d.year}'
    except ValueError:
        title = FILL
    out = [f'# {title} story and event leads', '',
           f'{FILL}: one paragraph on what you compared against (counts), how many stories, events and updates '
           'you are proposing, and that nothing has been imported or published.', '']

    updates = research.get('updates') or []
    if updates:
        out += ['## First action: updates to existing coverage', '']
        out += [f"- `{u.get('slug')}`: {cell(u.get('change'))} ({link('source', u.get('source_url'))})" for u in updates]
        out.append('')

    stories = [s for s in research.get('stories', []) if s.get('status') != 'hold']
    if stories:
        out += ['## Best new stories', '',
                '| Priority | Proposed story | Why use it today | Readiness and image |',
                '| --- | --- | --- | --- |']
        for i, s in enumerate(stories, 1):
            image = (s.get('image') or {}).get('status', 'none')
            ready = f"{s.get('status', '?')}; image: {image}"
            if s.get('key') in featured:
                ready += f'; featured #{featured.index(s["key"]) + 1}'
            draft = 'drafts/%s.md' % s.get('key')
            out.append(f"| {i} | {link(s.get('headline'), draft)} | {FILL} | {ready} |")
        out += ['', f'{FILL}: a short paragraph per story on what is verified, what is not, and the trap to avoid.', '']

    if featured:
        out += ['## Featured', '']
        out += [f"{i}. {cell((stories_by_key.get(k) or {}).get('headline') or k)}" for i, k in enumerate(featured, 1)]
        out += ['', f'{FILL}: which current featured stories these replace, and why.', '']

    events = research.get('events') or []
    if events:
        out += ['## Potential calendar additions', '',
                '| Event | Date and time | Place | Cost, registration and remaining checks |',
                '| --- | --- | --- | --- |']
        for e in sorted(events, key=lambda e: (e.get('starts_on') or '', e.get('start_time') or '')):
            when = ap_date_range(e['starts_on'], e.get('ends_on')) if e.get('starts_on') else FILL
            times = ap_time_range(e.get('start_time'), e.get('end_time'))
            if times:
                when += f', {times}'
            if e.get('hours_note'):
                when += f" ({cell(e['hours_note'])})"
            place = ', '.join(x for x in (cell(e.get('venue')), cell(e.get('community'))) if x)
            checks = '; '.join(x for x in (cell(e.get('cost')), cell(e.get('notes'))) if x)
            if e.get('status') != 'ready':
                checks = f"{e.get('status')}: {checks}" if checks else e.get('status')
            out.append(f"| {link(e.get('title'), e.get('source_url'))} | {when} | {place} | {checks} |")
        out.append('')

    out += ['## Image opportunities', '',
            f'{FILL}: cleared images with credit and license; permission requests drafted (not sent) with the '
            'contact; photos the editor could take. Delete this section if there are none.', '']

    sources = research.get('new_sources') or []
    if sources:
        out += ['## Useful new sources', '', '| Source | Leads supplied | How to use it |', '| --- | --- | --- |']
        for s in sources:
            logged = '' if s.get('logged_in_news_sources') else ' (not yet in news-sources.md)'
            out.append(f"| {link(s.get('name'), s.get('url'))}{logged} | {FILL} | {FILL} |")
        out.append('')

    held = research.get('held_leads') or []
    held_stories = [s for s in research.get('stories', []) if s.get('status') == 'hold']
    if held or held_stories:
        out += ['## Held leads and source checks', '']
        out += [f"- {link(s.get('headline'), (s.get('source_urls') or [None])[0])} (story on hold): {cell(s.get('notes'))}"
                for s in held_stories]
        out += [f"- {link(h.get('topic'), h.get('source_url'))}: missing {cell(h.get('missing'))}" for h in held]
        out.append('')

    out += ['## Sources swept', '', '| Source | Checked | Result |', '| --- | --- | --- |',
            f'| {FILL} | | |', '',
            'Every source you opened today, including the ones with nothing new.', '']

    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', default='.')
    parser.add_argument('--library')
    parser.add_argument('--date', default=date.today().isoformat())
    parser.add_argument('--packet')
    parser.add_argument('--out')
    parser.add_argument('--force', action='store_true', help='overwrite --out if it exists')
    args = parser.parse_args()

    if args.packet:
        packet = Path(args.packet).resolve()
    else:
        repo = Path(args.repo).resolve()
        library = Path(args.library or os.environ.get('FIRELANDS_PROJECT_DIR') or repo.parent.parent / 'Projects' / 'firelands-current')
        packet = (library / 'editorial' / args.date).resolve()
    try:
        research = json.loads((packet / 'research.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        sys.exit(f'Cannot read {packet / "research.json"}: {exc}')

    text = render(research)
    if args.out and Path(args.out).exists() and not args.force:
        sys.exit(f'{args.out} already exists; it may hold your edits. Pass --force to overwrite it.')
    if args.out:
        Path(args.out).write_text(text, encoding='utf-8')
        print(f'Wrote {args.out}')
    else:
        sys.stdout.reconfigure(encoding='utf-8')
        print(text)


if __name__ == '__main__':
    main()
