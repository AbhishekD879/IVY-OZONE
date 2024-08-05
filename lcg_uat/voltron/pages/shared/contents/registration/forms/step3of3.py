import random

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.registration.forms.base_form import StepFormBase
from voltron.pages.shared.contents.registration.primitives.dropdown import RegistrationDropdown
from voltron.pages.shared.contents.registration.primitives.input import RegistrationInput
from voltron.utils.waiters import wait_for_result


class AddressFinder(RegistrationInput):
    _enter_manually_link = 'xpath=.//div/a[contains(text(), "manually")]'

    def has_enter_manually_link(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._enter_manually_link, timeout=0),
                               name=f'{self.__class__.__name__} - Enter Manually Link displayed status to be {expected_result}',
                               timeout=timeout)

    @property
    def enter_manually_link(self):
        return LinkBase(selector=self._enter_manually_link, context=self._we)


class RegistrationMobileNumber(ComponentBase):
    _mobile_code = 'xpath=.//lh-form-field[.//*[@id="mobilecountrycode"]]'
    _mobile_code_type = RegistrationInput
    _mobile_number = 'xpath=.//lh-form-field[.//*[@id="mobilenumber"]]'
    _mobile_number_type = RegistrationInput

    @property
    def mobile_code(self):
        return self._mobile_code_type(selector=self._mobile_code, context=self._we)

    @property
    def mobile_number(self):
        return self._mobile_number_type(selector=self._mobile_number, context=self._we)

    @property
    def value(self):
        return f'{self.mobile_code.input.selected_item}{self.mobile_number.input.value}'

    @value.setter
    def value(self, value):
        mobile_code = value[:3]
        mobile_number = value[3:]
        self.mobile_code.input.value = mobile_code
        self.mobile_number.input.value = mobile_number


class Step3Of3Form(StepFormBase):
    _address_finder = 'xpath=.//pt-reg-address-finder'
    _address_finder_type = AddressFinder
    _address_one = 'xpath=.//pt-reg-address-line-1'
    _address_one_type = RegistrationInput
    _city = 'xpath=.//pt-reg-address-city'
    _city_type = RegistrationInput
    _province = 'xpath=.//pt-reg-address-state'
    _province_type = RegistrationDropdown
    _post_code = 'xpath=.//pt-reg-address-zip'
    _post_code_type = RegistrationInput
    _mobile = 'xpath=.//pt-reg-mobile-number'
    _mobile_type = RegistrationMobileNumber
    _create_my_account_button = 'xpath=.//button[@id="submit"]'
    _select_all_marketing_options = 'xpath=.//label[@for="selectallpromotionoptions"]'
    data = {
            'HU3 1PF': 'Dudley Avenue, Mayfield Street',
            'HU3 1PA': 'Beta Villas, Mayfield Street',
            'HU3 1ZB': 'Grosvenor Mews, Grosvenor Street',
            'HU10 6AB': 'Haydon Close, Willerby'
           }

    @property
    def address_finder(self):
        return self._address_finder_type(selector=self._address_finder, context=self._we)

    def has_address_finder(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._address_finder, timeout=0),
                               name=f'{self.__class__.__name__} - Address Finder displayed status to be {expected_result}',
                               timeout=timeout)

    @property
    def address_one(self):
        return self._address_one_type(selector=self._address_one, context=self._we)

    @property
    def city(self):
        return self._city_type(selector=self._city, context=self._we)

    @property
    def province(self):
        return self._province_type(selector=self._province, context=self._we)

    def has_province(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._province, timeout=0),
                               name=f'{self.__class__.__name__} - Province Input displayed status to be {expected_result}',
                               timeout=timeout)

    @property
    def post_code(self):
        return self._post_code_type(selector=self._post_code, context=self._we)

    @property
    def mobile(self):
        return self._mobile_type(selector=self._mobile, context=self._we)

    def enter_values(self, **kwargs):
        post_code_uk = kwargs.get('post_code_uk')
        postal_code, street = random.choice(list(self.data.items()))
        if post_code_uk:
            self.address_finder.input.value = post_code_uk
        else:
            if self.has_address_finder(timeout=1):
                self.address_finder.enter_manually_link.click()

            address = f'{random.choice([i for i in range(1, 99) if i not in [13, 24, 26, 28]])} {street}'
            address_one = kwargs.get('address_one', address)
            wait_for_result(lambda: self.address_one.input.value,
                            name='Address line to appear',
                            timeout=5)
            self.address_one.input.value = address_one

            city = kwargs.get('city', 'Wolverhampton')
            self.city.input.value = city
            province = kwargs.get('province')
            if self.has_province(timeout=1):
                if province:
                    self.province.dropdown.value = province
                else:
                    self.province.dropdown.select_randomly()

            post_code = kwargs.get('post_code', postal_code)
            self.post_code.input.value = post_code
        number = f'+447{random.randrange(111111111, 999999999)}'
        mobile = kwargs.get('mobile', number)
        self.mobile.value = mobile

    @property
    def create_my_account_button(self):
        return ButtonBase(selector=self._create_my_account_button, context=self._we)

    def submit_form(self):
        self.create_my_account_button.click()

    @property
    def all_marketing_options_checkbox(self):
        return CheckBoxBase(selector=self._select_all_marketing_options, context=self._we)
