from collections import OrderedDict
from selenium.common.exceptions import WebDriverException
from voltron.pages.shared import get_driver, get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase, ButtonNoScrollBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_into_view_above
from voltron.utils.waiters import wait_for_result


class PaymentOption(ButtonBase):

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(we=self._we, timeout=1)


class SelectMenu(ComponentBase):
    _item = 'xpath=.//md-option[@class="md-ink-ripple"]'
    _list_item_type = PaymentOption

    def is_payment_option_present(self, option_name, expected_result=True, timeout=3) -> bool:
        return wait_for_result(lambda: self.items_as_ordered_dict.get(option_name) is not None,
                               expected_result=expected_result,
                               poll_interval=0.5,
                               timeout=timeout,
                               name=f'{option_name} payment method presence status to be "{expected_result}"')

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._context)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        self._logger.debug(
            f'*** Found payment account items "{items_ordered_dict.keys()}"')
        return items_ordered_dict


class PaymentAccounts(ComponentBase):
    _select_button = 'xpath=.//span[@class="md-select-icon"]'
    _select_menu = 'xpath=.//*[contains(@class, "md-select-menu-container md-active md-clickable")]'

    @property
    def select_button(self):
        return ButtonNoScrollBase(selector=self._select_button, context=self._we, timeout=2)

    def has_select_menu(self, expected_result=True, timeout=1) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._select_menu, timeout=0, context=get_driver()) is not None and
            self._find_element_by_selector(selector=self._select_menu, timeout=0, context=get_driver()).is_displayed(),
            expected_result=expected_result,
            timeout=timeout,
            name=f'Select menu displayed status to be "{expected_result}"')

    @property
    def select_menu(self):
        return SelectMenu(selector=self._select_menu, context=get_driver(), timeout=2)

    @property
    def existing_account_name(self):
        return self._get_webelement_text(we=self._we)

    def selected_account(self):
        return self._get_webelement_text(we=self._we)

    def click(self):
        device = get_device_properties()
        if device['type'] == 'desktop':
            scroll_into_view_above(self._we)
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')
