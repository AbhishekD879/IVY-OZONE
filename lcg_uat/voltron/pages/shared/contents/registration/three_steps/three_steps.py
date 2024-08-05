from voltron.pages.shared.contents.registration.forms.base_form import RegistrationHeader
from voltron.pages.shared.contents.registration.forms.base_form import RegistrationSteps
from voltron.pages.shared.contents.registration.forms.step1of3 import Step1Of3Form
from voltron.pages.shared.contents.registration.forms.step2of3 import Step2Of3Form
from voltron.pages.shared.contents.registration.forms.step3of3 import Step3Of3Form
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from voltron.pages.shared import get_driver


class ThreeSteps(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/en/mobileportal/register?(.+)'
    _url_matcher_timeout = 10
    _registration_header = 'xpath=.//vn-header-bar'
    _registration_header_type = RegistrationHeader
    _registration_steps = 'xpath=.//*[contains(@class, "pills-position")]'

    _step1_form = 'xpath=.//*[contains(@class, "ui-tab") and contains(@class, "current")]'
    _step1_form_type = Step1Of3Form
    _step2_form = _step1_form
    _step2_form_type = Step2Of3Form
    _step3_form = _step1_form
    _step3_form_type = Step3Of3Form
    _local_spinner = 'xpath=.//vn-loading-indicator'
    _error_message = 'xpath=.//vn-message-panel'

    @property
    def header(self):
        return self._registration_header_type(selector=self._registration_header, context=self._we)

    @property
    def registration_steps(self):
        return RegistrationSteps(selector=self._registration_steps, context=self._we, timeout=1)

    def get_registration_step(self):
        registration_steps = {'REGISTER':'1', 'VERIFY':'2', 'CONFIRM':'3'}
        wait_for_haul(2)
        registration_step = next((step_name for step_name, step in self.registration_steps.items_as_ordered_dict.items() if step.is_selected()), '')
        return registration_steps[registration_step]

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        wait_for_result(lambda: self._find_element_by_selector(selector=self._registration_header, timeout=0),
                        name=f'{self.__class__.__name__} is active')

    def submit_step1(self, timeout=20):
        self.form_step1.submit_form()
        wait_for_result(lambda: self.get_registration_step() == '2', name='Registration Step is "2"', timeout=timeout)

    def submit_step2(self, timeout=10):
        self.form_step2.submit_form()
        wait_for_result(lambda: self.get_registration_step() == '3', name='Registration Step is "3"', timeout=timeout)

    def submit_step3(self):
        self.form_step3.submit_form()

    @property
    def error_message(self):
        return self._get_webelement_text(selector=self._error_message)

    def wait_for_error_message(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self.error_message,
                               name='Error message to be shown',
                               expected_result=expected_result,
                               timeout=timeout)

    def complete_all_registration_steps(
            self,
            username=None,
            password=None,
            **kwargs):

        currency = kwargs.get('currency', 'GBP')
        email = kwargs.get('email')
        social_title = kwargs.get('social_title', 'Mr.')
        first_name = kwargs.get('first_name', 'Automated')
        last_name = kwargs.get('last_name', 'Tester')
        country = kwargs.get('country', 'United Kingdom')
        birth_date = kwargs.get('birth_date', '01-Jun-1977')

        self.form_step1.country.dropdown.value = country

        self.form_step1.currency.dropdown.value = currency

        self.form_step1.email.input.value = email

        self.form_step1.password.input.value = password

        if self.form_step1.has_username():
            self.form_step1.username.input.value = username
            self._logger.info(f'*** Registering {currency} user "{username}" with password "{password}"')
        else:
            self._logger.info(f'*** Registering {currency} user email "{email}" with password "{password}"')
        self.submit_step1()

        self.form_step2.enter_values(social_title=social_title,
                                     first_name=first_name,
                                     last_name=last_name,
                                     birth_date=birth_date)

        self.submit_step2()

        self.form_step3.enter_values(
            **kwargs)
        ActionChains(get_driver()).send_keys(Keys.TAB).perform()

        self.submit_step3()

    @property
    def form_step1(self):
        step = self.get_registration_step()
        if step == '1':
            return self._step1_form_type(selector=self._step1_form, context=self._we)
        raise VoltronException('Unknown registration form step in header, expected 1, actual %s' % step)

    @property
    def form_step2(self):
        step = self.get_registration_step()
        if step == '2':
            return self._step2_form_type(selector=self._step2_form, context=self._we)
        raise VoltronException('Unknown registration form step in header, expected 2, actual %s' % step)

    @property
    def form_step3(self):
        step = self.get_registration_step()
        if step == '3':
            return self._step3_form_type(selector=self._step3_form, context=self._we)
        raise VoltronException('Unknown registration form step in header, expected 3, actual %s' % step)
