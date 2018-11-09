import logging

import allure
import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from helpers.common import allure_attach_json
from helpers.urls import URL
from pages.results_page import ResultsPage
from pages.search_page import MailSearchPage


@pytest.mark.parametrize('search_query', [
    'selenium',
    'python 3',
    'как сделать игру',
    'қымыз',
    'бульба',
    'київ'
])
@allure.title('Все саджесты должны содержать в себе введеный в поле поиска текст')
def test_suggests_contains_search_request(driver, search_query):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(search_query)
    suggestions = search_page.get_suggestions_text()
    assert suggestions, 'Саджесты не обнаружены'
    if not all(search_query in i for i in suggestions):
        allure_attach_json(suggestions)
        pytest.fail('В некоторых саджестах не обнаружен поисковый запрос')
    search_page.select_suggestion_by_text(suggestions[3])
    results_page = ResultsPage(driver)
    results_page.wait_for_load()
    assert results_page.has_results()


@pytest.mark.parametrize('search_query,expected', [
    ('ntcn', 'тест'),
    ('знерщт 3', 'python 3'),
    ('сила njrf', 'сила тока'),
    ('майнкравт', 'майнкрафт'),
    ('как зделать', 'как сделать'),
    ('crfxfnm музыку', 'скачать музыку'),
])
@allure.title('Саджесты должны правильно отображать введенный в неправильной раскладке поисковый запрос')
def test_suggests_with_invalid_layout(driver, search_query, expected):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(search_query)
    suggestions = search_page.get_suggestions_text()
    assert suggestions, 'Саджесты не обнаружены'
    if not all(expected in i for i in suggestions):
        allure_attach_json(suggestions)
        for i in suggestions:
            if expected not in i:
                logging.error(i)
        pytest.fail('В некоторых саджестах не обнаружен поисковый запрос')


@allure.title('Саджесты и строка поиск должны очищаться после клика по кнопке "стереть"')
def test_clear_button(driver):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field('selenium')
    suggestions = search_page.get_suggestions_text()
    assert suggestions, 'Саджесты не обнаружены'
    search_page.click_clear_button()
    assert not search_page.get_search_field_value()
    with pytest.raises(TimeoutException):
        search_page.get_suggestions_text()


@pytest.mark.parametrize('search_query', [
    'selenium',
    'python 3 уроки',
    'как сделать игру'
])
@allure.title('Текст введенный в поле поиска должен выделяться в саджестах жирным')
def test_suggests_highlighting(driver, search_query):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(search_query)
    suggests = search_page.get_suggestions_rows()
    assert suggests
    for row in suggests:
        row_text = row.find_element_by_xpath('.//span[@class="go-suggests__ellipsis"]')
        for word in search_query.split():
            try:
                row_text.find_element_by_xpath('.//b[text()="{}"]'.format(word))
            except NoSuchElementException:
                pytest.fail('Часть запроса "{}" в саджесте "{}" не выделена жирным'.format(word, row_text.text))


@pytest.mark.parametrize('proper_layout,invalid_layout', [
    ('скачать музыку' ,'crfxfnm vepsre')
])
@allure.title('Саджесты для правильной и неправильно раскладок должны быть одинаковы')
def test_suggests_for_invalid_and_proper_layouts_are_same(driver, proper_layout, invalid_layout):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(proper_layout)
    proper_suggests = search_page.get_suggestions_text()
    search_page.set_search_field(invalid_layout)
    invalid_suggests = search_page.get_suggestions_text()
    assert proper_suggests == invalid_suggests


@pytest.mark.parametrize('search_query,expected', [
    ('столица канады', 'Оттава'),
    ('где находится статуя свободы', 'Нью-Йорк'),
    ('где находится стоунхендж', 'Эймсбери'),
])
@allure.title('При поиске в саджестах должны отображаться факты для популярных запросов')
def test_suggests_for_facts(driver, search_query, expected):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(search_query)
    fact = search_page.get_suggestion_fact()
    assert expected == fact


@pytest.mark.parametrize('search_query,expected', [
    ('сколько минут в сутках', '1440 минуты'),
    ('сколько километров', '1000 метров'),
])
@allure.title('Тест конвертора величин в саджестах')
def test_suggests_for_converters(driver, search_query, expected):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(search_query)
    fact = search_page.get_suggestion_converter()
    assert expected == fact


@pytest.mark.parametrize('search_query', [
    'погода',
    'погода в москве',
])
@allure.title('Тест отображения погоды в саджестах')
def test_suggests_for_weather(driver, search_query):
    search_page = MailSearchPage(driver, url=URL.main_search_url)
    search_page.transfer()
    search_page.wait_for_load()
    search_page.set_search_field(search_query)
    fact = search_page.get_suggestion_weather()
    assert fact
