from typing import List, Any
import connect
import redis
import sys
import codecs
from redis_lru import RedisLRU

from seeds import seed_data
from models import Author, Quote


# Налаштування підключення до Redis
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

# Лічильники викликів для перевірки кешування
find_by_tag_calls = 0
find_by_author_calls = 0
find_by_tags_calls = 0

@cache
def find_by_tag(tag: str) -> List[str]:
    global find_by_tag_calls
    find_by_tag_calls += 1
    print(f"Calling find_by_tag, call number: {find_by_tag_calls}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> List[str]:
    global find_by_author_calls
    find_by_author_calls += 1
    print(f"Calling find_by_author, call number: {find_by_author_calls}")
    print(f"We are looking for the author's name: {author}")
    authors = Author.objects(fullname__iregex=author)
    result = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result.extend([q.quote for q in quotes])
    return result


@cache
def find_by_tags(tags: List[str]) -> List[str]:
    global find_by_tags_calls
    find_by_tags_calls += 1
    print(f"Calling find_by_tags, call number: {find_by_tags_calls}")
    quotes = Quote.objects(tags__in=tags)
    result = [q.quote for q in quotes]
    return result


def process_command(command: str) -> bool:
    if command.startswith("name:"):
        author = command[len("name:") :].strip()
        quotes = find_by_author(author)
        for quote in quotes:
            print(quote.encode("utf-8").decode("utf-8"))
    elif command.startswith("tag:"):
        tag = command[len("tag:") :].strip()
        quotes = find_by_tag(tag)
        for quote in quotes:
            print(quote.encode("utf-8").decode("utf-8"))
    elif command.startswith("tags:"):
        tags = command[len("tags:") :].strip().split(",")
        quotes = find_by_tags(tags)
        for quote in quotes:
            print(quote.encode("utf-8").decode("utf-8"))
    elif command == "exit":
        print("Exiting...")
        return False
    else:
        print("Unknown command.")
    return True

def main():
    seed_data()
    while True:
        command = input("Enter command: ")
        if not process_command(command):
            break

if __name__ == "__main__":
    main()
