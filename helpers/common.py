import json

import allure
from requests import Response


def attach_screenshot(driver, element=None, name=None):
    def apply_style(style):
        parent.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)
    if element:
        parent = element._parent
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("window.scrollBy(0, -150);")
        original_style = element.get_attribute('style')
        apply_style('background: yellow; border: 2px solid red;')
        screenshot = driver.get_screenshot_as_png()
        apply_style(original_style)
    else:
        screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG, extension='PNG')


def allure_attach_json(obj: (dict, list), name=None):
    allure.attach(
     body=json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False),
     name=name,
     attachment_type=allure.attachment_type.JSON,
     extension='JSON'
)


def get_error_type(response: Response):
    return response.json().get('error').get('type')


def get_error_code(response: Response):
    return response.json().get('error').get('code')


def get_requests_status(response: Response):
    return response.json().get('success')
