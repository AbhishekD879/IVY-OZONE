import re
from collections import OrderedDict
from voltron.pages.shared.contents.registration.forms.base_form import StepFormBase
from voltron.pages.shared.contents.registration.primitives.input import RegistrationInput
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class RegistrationSocialTitleItem(ComponentBase):
    _name = 'xpath=.//label[@data-wa="gender"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class RegistrationSocialTitle(ComponentBase):
    _item = 'xpath=.//*[contains(@class, "form-control-tabs-item")] | .//*[contains(@class, "form-control-tabs")]//child::label'
    _list_item_type = RegistrationSocialTitleItem

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({item_we.text: list_item})
        return items_ordered_dict

    @property
    def value(self):
        raise VoltronException('Cannot detect selected Social Title')

    @value.setter
    def value(self, value):
        items = self.items_as_ordered_dict
        status = items.get(value)
        if not status:
            raise VoltronException(f'"{value}" not found in {list(items.keys())}')
        status.click()


class DateOfBirth(ComponentBase):
    _day = 'xpath=.//lh-form-field[./*[@id="day"]]'
    _day_type = RegistrationInput
    _month = 'xpath=.//lh-form-field[./*[@id="month"]]'
    _month_type = RegistrationInput
    _year = 'xpath=.//lh-form-field[./*[@id="year"]]'
    _year_type = RegistrationInput

    @property
    def day(self):
        return self._day_type(selector=self._day, context=self._we)

    @property
    def month(self):
        return self._month_type(selector=self._month, context=self._we)

    @property
    def year(self):
        return self._year_type(selector=self._year, context=self._we)

    @property
    def value(self):
        return f'{self.day.input.value}-{self.month.input.value}-{self.year.input.value}'

    @value.setter
    def value(self, value):
        match = re.match(r'^([0-9a-zA-Z]+).([0-9a-zA-Z]+).([0-9a-zA-Z]+)', value)
        if match:
            day = match.group(1)
            day = day[-1] if day.startswith('0') else day
            month = match.group(2)
            year = match.group(3)
            (self.year.input.value, self.month.input.value, self.day.input.value) = (year, month, day)
        else:
            raise VoltronException(f'Unexpected birth date value "{value}" use "DD.MM.YYYY format" ')


class Step2Of3Form(StepFormBase):
    _social_title = 'xpath=.//pt-reg-gender'
    _social_title_type = RegistrationSocialTitle
    _first_name = 'xpath=.//pt-reg-first-name'
    _first_name_type = RegistrationInput
    _last_name = 'xpath=.//pt-reg-last-name'
    _last_name_type = RegistrationInput
    _date_of_birth = 'xpath=.//pt-reg-date-of-birth-split'
    _date_of_birth_type = DateOfBirth

    @property
    def social_title(self):
        return self._social_title_type(selector=self._social_title, context=self._we)

    @property
    def first_name(self):
        return self._first_name_type(selector=self._first_name, context=self._we)

    @property
    def last_name(self):
        return self._last_name_type(selector=self._last_name, context=self._we)

    @property
    def date_of_birth(self):
        return self._date_of_birth_type(selector=self._date_of_birth, context=self._we)

    def enter_values(self,
                     social_title=None,
                     first_name=None,
                     last_name=None,
                     birth_date=None):
        self.social_title.value = social_title
        self.first_name.input.value = first_name
        self.last_name.input.value = last_name
        self.date_of_birth.value = birth_date
