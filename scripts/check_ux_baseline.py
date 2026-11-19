#!/usr/bin/env python3
"""Check the local 5e.tools reader contract before and after UI changes."""
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    data = root / 'data'
    books = json.loads((data / 'books.json').read_text(encoding='utf-8'))['book']
    ids = [book['id'].lower() for book in books]
    errors = []
    if not ids or len(set(ids)) != len(ids):
        errors.append('Book index is empty or has duplicate IDs')
    for book_id in ('xphb', 'xdmg', 'xmm'):
        if book_id not in ids:
            errors.append(f'Missing core book: {book_id}')
    for book_id in sorted(set(ids)):
        path = data / 'book' / f'book-{book_id}.json'
        try:
            records = json.loads(path.read_text(encoding='utf-8'))['bookData']
            if not any(record['id'].lower() == book_id and record['data'] for record in records):
                errors.append(f'No non-empty payload for {book_id}: {path.name}')
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            errors.append(f'{path.name}: {exc}')
    for page in ('index.html', 'books.html', 'book.html', 'spells.html', 'classes.html', 'bestiary.html'):
        if not (root / page).is_file():
            errors.append(f'Missing native entry point: {page}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(ids)} indexed books with non-empty payloads; native entry points intact.')


if __name__ == '__main__':
    main()
