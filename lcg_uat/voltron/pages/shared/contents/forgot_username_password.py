from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.js_functions import mouse_event_click as safari_click
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class VerifyUserDetails(BaseContent):
    _email_field = 'xpath=.//input[@name="email"]'
    _day_dropdown = 'xpath=.//select[@name="day"] | .//input[@name= "day"]'
    _month_dropdown = 'xpath=.//select[@name="month"] | .//input[@name= "month"]'
    _year_input = 'xpath=.//input[@name="year"]'
    _submit_btn = 'xpath=.//button[@class="btn submit btn-primary w-100"] | .//*[contains(@class,"submit")] | .//button[@class="btn btn-primary w-100"]'
    _no_longer_mobile_num = 'xpath=.//a[contains(@class,"cursorPointer")]'

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit_btn)

    @property
    def enter_email(self):
        return self._find_element_by_selector(selector=self._email_field, context=self._we).get_attribute('value')

    @enter_email.setter
    def enter_email(self, value):
        we = self._find_element_by_selector(selector=self._email_field, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    @property
    def day_dropdown(self):
        return self._find_element_by_selector(selector=self._day_dropdown, context=self._we)

    @property
    def day(self):
        return self.day_dropdown.value

    @day.setter
    def day(self, value):
        we = self._find_element_by_selector(selector=self._day_dropdown, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    @property
    def month_dropdown(self):
        return self._find_element_by_selector(selector=self._month_dropdown, context=self._we)

    @property
    def month(self):
        return self.month_dropdown.value

    @month.setter
    def month(self, value):
        we = self._find_element_by_selector(selector=self._month_dropdown, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    @property
    def year(self):
        return self._find_element_by_selector(selector=self._year_input, context=self._we).get_attribute('value')

    @year.setter
    def year(self, value):
        we = self._find_element_by_selector(selector=self._year_input, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    @property
    def no_longer_mobile_num(self):
        return self._find_element_by_selector(selector=self._no_longer_mobile_num, context=self._we)


class ForgotPassword (VerifyUserDetails):
    _user_input = 'xpath=.//*[@name="userid"] | .//*[@formcontrolname="lostPasswordEmail"]'
    _submit_btn = 'xpath=.//*[@class="btn submit btn-primary w-100"] | .//*[contains(@class,"submit")] | .//button[@class="btn btn-primary w-100"]'
    _live_chat = 'xpath=.//button[contains(text(), "Live Chat")]'
    _contact_us = 'xpath=.//*[@id="contactButton"] | .//a[contains(text(), "CONTACT US")]'
    _forgot_password_title = 'xpath=.//*[contains(@class,"header-ctrl-txt")]'
    _forgot_password = 'xpath=.//*[contains(@data-tracking-values, "Password")]'
    _change_password = 'xpath=.//*[@class="theme-check ng-star-inserted"]| .//*[@class="txt-md-v2 txt-color-100"]'

    @property
    def reset_password(self):
        return self._find_element_by_selector(selector=self._change_password, context=self._we)

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)

    @property
    def password(self):
        return LinkBase(selector=self._forgot_password)

    @property
    def live_chat(self):
        return ComponentBase(selector=self._live_chat, context=self._we)

    @property
    def contact_us(self):
        return ComponentBase(selector=self._contact_us, context=self._we)

    @property
    def header_title_forgot_password(self):
        return self._find_element_by_selector(selector=self._forgot_password_title, context=self._we)

    @property
    def username_input(self):
        return self._find_element_by_selector(selector=self._user_input, context=self._we)

    @username_input.setter
    def username_input(self, value):
        we = self._find_element_by_selector(selector=self._user_input, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit_btn)
