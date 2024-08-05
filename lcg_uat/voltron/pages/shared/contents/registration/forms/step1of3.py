from voltron.pages.shared.contents.registration.forms.base_form import StepFormBase
from voltron.pages.shared.contents.registration.primitives.dropdown import RegistrationDropdown
from voltron.pages.shared.contents.registration.primitives.input import RegistrationInput
from voltron.utils.waiters import wait_for_result


class RegistrationPassword(RegistrationInput):
    _input = 'xpath=.//input[@formcontrolname="password"]'


class Step1Of3Form(StepFormBase):
    _country = 'xpath=.//pt-reg-country-of-residence'
    _country_type = RegistrationDropdown
    _currency = 'xpath=.//pt-reg-currency'
    _currency_type = RegistrationDropdown
    _email = 'xpath=.//pt-reg-email'
    _email_type = RegistrationInput
    _username = 'xpath=.//pt-reg-username'
    _username_type = RegistrationInput
    _password = 'xpath=.//pt-reg-password'
    _password_type = RegistrationPassword

    def submit_form(self):
        self.click()
        if self.has_username():
            wait_for_result(lambda: 'ng-touched ng-valid' in self.username.input.get_attribute('class'),
                            name='Username to be confirmed',
                            timeout=3)
        else:
            wait_for_result(lambda: 'ng-touched ng-valid' in self.email.input.get_attribute('class'),
                            name='Email to be confirmed',
                            timeout=3)
        self.step_button.click()

    @property
    def country(self):
        return self._country_type(selector=self._country, context=self._we, timeout=5)

    @property
    def currency(self):
        return self._currency_type(selector=self._currency, context=self._we, timeout=5)

    @property
    def email(self):
        return self._email_type(selector=self._email, context=self._we, timeout=5)

    @property
    def username(self):
        return self._username_type(selector=self._username, context=self._we)

    def has_username(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(self._username, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Username text box status to be "{expected_result}"')

    @property
    def password(self):
        return self._password_type(selector=self._password, context=self._we)

    def enter_values(self,
                     country=None,
                     email=None,
                     username=None,
                     password=None):
        if email:
            self.email.input.value = email
        if username:
            self.username.input.value = username
        if password:
            self.password.input.value = password
        if country:
            self.country.dropdown.value = country
