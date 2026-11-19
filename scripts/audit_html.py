"""Read a local HTML snapshot and extract Google SEO inspection evidence."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titles, self.h1s, self.descriptions, self.canonicals = [], [], [], []
        self.robots, self.images, self.links, self.bases = [], [], [], []
        self.active = []
        self.ignore = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style', 'template'):
            self.ignore += 1
        if self.ignore:
            return
        if tag in ('title', 'h1'):
            self.active.append({'tag': tag, 'text': [], 'line': self.getpos()[0]})
        if tag == 'meta':
            name = (a.get('name') or '').lower()
            if name == 'description':
                self.descriptions.append(a.get('content') or '')
            if name in ('robots', 'googlebot', 'googlebot-news'):
                self.robots.append({'agent': name, 'content': a.get('content') or '', 'line': self.getpos()[0]})
        if tag == 'link' and 'canonical' in (a.get('rel') or '').lower().split():
            self.canonicals.append(a.get('href') or '')
        if tag == 'base' and a.get('href'):
            self.bases.append(a['href'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag == 'img':
            self.images.append({'src': a.get('src'), 'alt': a.get('alt'), 'line': self.getpos()[0]})

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template'):
            self.ignore = max(0, self.ignore - 1)
            return
        if self.ignore:
            return
        for i in range(len(self.active) - 1, -1, -1):
            if self.active[i]['tag'] == tag:
                item = self.active.pop(i)
                result = {'text': ' '.join(''.join(item['text']).split()), 'line': item['line']}
                (self.titles if tag == 'title' else self.h1s).append(result)
                break

    def handle_data(self, data):
        if not self.ignore:
            for item in self.active:
                item['text'].append(data)


def audit(html, url):
    page = Page()
    page.feed(html)
    page.close()
    issues = []
    for label, values in (('title', page.titles), ('h1', page.h1s), ('description', page.descriptions), ('canonical', page.canonicals)):
        if not values:
            issues.append({'type': 'missing_' + label})
        elif len(values) > 1:
            issues.append({'type': 'multiple_' + label, 'count': len(values), 'judgment': 'review'})
    if page.titles and not page.titles[0]['text']:
        issues.append({'type': 'empty_title'})
    for item in page.robots:
        tokens = {v.strip().lower() for v in item['content'].replace(',', ' ').split()}
        if tokens & {'noindex', 'none'}:
            issues.append({'type': 'noindex', **item})
        if {'index', 'noindex'}.issubset(tokens):
            issues.append({'type': 'conflicting_robots', **item})
    base = urljoin(url, page.bases[0]) if page.bases else url
    return {'url': url, 'titles': page.titles, 'h1s': page.h1s, 'descriptions': page.descriptions,
            'canonical_raw': page.canonicals, 'canonical_resolved': [urljoin(base, c) for c in page.canonicals],
            'robots_meta': page.robots, 'images': page.images, 'links': [urljoin(base, v) for v in page.links],
            'issues': issues, 'unverified': ['HTTP status and headers', 'robots.txt', 'JS rendered DOM', 'indexing', 'performance', 'link destinations'],
            'scope': 'provided HTML snapshot only'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--url', required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    try:
        url = urlsplit(a.url)
        if url.scheme not in ('http', 'https') or not url.hostname:
            raise ValueError('--url must be an absolute HTTP(S) URL')
        result = audit(a.input.read_text(encoding='utf-8-sig'), a.url)
        with a.output.open('x', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps({'issues': len(result['issues']), 'scope': result['scope']}))
    except (OSError, ValueError) as e:
        p.exit(2, str(e) + '\n')


if __name__ == '__main__':
    main()
