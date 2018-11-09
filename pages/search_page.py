import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from helpers.common_elements import Field, Button, BasePage
from helpers.waiter import Wait


class MailSearchPageLocators(object):
    search_fld = (By.NAME, 'q')
    submit_btn = (By.XPATH, '//button[@type="submit"]')
    suggestions_block = (By.ID, 'go-suggests')
    suggestions = (By.CLASS_NAME, 'go-suggests__item')
    clear_btn = (By.ID, 'MSearch-clear')
    fact = (By.CLASS_NAME, 'go-suggests__item__fact')
    converter = (By.CLASS_NAME, 'go-suggests__item__converter')
    weather = (By.XPATH, '//span[contains(@class, "go-suggests__item__weather")]')


class MailSearchPage(BasePage):

    def elements_to_wait(self):
        Wait.for_presence(self.driver, *MailSearchPageLocators.search_fld)
        Wait.for_presence(self.driver, *MailSearchPageLocators.submit_btn)

    @allure.step('Установка значения в поле поиска')
    def set_search_field(self, value):
        search_fld = Field(self.driver, *MailSearchPageLocators.search_fld)
        search_fld.set_value(value)

    @allure.step('Получение значения поля поиска')
    def get_search_field_value(self):
        search_fld = Field(self.driver, *MailSearchPageLocators.search_fld)
        return search_fld.get_value()

    @allure.step('Ожидание загрузки саджестов')
    def wait_for_suggestions(self):
        Wait.for_visibility(self.driver, *MailSearchPageLocators.suggestions_block)

    @allure.step('Получение всех элементов с саджестами')
    def get_suggestions_rows(self):
        self.wait_for_suggestions()
        return self.driver.find_elements(*MailSearchPageLocators.suggestions)

    @allure.step('Получение текста из саджестов')
    def get_suggestions_text(self):
        self.wait_for_suggestions()
        return [i.text for i in self.driver.find_elements(*MailSearchPageLocators.suggestions)]

    @allure.step('Поиск наличия фактов в саджестах')
    def get_suggestion_fact(self):
        self.wait_for_suggestions()
        try:
            return self.driver.find_element(*MailSearchPageLocators.fact).text.replace('—', '').strip()
        except NoSuchElementException:
            return None

    @allure.step('Поиск наличия результатов конвертирования в саджестах')
    def get_suggestion_converter(self):
        self.wait_for_suggestions()
        try:
            return self.driver.find_element(*MailSearchPageLocators.converter).text.replace('—', '').strip()
        except NoSuchElementException:
            return None

    @allure.step('Поиск результатов поиска погоды в саджестах')
    def get_suggestion_weather(self):
        self.wait_for_suggestions()
        try:
            return self.driver.find_element(*MailSearchPageLocators.weather).text.replace('—', '').strip()
        except NoSuchElementException:
            return None

    @allure.step('Выбор саджеста по его тексту')
    def select_suggestion_by_text(self, text):
        result = None
        for element in self.get_suggestions_rows():
            if element.text == text:
                result = element
        result.click()

    @allure.step('Очистка формы поиска')
    def click_clear_button(self):
        clear_btn = Button(self.driver, *MailSearchPageLocators.clear_btn)
        clear_btn.click()