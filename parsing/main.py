import requests
from bs4 import BeautifulSoup
import re
import time
from collections import Counter

URL = "https://sgaf.ru/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"
}


def get_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
        return None


def parse_price(price_text):
    if not price_text:
        return None
    numbers = re.findall(r'\d+', price_text.replace(" ", ""))
    if numbers:
        return int(numbers[0])
    return None


def main():
    html = get_html(URL)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")

    events = []


    cards = soup.find_all("div", class_=re.compile("event|card|afisha", re.I))


    if not cards:

        cards = soup.select("a[href*='/afisha/']")

    for card in cards:
        text = card.get_text(" ", strip=True)


        if len(text) < 20:
            continue


        date_match = re.search(r'(\d{1,2}\s+[а-яА-Я]+,\s+\d{1,2}:\d{2})', text)
        date_str = date_match.group(1) if date_match else "Дата не указана"


        price_match = re.search(r'от\s*([\d\s]+)\s*₽', text)
        price = parse_price(price_match.group(1)) if price_match else None


        lines = text.split("\n")
        title = "Неизвестное мероприятие"
        for line in lines:
            line = line.strip()
            if line and not re.search(r'от\s*\d', line) and not re.search(r'\d{1,2}:\d{2}', line) and len(line) > 5:
                title = line
                break


        place = "Свердловская филармония"
        if "зал" in text.lower():
            place_match = re.search(r'([А-Яа-я\s]+зал)', text)
            if place_match:
                place = place_match.group(1).strip()


        age = "12+"
        if "дет" in title.lower() or "сказка" in title.lower():
            age = "0+"

        events.append({
            "title": title,
            "date": date_str,
            "place": place,
            "price": price,
            "age": age
        })

    if not events:
        print("Не удалось найти события")
        return

    print(f"\nНайдено событий: {len(events)}")

    prices = [e["price"] for e in events if e["price"] is not None]

    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)

        cheapest = min((e for e in events if e["price"] is not None), key=lambda x: x["price"])
        priciest = max((e for e in events if e["price"] is not None), key=lambda x: x["price"])

        print(f"\nМинимальная цена: {min_price} ₽")
        print(f"Максимальная цена: {max_price} ₽")
        print(f"Средняя цена: {avg_price:.2f} ₽")
        print(f"\nСамое дешевое: '{cheapest['title']}' ({cheapest['price']} ₽)")
        print(f"Самое дорогое: '{priciest['title']}' ({priciest['price']} ₽)")
    else:
        print("Цены не найдены.")

    places = [e["place"] for e in events]
    if places:
        counter = Counter(places)
        popular_place, count = counter.most_common(1)[0]
        print(f"\nСамая загруженная площадка: {popular_place} ({count} событий)")

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write("АФИША КОНЦЕРТОВ\n\n")
        for i, e in enumerate(events, 1):
            f.write(f"{i}. {e['title']}\n")
            f.write(f"   Дата и время: {e['date']}\n")
            f.write(f"   Место: {e['place']}\n")
            f.write(f"   Цена: {e['price']} ₽\n")
            f.write(f"   Возраст: {e['age']}\n")
            f.write("-" * 30 + "\n")

        if prices:
            f.write(f"\nСтатистика:\n")
            f.write(f"Мин. цена: {min_price} ₽\n")
            f.write(f"Макс. цена: {max_price} ₽\n")
            f.write(f"Средняя цена: {avg_price:.2f} ₽\n")
        if places:
            f.write(f"Самая загруженная площадка: {popular_place} ({count})\n")

    print("\nРезультаты записаны в файл")


if __name__ == "__main__":
    main()