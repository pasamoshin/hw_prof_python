from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
from pprint import pprint

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
headers = Headers(browser='firefox', os='win').generate()


html_vacancy = requests.get(HOST, headers=headers).text

soup = BeautifulSoup(html_vacancy, features='lxml')

all_vacancies = soup.find(id='a11y-main-content')
vacancies_tags = all_vacancies.find_all('a', attrs={'class':'serp-item__title'})
print(vacancies_tags)
# ip_div = soup.find(id='d_clip_button').find('span').text

# for div in vacancies_tags:
#     vacancy_name = div.find(class_ ='serp-item__title')
#     print(vacancy_name)

