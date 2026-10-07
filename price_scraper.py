# language: Python, file: price_scraper.py
# *парсер: собирает название, цену, ссылку с books.toscrape.com, сохраняет в CSV*
# *зависимости: pip install requests beautifulsoup4*
# *запуск: python price_scraper.py*

import csv
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
MAX_PAGES = 3
OUTPUT_FILE = "books.csv"
DELAY = 1.0  # пауза между запросами, чтобы не забанили


def fetch_page(url):
    """Скачивает страницу и возвращает HTML или None при ошибке."""
    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0 Safari/537.36"
        })
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[!] Ошибка запроса {url}: {e}")
        return None


def parse_page(html, page_url):
    """Парсит одну страницу, возвращает список книг."""
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    result = []

    for book in books:
        try:
            title = book.find("h3").find("a")["title"]
            price = book.find("p", class_="price_color").text.strip()
            relative_link = book.find("h3").find("a")["href"]
            # ссылки на страницах каталога относительные
            full_link = page_url.replace("index.html", "") + relative_link.lstrip("./")

            result.append({
                "title": title,
                "price": price,
                "link": full_link,
            })
        except (AttributeError, KeyError, TypeError) as e:
            print(f"[!] Не удалось распарсить элемент: {e}")
            continue

    return result


def scrape(base_url, max_pages):
    """Проходит по страницам каталога и собирает все книги."""
    all_books = []

    for page in range(1, max_pages + 1):
        if page == 1:
            url = base_url + "index.html"
        else:
            url = f"{base_url}catalogue/page-{page}.html"

        print(f"[*] Страница {page}: {url}")
        html = fetch_page(url)
        if not html:
            break

        books = parse_page(html, url)
        if not books:
            print("[*] Книг не найдено, останавливаемся.")
            break

        all_books.extend(books)
        print(f"[+] Собрано {len(books)} книг (всего: {len(all_books)})")

        if page < max_pages:
            time.sleep(DELAY)

    return all_books


def save_csv(data, filename):
    """Сохраняет список словарей в CSV."""
    if not data:
        print("[!] Нечего сохранять.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
        writer.writeheader()
        writer.writerows(data)

    print(f"[+] Сохранено {len(data)} записей в {filename}")


def main():
    print("[*] Старт парсинга...")
    data = scrape(BASE_URL, MAX_PAGES)
    save_csv(data, OUTPUT_FILE)
    print("[*] Готово.")


if __name__ == "__main__":
    main()