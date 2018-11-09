import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from helpers.waiter import Wait
from helpers.common_elements import BasePage


class ResultsPageLocators(object):
    results_block = (By.CLASS_NAME, 'result')


class ResultsPage(BasePage):

    def elements_to_wait(self):
        Wait.for_visibility(self.driver, *ResultsPageLocators.results_block)

    @allure.step('Проверка на наличие результатов поиска')
    def has_results(self):
        try:
            self.driver.find_element_by_class_name('not-found')
            return False
        except NoSuchElementException:
            return True
