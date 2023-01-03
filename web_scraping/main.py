from application.parser import *


if __name__ == '__main__':
    # Передаю начальный url
    url = "/search/vacancy?text=python&area=1&area=2"
    # Устанавливаю значения фильтрации
    filter = set_filter()
    # Выбор валюты
    currency = set_currency()

    while 1:
        con = WebRequest(url, 'firefox', 'win')
        data = con.request()
        pars = Parsing(data)
        l = pars.get_vacancies(currency, filter)
        # Получение ссылки на следующую страницу
        next_page = pars.get_link_next_page()
        if next_page:
            url = next_page
        else:
            print('Вакансии закончились')
            break
    # Сохранение в json
    save_vacancies(VACANCYS_LICT)
