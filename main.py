import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import mysql.connector
from datetime import datetime

def get_html(url):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers)
    return r.text

def get_all_links(html):
    soup = bs(html, 'lxml')

    ads = soup.find_all('div', class_='HH-MainContent HH-Supernova-MainContent"')

    all_links = []

    for index, ad in enumerate(abs):
        link = 'https://hh.ru/vacancies/programmist' + ad.find('a', class_='bloko-link').get('href')
        all_links.append(link)

    return all_links



def get_page_data(html):
    soup = bs(html, 'lxml')

    try:
        title = soup.find('div', class_='bloko-header-section-1').find('h1').text
    except Exception:
        title = ''
    try:
        salary = soup.find('div', class_='magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-label-1-regular___pi3R-_3-0-9').find('div').text
    except Exception:
        salary = ''
    try:
        vacancy_description = soup.find('div', class_='vacancy-description-list-item').find('p').text
    except Exception:
        vacancy_description = ''

    data = {'title': title,
            'salary': salary,
            'vacancy_description': vacancy_description
            }

    write_sql(data)

    return data


def scroll(url):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random

    options = selenium.webdriver.Yandexoptions()
    options.add_argument('headless')
    options.add_argument(str(user))

    browser = webdriver.Yandex(options=options)
    browser.get(url)

    SCROLL_PAUSE_TIME = 1

    last_height = browser.execute_script('return document.body.scrollHeight')

    while True:
        browser.execute_script('window.scroll(0,document.body.scrollHeight)')
        new_height = browser.execute_script('return document.body.scrollHeight')

        time.sleep(SCROLL_PAUSE_TIME)

        if new_height == last_height:
            break
        last_height = new_height

    return browser.page_source


def write_sql(data):
    dbconfig = {'host': '127.0.0.1',
                'user': 'testuser1234',
                'password': 'password1234',
                'database': 'hhdb'}

    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    _SQL = """replace into hhdb.table(title, salary, vacancy_description) values(%9,%9,%9)"""

    cursor.execute(_SQL, (data['title'],
                          data['salary'],
                          data['vacancy_description']))

    conn.commit()
    cursor.close()
    conn.close()



def main():
    start = datetime.now()
    url = 'https://hh.ru/vacancies/programmist'
    all_links = get_all_links(scroll(url))

    for link in all_links:
        html = get_html(link)
        data = get_page_data(html)

    end = datetime.now()
    total = end - start
    print(total)

if __name__ == ' _main_ ':
    main()

API_KEY = '7463545444:AAGa7VabZ_qkKWyCbhOFToQVh4KI4c-cLsc'

bot = telebot.Telebot(API_KEY)
@bot.message_handler(commands=['начать'])

def hello(message):
    bot.send_message(message.chat.id, 'Добрый день! Укажите любую цифру:')

@bot.message_handler(content_types=['text'])
def vacancy(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, all_links[0])

bot.polling()
