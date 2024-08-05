from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.js_functions import set_date_picker


class DatePickerItem(ComponentBase):
    _date_picker = 'xpath=.//*[@data-crlat="datePickerValue"]'
    _date_picker_text = 'xpath=.//*[@data-crlat="datePickerText"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._date_picker_text)

    @property
    def value(self):
        return self._find_element_by_selector(selector=self._date_picker).get_attribute('value')

    @property
    def date_picker_value(self):
        return self.value

    @date_picker_value.setter
    def date_picker_value(self, value):
        # we = self._find_element_by_selector(selector=self._date_picker_text, context=self._we)
        we = self._find_element_by_selector(selector='xpath=.//input')
        self.scroll_to_we(we)
        set_date_picker(we, value)


class DatePicker(DatePickerItem):
    _date_from = 'xpath=.//*[@dateType="startDate"]'
    _date_to = 'xpath=.//*[@dateType="endDate"]'

    @property
    def date_from(self):
        return DatePickerItem(selector=self._date_from, context=self._we)

    @property
    def date_to(self):
        return DatePickerItem(selector=self._date_to, context=self._we)
