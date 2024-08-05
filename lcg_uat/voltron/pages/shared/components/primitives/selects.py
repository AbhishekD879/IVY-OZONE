import random

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.webdriver.support.select import Select
from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class SelectBase(ComponentBase, Select):
    _dropdown_market_selector = 'xpath=.//*[@data-crlat="open-menu-button"] | .//*[@data-crlat="dropdown.label"]'
    _down_arrow = 'xpath=.//*[@data-crlat="dropdown.arrowDown"] | .//*[@class="select-arrow"]'
    _item = 'xpath=.//*[@data-crlat="dropdown.menuItem"]'

    @property
    def change_market_button(self):
        return self._find_element_by_selector(selector=self._dropdown_market_selector, context=self._we, timeout=2)

    @property
    def has_down_arrow(self):
        return self._find_element_by_selector(selector=self._down_arrow, timeout=20) is not None

    def __init__(self, *args, **kwargs):
        ComponentBase.__init__(self, *args, **kwargs)
        try:
            Select.__init__(self, webelement=self._we)
        except UnexpectedTagNameException:
            pass

    @property
    def dropdown(self):
        return ComponentBase(selector=self._dropdown_market_selector, context=self._we, timeout=2)

    def is_expanded(self, timeout=5, expected_result=True):
        result = wait_for_result(
            lambda: 'expanded' in self.get_attribute('class'),
            timeout=timeout,
            name=f'"{self.__class__.__name__}" to be expanded',
            expected_result=expected_result)
        return result

    def expand(self):
        if self.is_expanded():
            self._logger.warning(f'*** Bypassing accordion expand, since "{self.__class__.__name__}" already expanded')
        else:
            self._logger.debug(f'*** Expanding "{self.__class__.__name__}"')

            self.dropdown.click()
            wait_for_result(lambda: self.is_expanded(timeout=0),
                            name=f'"{self.__class__.__name__}" section to expand',
                            timeout=3)

    @property
    def available_market_template(self):
        self._find_elements_by_selector(selector=self._item, timeout=3)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    def _wait_active(self, timeout=0):
        try:
            self._we = self._find_myself()
            return wait_for_result(lambda: self._we.is_enabled(),
                                   timeout=2,
                                   name='Drop down to be enabled')
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()

    @property
    def selected_item(self):
        items = Select(self._we).options
        for item in items:
            if item.get_attribute('selected') is not None and \
                    any([True for status in ('true', 'selected') if status in item.get_attribute('selected')]):
                return item.text
        else:
            return self.first_selected_option

    @property
    def value(self):
        self.scroll_to_we()
        try:
            return self._select_control.first_selected_option.text
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()
            return self._select_control.first_selected_option.text
        except NoSuchElementException as e:
            if 'No options are selected' in e.msg:
                return None

    @value.setter
    def value(self, value):
        self.scroll_to_we()
        self._logger.debug(f'*** Setting DropDown Value "{value}"')
        try:
            self._logger.debug(
                f'*** User has selected "{value}" on DropDown. Call "{self.__class__.__name__}"'
            )
            self._select_control.select_by_visible_text(value)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()
            self._select_control.select_by_visible_text(value)
        except NoSuchElementException:
            raise VoltronException(f'Value "{value}" not found in {self.available_options}')

    @property
    def default_value(self):
        return self.value

    def select_value_by_index(self, index):
        try:
            self._select_control.select_by_index(index)
        except NoSuchElementException:
            self._logger.warning('*** Item by index "%s" is not found, selecting first item instead' % index)
            self._select_control.select_by_index(0)

    def select_value_by_text(self, text):
        try:
            self._select_control.select_by_visible_text(text)
        except NoSuchElementException:
            self._logger.warning('*** Item with text "%s" is not found, selecting first item instead' % text)
            self._select_control.select_by_index(0)

    def select_value(self, value):
        try:
            self._select_control.select_by_value('string:%s' % value)
        except NoSuchElementException:
            self._logger.warning('*** Item "%s" is not found, selecting first item instead' % value)
            self._select_control.select_by_index(0)

    @property
    def _select_control(self):
        return Select(self._we)

    @property
    def available_options(self):
        options_we = self._select_control.options
        import html
        option_values = [html.unescape(wait_for_result(lambda: option_we.get_attribute('innerHTML'),
                                                    name='Option text is not empty',
                                                    timeout=2))
                         for option_we in options_we]
        return option_values

    def select_randomly(self):
        value = random.choice(self.available_options)
        self.value = value
        return value


class BYBSelectBase(SelectBase):

    @property
    def selected_item(self):
        try:
            return self._select_control.first_selected_option.text
        except NoSuchElementException as e:
            if 'No options are selected' in e.msg:
                return None
        except Exception:
            return self.options[0].text


class RegistrationDropDown(SelectBase):

    def get_label(self):
        return self.default_value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class DesktopCreditCardSelectOptions(ComponentBase):
    _item = 'xpath=.//*[@data-dk-dropdown-value]'
    _list_item_type = TextBase


class DesktopCreditCardIframeSelect(ComponentBase):
    _value = 'xpath=.//*[@class="dk_label"]'
    _options_popup = 'xpath=.//*[@class="dk_options_inner"]'

    @property
    def options_popup(self):
        return DesktopCreditCardSelectOptions(selector=self._options_popup, context=self._we, timeout=3)

    @property
    def value(self):
        return self._get_webelement_text(selector=self._value, context=self._we)

    @value.setter
    def value(self, value):
        if self.value.upper() != value.upper():
            self._logger.debug(
                f'*** User has selected "{value}" on DropDown. Call of "{self.__class__.__name__}"'
            )
            self.click()
            value_option = self.options_popup.items_as_ordered_dict.get(value)
            if value_option:
                value_option.click()
            else:
                raise VoltronException(f'Value "{value}" not found in "{list(self.options_popup.items_as_ordered_dict.keys())}"')
        else:
            self._logger.warning(f'*** Bypassing click on option: "{value}" as it is already selected')

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass
