import allure
import pytest
import requests
from selenium import webdriver

from helpers.urls import URL

ACCESS_KEY = ''  # в идеале нужно его хранить не здесь, а где-то удаленно


@pytest.fixture
def driver():
    desired_caps = {
        'browserName': 'chrome',
        'version': '79.0',
        'enableVNC': False,
        'enableVideo': False,
        'sessionTimeout': '6m',
    }
    driver = webdriver.Remote(
        command_executor=f'http://localhost:4444/wd/hub',
        desired_capabilities=desired_caps,
        options=None,
    )
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
