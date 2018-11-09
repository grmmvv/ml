import selenium.webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from helpers.common import attach_screenshot

TIMEOUT = 10


class Wait(object):

    @staticmethod
    def for_presence(driver: selenium.webdriver.Remote, locator: By, locator_value: str, message='', timeout=TIMEOUT):
        if not message:
            message = 'Таймаут ожидания присутствия в DOM элемента "{}"'.format(locator_value)
        try:
            WebDriverWait(driver, timeout).until(ec.presence_of_element_located((locator, locator_value)), message=message)
        except TimeoutException:
            attach_screenshot(driver, name='Страница где превышено ожидание элемента: "{}"'.format(locator_value))
            raise TimeoutException(message)

    @staticmethod
    def for_visibility(driver: selenium.webdriver.Remote, locator: By, locator_value: str, message='', timeout=TIMEOUT):
        if not message:
            message = 'Таймаут ожидания видимости элемента "{}"'.format(locator_value)
        try:
            WebDriverWait(driver, timeout).until(
                ec.visibility_of_element_located((locator, locator_value)), message=message
            )
        except TimeoutException:
            attach_screenshot(driver, name='Страница где превышено ожидание видимости элемента: "{}"'.format(locator_value))
            raise TimeoutException(message)

    @staticmethod
    def for_invisibility(driver: selenium.webdriver.Remote, locator: By, locator_value: str, message='', timeout=TIMEOUT):
        if not message:
            message = 'Таймаут ожидания невидимости элемента "{}"'.format(locator_value)
        try:
            WebDriverWait(driver, timeout).until(
                ec.invisibility_of_element_located((locator, locator_value)), message=message
            )
        except TimeoutException:
            attach_screenshot(driver,
                              name='Страница где превышено ожидание невидимости элемента: "{}"'.format(locator_value))
            raise TimeoutException(message)

    @staticmethod
    def for_clickable(driver: selenium.webdriver.Remote, locator: By, locator_value: str, message='', timeout=TIMEOUT):
        if not message:
            message = 'Таймаут ожидания видимости элемента "{}"'.format(locator_value)
        try:
            WebDriverWait(driver, timeout).until(ec.element_to_be_clickable((locator, locator_value)), message=message)
        except TimeoutException:
            attach_screenshot(driver,
                              name='Страница где превышено ожидание кликабельности элемента: "{}"'.format(locator_value))
            raise TimeoutException(message)

    @staticmethod
    def for_page_reload(driver: selenium.webdriver.Remote, message='', timeout=TIMEOUT):
        if not message:
            message = 'Превышено время ожидания перезагрузки страницы'
        el_for_stale = driver.find_element_by_xpath('//body')
        try:
            WebDriverWait(driver, timeout).until(ec.staleness_of(el_for_stale), message=message)
        except TimeoutException:
            attach_screenshot(driver, name='Страница где превышено ожидание перезагрузки')
            raise TimeoutException(message)

    @staticmethod
    def for_url_to_be(driver: selenium.webdriver.Remote, url: str, message='', timeout=TIMEOUT):
        if not message:
            message = 'Превышено время ожидания изменения URL'
        try:
            WebDriverWait(driver, timeout).until(ec.url_to_be(url), message=message)
        except TimeoutException:
            attach_screenshot(driver, name='Страница где превышено ожидание изменение URL')
            raise TimeoutException(message)
