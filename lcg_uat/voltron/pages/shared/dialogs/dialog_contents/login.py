from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.inputs import PasswordInput
from voltron.pages.shared.contents.forgot_username_password import ForgotPassword
from voltron.pages.shared.dialogs.dialog_base import DialogHeader
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.js_functions import mouse_event_click as safari_click
from voltron.utils.waiters import wait_for_result


class RememberMe(ComponentBase):
    _checkbox = 'xpath=.//label[@for="rememberMe"]'
    _input = 'xpath=.//input[@id="rememberMe"]'
    _text = 'xpath=//*[@data-crlat="rememberMeText"]'

    @property
    def input(self):
        return self._find_element_by_selector(selector=self._input, context=self._we)

    def is_checked(self, expected_result=True):
        return wait_for_result(lambda: self.input.is_selected(),
                               timeout=3,
                               name=f'"{self.__class__.__name__}" Checkbox status to be {expected_result}',
                               expected_result=expected_result)

    def click(self):
        we = self._find_element_by_selector(selector=self._checkbox)
        if we is None:
            we = self._find_element_by_selector(selector=self._input)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text, context=self._we)


class LogInDialogHeader(DialogHeader):
    _title = 'xpath=.//*[contains(@class, "header-ctrl-txt")]'
    _close_button = 'xpath=.//span[contains(@class, "close")]'


class LogIn(Dialog):
    _dialog_content = 'xpath=.//*[@id="login"]'
    _dialog_header = 'xpath=.//vn-header-bar'
    _dialog_header_type = LogInDialogHeader
    _error_message = 'xpath=.//vn-message-panel'
    _username_input = 'xpath=.//*[@id="username"]/input'
    _password_input = 'xpath=.//*[@id="password"]/input'
    _password_input_type = PasswordInput
    _remember_me = 'xpath=.//lh-remember-me'
    _remember_me_type = RememberMe
    _login_button = 'xpath=.//button[contains(@class, "login")] | .//*[@class="login w-100 btn btn-primary"]'
    _forgot_password_link = 'xpath=.//*[contains(@data-tracking-values, "ForgottenPassword")] | .//*[@class="forgot-password"]'
    _forgot_username_link = 'xpath=.//*[contains(@data-tracking-values, "ForgottenUsername")] | .//*[@class="forgot-username"]'
    _forgot_password_type = ForgotPassword
    _forgot_four_digit_pin_link = 'xpath=.//*[contains(@data-tracking-values, "Forgotten Pin")]'
    _join_us_button = 'xpath=.//button[contains(text(), "Register")] | .//button[contains(text(), "REGISTER")]'
    _create_an_account = 'xpath=.//*[contains(text(), "Create an account")]'
    _error_message_box = 'xpath=.//div[contains(@class, "theme-error-i ng-star-inserted")]'
    _connect_card_toggle = 'xpath=.//a[contains(text(),"Connect Card")]'
    _online_toggle = 'xpath=.//label[contains(text(),"Online")]'
    _connect_card_number = 'xpath=.//div[@id="connectCardNumber"]/input'
    _connect_card_pin = 'xpath=.//div[@id="pin"]/input'
    _forgot_password_text = 'xpath=.//div[@class="pc-txt txt-s mb-0 ng-star-inserted"][1]/p'

    @property
    def forgot_password(self):
        return self._forgot_password_type(selector=self._forgot_password_link, context=self._we)

    @property
    def forgot_four_digit_pin(self):
        return self._find_element_by_selector(selector=self._forgot_four_digit_pin_link, context=self._we)

    @property
    def connect_card_number_field(self):
        return self._find_element_by_selector(selector=self._connect_card_number, context=self._we)

    @property
    def forgot_username(self):
        return self._find_element_by_selector(selector=self._forgot_username_link, context=self._we)

    @property
    def create_an_account(self):
        return self._find_element_by_selector(selector=self._create_an_account, context=self._we)

    @property
    def username(self):
        return self._find_element_by_selector(selector=self._username_input, context=self._we).get_attribute('value')

    @username.setter
    def username(self, value):
        username_field = self.username_field
        username_field.click()
        username_field.clear()
        username_field.value = value

    @property
    def username_field(self):
        return InputBase(selector=self._username_input, context=self._we)

    @property
    def remember_me(self):
        return self._remember_me_type(selector=self._remember_me, context=self._we)

    @property
    def password(self):
        return self._password_input_type(selector=self._password_input, context=self._we)

    @password.setter
    def password(self, value):
        password = self.password
        password.clear()
        password.value = value

    def click_login(self, spinner_wait=True):
        self.login_button.is_displayed(timeout=3, name='Login button is visible')
        self.login_button.is_enabled()
        self.login_button.click()
        try:
            self.login_button.click()
        except Exception as e:
            pass
        self._spinner_wait() if spinner_wait else None

    @property
    def error_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._error_message, context=self._we, timeout=3)

    def wait_error_message(self):
        return wait_for_result(lambda: self._get_webelement_text(selector=self._error_message, context=self._we, timeout=0) != '',
                               expected_result=True,
                               name=f'{self.__class__.__name__} - Error message appears',
                               timeout=15)

    def wait_for_error_message_to_change(self, expected_message, timeout=2):
        return wait_for_result(lambda: self._get_webelement_text(selector=self._error_message, context=self._we, timeout=0) == expected_message,
                               name=f'LogIn dialog error message to be "{expected_message}"',
                               expected_result=True,
                               timeout=timeout)

    @property
    def join_us(self):
        return ButtonBase(selector=self._join_us_button, context=self._we)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we)

    @property
    def online_toggle(self):
        return LoginToggleButton(selector=self._online_toggle, context=self._we)

    @property
    def connect_card_toggle(self):
        return LoginToggleButton(selector=self._connect_card_toggle, context=self._we)

    @property
    def connect_card_number(self):
        return self._find_element_by_selector(selector=self._connect_card_number, context=self._we).get_attribute(
            'value')

    @connect_card_number.setter
    def connect_card_number(self, value):
        we = self._find_element_by_selector(selector=self._connect_card_number, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.clear()
        we.send_keys(value)

    @property
    def connect_card_pin(self):
        return self._password_input_type(selector=self._connect_card_pin, context=self._we)

    @connect_card_pin.setter
    def connect_card_pin(self, value):
        we = self._find_element_by_selector(selector=self._connect_card_pin, context=self._we)
        we.clear()
        we.send_keys(value)

    @property
    def register_now_button(self):
        return self.join_us

    @property
    def error_message_exclamation_mark(self):
        return self.before_element(selector=self._error_message_box, context=self._we)

    @property
    def forgot_password_text(self):
        return self._find_element_by_selector(selector=self._forgot_password_text, context=self._we)


class LoginToggleButton(ButtonBase):

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: '1px solid rgb(0, 0, 0)' in self.css_property_value('border'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result
