import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from helpers.urls import URL

ACCESS_KEY = ''  # в идеале нужно его хранить не здесь, а где-то удаленно


@pytest.fixture
def driver():
    options = Options()
    options.headless = True
    with allure.step('Запускаем локальный инстанс браузера'):
        driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.fixture(params=[
    URL.latest_fixer_api_url,
    URL.get_fixer_url_for_date('2000', '01', '03'),
])
def mocker_response(request):
    with allure.step('Получение списка валют относительно EUR'):
        input_params = {'access_key': ACCESS_KEY, 'symbols': 'EUR,RUB,USD'}
        input_request = requests.get(request.param, params=input_params)
        assert input_request.status_code == 200
    with allure.step('Пересчет валют относительно USD'):
        input_json = input_request.json()
        eur_in_usd = round(1 / input_json.get('rates').get('USD'), 6)
        rub_in_usd = round(input_json.get('rates').get('RUB') * eur_in_usd, 6)
    with allure.step('Формирование ответа от API относительно USD'):
        output_json = input_json.copy()
        output_json['base'] = 'USD'
        output_json['rates'] = {'EUR': eur_in_usd, 'RUB': rub_in_usd}
    return output_json, request.param
