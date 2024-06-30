import json
import connect
from mongoengine.errors import NotUniqueError
from models import Author, Quote

def seed_authors_from_json(filename):
    with open(filename, encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'),
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'),
                                description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує: {el.get('fullname')}")

def seed_quotes_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for el in data:
        author_name = el.get('author')
        authors = Author.objects(fullname=author_name)
        
        if authors:
            author = authors[0]  # Припускаємо, що існує лише один автор із таким повним ім'ям
        else:
            print(f"Автор '{author_name}' не знайдено у базі даних. Пропускаємо.")
            continue

        quote = Quote(
            quote=el.get('quote'),
            author=author,
            tags=el.get('tags', [])
        )
        quote.save()

def seed_data():
    seed_authors_from_json('authors.json')
    seed_quotes_from_json('quotes.json')

if __name__ == '__main__':
    seed_data()
