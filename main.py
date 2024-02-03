import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

TELEGRAM_BOT_TOKEN = '6659085594:AAGtTCw3wnwidiBL5A76zQ9fT7GfTClOhmA'
TELEGRAM_CHANNEL_ID = '@orthodoxtwahedoo'
WEBSITE_URL = 'https://etcareers.com/jobs/'

def fetch_website_data():
    response = requests.get('https://etcareers.com/jobs/')
    if response.status_code == 200:
        return response.text
    else:
        return None

def send_to_telegram(message):
    bot = Bot(token='6659085594:AAGtTCw3wnwidiBL5A76zQ9fT7GfTClOhmA')
    bot.send_message(chat_id=656196513, text=message)

def scrape_and_send():
    previous_data = None

    while True:
        website_data = fetch_website_data()

        if website_data:
            soup = BeautifulSoup(website_data, 'lxml')
            jobs = soup.find_all('article', class_='media well listing-item listing-item__jobs listing-item__featured')

            for job in jobs:
                item_of_company = job.find('span', class_='listing-item__info--item listing-item__info--item-company')
                item_location = job.find('span', class_='listing-item__info--item listing-item__info--item-location')
                published_date = job.find('div', class_='listing-item__date')
                more_info = job.find('div', class_='media-body').a

                if item_location and item_of_company:
                    message = f"item_location: {item_location.text.strip()}\nitem_of_company: {item_of_company.text.strip()}"
                    if published_date:
                        message += f"\npublished_date: {published_date.text.strip()}"
                    if more_info:
                        message += f"\nmore_info: {more_info['href']}"

                    if message != previous_data:
                        send_to_telegram(message)
                        previous_data = message
                    else:
                        print("No update found.")

        time.sleep(60)

if __name__ == '__main__':
    scrape_and_send()


