import json
import re
from bs4 import BeautifulSoup as bs
import requests
from fake_headers import Headers
from pprint import pprint


VACANCYS_LICT = []


class WebRequest():
    def __init__(self, url, browser, os):
        self.url = 'https://spb.hh.ru' + url
        self.headers = Headers(browser=browser, os=os).generate()

    def request(self):
        req = requests.get(self.url, headers=self.headers)

        if req.status_code == 200:
            return req.text
        else:
            print(req)


class Parsing():
    def __init__(self, data) -> None:
        self.soup = bs(data, features='lxml')

    def filling_values(self, list):
        if list == None:
            list = '-'
        else:
            list = list.text
        return list

    def get_link_next_page(self):
        try:
            link_next = self.soup.find('a', {'data-qa': 'pager-next'})['href']
        except:
            link_next = None
        return link_next

    def get_vacancys(self):
        data = self.soup.find(
            id='a11y-main-content').find_all(class_='vacancy-serp-item__layout')

        for vacancy in data:
            name = vacancy.find(class_='serp-item__title').text
            organization = vacancy.find(
                class_='bloko-link bloko-link_kind-tertiary').text

            compensation = vacancy.find(
                'span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            compensation = self.filling_values(compensation)

            city = vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]

            description = vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
            description = self.filling_values(description)

            requirements = vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
            requirements = self.filling_values(requirements)

            link = vacancy.find(class_='serp-item__title')['href']

            vacancy = {'name': name, 'organization': organization,
                       'compensation': compensation, 'city': city,
                       'description': description, 'requirements': requirements,
                       'link': link
                       }

            VACANCYS_LICT.append(vacancy)
            # print(vacancy)
            del vacancy


    def filter_vacancy(self):
        data = self.soup.find(
            id='a11y-main-content').find_all(class_='vacancy-serp-item__layout')
        id = 1
        for vacancy in data:
            description = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}, 
                                        text=re.compile('([Dd]jango)'))
            description
            requirements =  vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}, text=re.compile('([Dd]jango)'))
            
            
            if description:
                print(description.text)
                print()
            if requirements:
                print(requirements.text + description.text)
            print("-"*10)

        


def save_vacancys(data):
    with open('vacancys.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    url = "/search/vacancy?text=python&area=1&area=2"
    while 1:
        con = WebRequest(
            url, 'firefox', 'win')
        data = con.request()
        pars = Parsing(data)
        l = pars.get_vacancys()
        next_page = pars.get_link_next_page()
        if next_page:
            url = next_page
        else:
            print('Вакансии закончились')
            break

        f = pars.filter_vacancy()
    # save_vacancys(VACANCYS_LICT)
    

    
