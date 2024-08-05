import re
from datetime import datetime

from voltron.pages.ladbrokes.components.primitives.button_array import ButtonsArrayBaseLadbrokes
from voltron.pages.ladbrokes.contents.registration.three_steps.forms.base_form import StepFormBase
from voltron.pages.shared import get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.inputs import RegistrationInput
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class BirthDate(ComponentBase):
    _day = 'xpath=.//*[@id="day"]'
    _month = 'xpath=.//*[@id="month"]'
    _year = 'xpath=.//*[@id="year"]'
    _error = 'xpath=(//*[@class="error-tooltip"])[3]'

    @property
    def error(self):
        return self._get_webelement_text(selector=self._error, timeout=2, context=self._we)

    def set_value(self, data):
        self.value = data

    @property
    def value(self):
        return '%s-%s-%s' % (self.day, self.month, self.year)

    @value.setter
    def value(self, value):
        match = re.match(r'^([0-9a-zA-Z]+).([0-9a-zA-Z]+).([0-9a-zA-Z]+)', value)
        if match:
            (self.year, self.month, self.day) = (match.group(3), match.group(2), match.group(1))
        else:
            raise VoltronException('Unexpected birth date value "%s" use "DD.MM.YYYY format" ' % value)

    @property
    def day_drop_down(self):
        return SelectBase(selector=self._day, context=self._we)

    @property
    def day(self):
        return self.day_drop_down.value

    @day.setter
    def day(self, value):
        datetime_value = datetime.strptime(value, '%d')
        value = datetime.strftime(datetime_value, '%#d')
        self.day_drop_down.value = value

    @property
    def month_drop_down(self):
        return SelectBase(selector=self._month, context=self._we)

    @property
    def month(self):
        return self.month_drop_down.value

    @month.setter
    def month(self, value):
        datetime_value = datetime.strptime(value, '%b')
        value = datetime.strftime(datetime_value, '%B')
        self.month_drop_down.value = value

    @property
    def year_drop_down(self):
        return SelectBase(selector=self._year, context=self._we)

    @property
    def year(self):
        return self.year_drop_down.value

    @year.setter
    def year(self, value):
        self.year_drop_down.value = value


class Step1of3Form(StepFormBase):
    _title_buttons = 'xpath=.//*[@class="title-buttons"]'
    _first_name = 'xpath=.//*[@data-field-name="FirstName"]/div/input'
    _last_name = 'xpath=.//*[@data-field-name="LastName"]/div/input'
    _birth_date = 'xpath=.//*[@data-field-name="BirthDate"]'
    _ios_birth_date = 'xpath=.//*[@data-field-name="BirthDate"]/div/input'
    _email = 'xpath=.//*[@data-field-name="RegisterEmail"]/div/input'

    @property
    def social_title(self):
        return ButtonsArrayBaseLadbrokes(selector=self._title_buttons, context=self._we)

    @social_title.setter
    def social_title(self, value):
        ButtonsArrayBaseLadbrokes(selector=self._title_buttons, context=self._we).value = value

    @property
    def first_name(self):
        return RegistrationInput(selector=self._first_name, context=self._we)

    @first_name.setter
    def first_name(self, value):
        RegistrationInput(selector=self._first_name, context=self._we).value = value

    @property
    def last_name(self):
        return RegistrationInput(selector=self._last_name, context=self._we)

    @last_name.setter
    def last_name(self, value):
        RegistrationInput(selector=self._last_name, context=self._we).value = value

    @property
    def birth_date(self):
        if 'IOS' in get_device_properties()['os'].upper():
            return RegistrationInput(selector=self._ios_birth_date, context=self._we, timeout=1)
        else:
            return BirthDate(selector=self._birth_date, context=self._we, timeout=1)

    @birth_date.setter
    def birth_date(self, value):
        if 'IOS' in get_device_properties()['os'].upper():
            RegistrationInput(selector=self._ios_birth_date, context=self._we, timeout=1).value = value
        else:
            BirthDate(selector=self._birth_date, context=self._we, timeout=1).value = value

    @property
    def email(self):
        return RegistrationInput(selector=self._email, context=self._we)

    @email.setter
    def email(self, value):
        RegistrationInput(selector=self._email, context=self._we).value = value

    def enter_values(self,
                     social_title='Mr',
                     first_name='Automated',
                     last_name='Tester',
                     birth_date='10-Jul-1976',
                     email='test@playtech.com'):
        if 'IOS' in get_device_properties()['os'].upper():
            birth_date = datetime.strftime(datetime.strptime(birth_date, '%d-%b-%Y'), '%d/%m/%Y')
        self.social_title.value = social_title
        self.first_name.value = first_name
        self.last_name.value = last_name
        self.birth_date.value = birth_date
        self.email.value = email


class RegistrationInputLadbrokes(RegistrationInput):
    _error = 'xpath=.//*[@class="error-tooltip"]'

    @property
    def error(self):
        we = self._find_element_by_selector(selector=self._error, context=self._we)
        error_text = self._get_webelement_text(we=we) if we else ''
        return error_text
