import allure
import pytest
import selenium.webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from helpers.waiter import Wait


class PageElement(object):

    def __init__(self, driver: selenium.webdriver.Remote, locator: By, locator_value: str):
        self.browser = driver
        self.find_by = locator
        self.find_value = locator_value
        self.element = self.__get_element__

    def __get_element__(self):
        try:
            return self.browser.find_element(self.find_by, self.find_value)
        except NoSuchElementException:
            if isinstance(self.browser, WebElement):
                message = 'Не удалось найти элемент \'{}\' по его "{}"'.format(self.find_value, self.find_by)
            else:
                message = 'Не удалось найти элемент \'{}\' на странице "{}" по его "{}"'.format(
                    self.find_value, self.browser.current_url, self.find_by
                )
            raise NoSuchElementException(message)


class Field(PageElement):

    def clear_value(self):
        self.element().clear()
        if self.get_value():
            self.element().send_keys(Keys.CONTROL + 'a')
            self.element().send_keys(Keys.DELETE)

    def set_value(self, value):
        Wait.for_clickable(self.browser, self.find_by, self.find_value)
        self.clear_value()
        self.element().send_keys(str(value))
        assert self.element().get_attribute('value')

    def update_value(self, value):
        self.element().send_keys(value)

    def get_value(self):
        return self.element().get_attribute('value')


class Button(PageElement):

    def click(self):
        self.element().click()

    def is_active(self):
        return self.element().is_enabled()

    def is_visible(self):
        return self.element().is_displayed()


class BasePage(object):

    def __init__(self, driver: selenium.webdriver.Chrome, url=None):
        self.driver = driver
        self.url = url

    def __call__(self, url=None):
        self.url = url

    def transfer(self):
        with allure.step('Переход на странцу: {}'.format(self.url)):
            self.driver.get(self.url)

    def elements_to_wait(self):
        pass

    @allure.step('Ожидание загрузки основных элементов страницы')
    def wait_for_load(self):
        try:
            self.elements_to_wait()
        except TimeoutException as e:
            pytest.fail(e.msg)