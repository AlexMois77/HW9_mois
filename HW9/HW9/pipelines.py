import json
from itemadapter import ItemAdapter

class DataPipeline:
    def __init__(self):
        self.quotes = []
        self.authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'quote' in adapter and 'author' in adapter:
            self.quotes.append(dict(adapter))
        elif 'fullname' in adapter:
            self.authors.append(dict(adapter))
        return item

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)
