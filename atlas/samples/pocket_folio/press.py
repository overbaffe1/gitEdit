"""Publish a portfolio edition from one local issue file. No network or README rewriting."""

import argparse
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BLOCK = Path('templates/blocks/pocket-folio.md')
ART = Path('assets/pocket-folio')


def load_issue(path):
    issue = json.loads(path.read_text(encoding='utf-8'))
    works = issue['works']
    if len(works) != 3:
        raise ValueError('Для восьми страниц нужны ровно три работы.')
    urls = [issue['profile']]
    for w in works:
        rows = w['marks']
        if (not rows or not rows[0] or len({len(row) for row in rows}) != 1
                or set(''.join(rows)) - set('01|') or sum(map(len, rows)) != w['number']):
            raise ValueError(f"{w['project']}: marks — прямоугольник из 0, 1 и |; по одному знаку на единицу числа.")
        urls.extend(w[k]['url'] for k in ('proof', 'also'))
    if any(urlsplit(u).scheme != 'https' or not urlsplit(u).hostname for u in urls):
        raise ValueError('Для портфолио нужны полные HTTPS-ссылки.')
    return issue


def markdown(issue):
    e = escape
    lines = ['<table>', '<thead>',
             (f'<tr><th colspan="2" align="left"><sub>ЛИЧНЫЙ ТИРАЖ · № {e(issue["issue"])} · {e(issue["author"])}</sub>'
              f'<br>{e(issue["title"])}</th></tr>'), '</thead>', '<tbody>']
    for i, w in enumerate(issue['works'], 1):
        proof, also = w['proof'], w['also']
        lines += ['<tr>',
                  (f'<th scope="row" align="center">'
                   f'<a href="{e(proof["url"])}" title="{e(proof["label"])}"><strong>{w["number"]}</strong>'
                   f'<br><sub>{e(w["unit"])}</sub></a></th>'),
                  (f'<td><sub>{2 * i:02d}–{2 * i + 1:02d} · {e(w["project"])}</sub><br><strong>{e(w["title"])}</strong><br>{e(w["body"])}'
                   f'<br><a href="{e(also["url"])}">{e(also["label"])}</a></td>'), '</tr>']
    return '\n'.join([*lines, '</tbody>', '</table>']) + '\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--issue', type=Path, default=HERE / 'issue.json')
    p.add_argument('--markdown', action='store_true', help='print just the portable block to stdout (stdlib only)')
    p.add_argument('--out', type=Path, default=ROOT, help='output tree; never modifies the home README')
    p.add_argument('--fonts', type=Path, default=Path('/usr/share/fonts/truetype/dejavu'))
    args = p.parse_args()
    try:
        issue = load_issue(args.issue)
        block = markdown(issue)
        if args.markdown:
            print(block, end='')
            return
        from paper import print_edition

        (args.out / ART).mkdir(parents=True, exist_ok=True)
        print_edition(issue, args.out / ART, args.fonts)
        path = args.out / BLOCK
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(block, encoding='utf-8')
    except (ImportError, OSError, ValueError, KeyError) as exc:
        p.exit(1, f'{p.prog}: {exc}\n')


if __name__ == '__main__':
    main()
