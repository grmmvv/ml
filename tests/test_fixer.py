import json

from datetime import datetime

import allure
import pytest
import requests
import requests_mock

from conftest import ACCESS_KEY
from helpers.common import get_error_type, get_error_code, get_requests_status
from helpers.urls import URL

pytestmark = pytest.mark.skipif(not ACCESS_KEY, reason='Для корректной работы требуется активный ключ к Fixer API в conftest.py')


@allure.title('Deprecated методы API не должны работать и должны отдавать deprecated-подсказку')
def test_deprecated_api_is_not_working():
    url = URL.old_fixer_api_url
    response = requests.get(url)
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    assert 'endpoint is deprecated' in response.text, 'Текст об устаревании методов не обнаружен при обращении к ним'


@allure.title('Эндпоинты не должны работать без ключа доступа')
def test_latest_api_not_working_wo_access_key():
    url = 'http://data.fixer.io/api/latest'
    response = requests.get(url)
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    assert get_requests_status(response) == False, 'Некорректный запрос вернул успешный статус'
    assert get_error_code(response) == 101, 'Запрос без ключа доступа вернул неверный код ошибки'
    assert get_error_type(response) == 'missing_access_key', 'Запрос без ключа доступа вернул некорректную ошибку'


@pytest.mark.parametrize('access_key', [
    'text',
    '098f6bcd4621d373cade4e832627b4f6'
])
@allure.title('Эндпоинты не должны принимать произвольный текст "{access_key}" в качестве ключа доступа')
def test_latest_api_not_working_w_invalid_key(access_key):
    url = URL.latest_fixer_api_url
    response = requests.get(url, params={'access_key': access_key})
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    assert get_requests_status(response) == False
    assert get_error_code(response) == 101, 'Запрос с некорректным ключом доступа вернул неверный код ошибки'
    assert get_error_type(response) == 'invalid_access_key', 'Запрос с некорректным ключом доступа вернул некорректную ошибку'


@pytest.mark.parametrize('endpoint_url', [
    URL.latest_fixer_api_url,
    URL.get_fixer_url_for_date('2000', '01', '03'),
])
@allure.title('Базовый бесплатный план не должен включать в себя доступ к смене базовой валюты')
def test_free_subscription_plan_with_base_argument(endpoint_url):
    response = requests.get(endpoint_url, params={'access_key': ACCESS_KEY, 'base': 'USD'})
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    assert get_requests_status(response) == False, 'Запрос с бесплатным планом прошел успешно'
    assert get_error_code(response) == 105, 'Код ошибки отличается от ожидаемого'
    assert get_error_type(response) == 'base_currency_access_restricted', 'Текст ошибки отличается от ожидаемого'


@pytest.mark.parametrize('endpoint_url', [
    URL.latest_fixer_api_url,
    URL.get_fixer_url_for_date('2000', '01', '03'),
])
@allure.title('Обращение к одной неизвестной валюте должно возвращать ошибку')
def test_single_invalid_currency_symbols(endpoint_url):
    response = requests.get(endpoint_url, params={'access_key': ACCESS_KEY, 'symbols': 'NOPE'})
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    assert get_requests_status(response) == False, 'Запрос с неверной валютой прошел успешно'
    assert get_error_code(response) == 202, 'Код ошибки отличается от ожидаемого'
    assert get_error_type(response) == 'invalid_currency_codes', 'Текст ошибки отличается от ожидаемого'


@pytest.mark.parametrize('endpoint_url', [
    URL.latest_fixer_api_url,
    URL.get_fixer_url_for_date('2000', '01', '03'),
])
@allure.title('Использование неправильных кодов валют одновременно с правильными не должно вызывать ошибок')
@allure.description('Неправильные коды валют должны быть проигнорированы и не должны отображаться в результатах')
def test_multiple_invalid_currency_symbols(endpoint_url):
    response = requests.get(endpoint_url, params={'access_key': ACCESS_KEY, 'symbols': 'USD,NOPE,TEST,RUB'})
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    assert ('NOPE', 'TEST') not in list(response.json().get('rates').keys())


@allure.title('Получение данных с base-аргументов с испльзованием mock')
@allure.description('В идеале нужно использовать нормальный план, но так как у меня его нет я сделал пример с mock')
def test_fixer_api_with_mock(mocker_response):
    params = {
        'access_key': ACCESS_KEY,
        'base': 'USD',
        'symbols': 'EUR,RUB'
    }
    output_json, endpoint_url = mocker_response
    with requests_mock.Mocker() as m:
        m.get(endpoint_url, text=json.dumps(output_json))
        response = requests.get(endpoint_url, params=params)
    assert response.status_code == 200, 'Запрос вернул отличный от ожидаемого статус код'
    if get_requests_status(response) != True:
        pytest.fail(
            'Запрос выполнен с ошибкой: "{}", код ошибки: {}'.format(get_error_type(response),
                                                                     get_error_code(response)))
    assert datetime.utcfromtimestamp(response.json().get('timestamp')).strftime('%Y-%m-%d') == response.json().get('date')
    assert response.json().get('base') == params.get('base'), 'Базовая валюта должна соответствовать ожидаемой'
    assert params.get('symbols').split(',') == list(response.json().get('rates').keys()), 'Список валют должен соответствовать ожидаемому'
