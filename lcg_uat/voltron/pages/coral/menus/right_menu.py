import re
from selenium.common.exceptions import WebDriverException
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import ComponentContent
from voltron.pages.shared.menus.right_menu import RightMenu
from voltron.pages.shared.menus.right_menu import RightMenuItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_to_center_of_element, mouse_event_click
from voltron.utils.waiters import wait_for_result


class CoralRightMenuIconBase(ComponentBase):
    pass


class MyBalanceMenu(ComponentBase):
    _item = 'xpath=.//vn-am-balance-item/div'


class CoralRightMenuItem(RightMenuItem):
    # _name = 'xpath=.//*[contains(@class, "list-nav-txt")]'  # Old xpath not working
    _name = 'xpath=.//*[contains(@class, "menu-item-txt")]'
    _icon = 'xpath=.//i[contains(@class, "ui-icon")]'
    _free_bet_icon = 'xpath=.//span[contains(@class, "badge-offset") and .//text() = "FB"]'
    _icon_type = CoralRightMenuIconBase
    _right_arrow_icon = 'xpath=.//span[contains(@class, "theme-right")]'
    _badge = 'xpath=.//*[span[@vnmenuitembadge]]'
    _my_balance = 'xpath=.//*[contains(@class, "ng-star-inserted")]'
    _my_balance_type = MyBalanceMenu

    @property
    def right_arrow_icon(self):
        return CoralRightMenuIconBase(selector=self._right_arrow_icon, timeout=1, context=self._we)

    def has_arrow_icon(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._right_arrow_icon, timeout=0),
                               name='Right arrow icon shown status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    def has_free_bet_icon(self, expected_result=True, timeout=5) -> bool:
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._free_bet_icon, timeout=0) is not None,
                               name='Free bet icon shown status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    def click(self):
        scroll_to_center_of_element(self._we)
        try:
            mouse_event_click(self._we)
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    @property
    def badge_text(self):
        return self._wait_for_not_empty_web_element_text(selector=self._badge, context=self._we, timeout=3)


class CoralRightMenuHeader(ComponentBase):
    _back_button = 'xpath=.//*[contains(@class, "ui-back")]'
    _title = 'xpath=.//*[contains(@class, "header-ctrl-txt")]'
    _close_button = 'xpath=.//*[contains(@class, "header-ctrl-r")]/span | .//*[contains(@class, "close")]/span'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we, timeout=1)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=1)

    def has_back_button(self, expected_result=True, poll_interval=0.5, timeout=5) -> bool:
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._back_button, timeout=0) is not None,
                               name=f'{self.__class__.__name__} – Back Button shown status to be {expected_result}',
                               expected_result=expected_result,
                               poll_interval=poll_interval,
                               timeout=timeout)


class CoralRightMenu(RightMenu, ComponentContent):
    # todo:     VOL-5538  CoralRightMenu should be moved to shared and renamed
    # _url_pattern = r'^http[s]?:\/\/.+\/en/menu?'
    _item = 'xpath=.//vn-am-icon-menu//a | .//vn-am-menu-item//a'
    _list_item_type = CoralRightMenuItem
    _header = 'xpath=.//vn-header-bar | .//vn-am-header'
    _deposit_button = 'xpath=//*[@section="Menu"]//span[contains(text(), "Deposit")]'
    _log_out = 'xpath=.//vn-am-logout//a'
    _my_balance = 'xpath=.//vn-am-list-layout'
    _my_balance_footer = 'xpath=.//vn-am-bonus-balance'
    _balance_amount = 'xpath=.//*[@class="balance-amount"]'

    @property
    def my_balance(self):
        return CoralMyBalanceDesktop(selector=self._my_balance, context=self._we)

    @property
    def my_balance_footer_items(self):
        return self._find_element_by_selector(selector=self._my_balance_footer)

    @property
    def header(self):
        return CoralRightMenuHeader(selector=self._header, timeout=2)

    @property
    def close_icon(self):
        return self.header.close_button

    @property
    def deposit_button(self):
        return self._find_element_by_selector(selector=self._deposit_button, context=self._we)

    def has_deposit_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._deposit_button, timeout=0.5) is not None,
            name=f'{self.__class__.__name__} - Deposit Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def show_balance(self):
        raise NotImplementedError(f'Show Balance is not present on {self.__class__.__name__}')

    @property
    def hide_balance(self):
        raise NotImplementedError(f'Hide Balance is not present on {self.__class__.__name__}')

    @property
    def balance(self):
        raise NotImplementedError(f'Balance is not present on {self.__class__.__name__}')

    @property
    def vip_summary(self):
        raise NotImplementedError(f'Vip Summary is not present on {self.__class__.__name__}')  # yet?

    def has_vip_summary(self, expected_result=True, timeout=0):
        raise NotImplementedError(f'Vip Summary is not present on {self.__class__.__name__}')  # yet?

    @property
    def odds_boost_amount(self):
        raise NotImplementedError(f'Odds Boost Amount is not present on {self.__class__.__name__}')

    @property
    def balance_amount(self):
        return self._get_webelement_text(selector=self._balance_amount)


class CoralMyBalance(CoralRightMenu):
    _item = 'xpath=.//div[contains(@class, "list-nav-link")]'
    _amount = 'xpath=.//*[contains(@class, "font-weight-bold ml-auto balance-amount")]'
    _list_item_type = CoralRightMenuItem
    _deposit_button = 'xpath=.//a[contains(@class,"btn-primary")]'
    _available_to_use = 'xpath=.//vn-am-bonus-balance'

    @property
    def deposit_button(self):
        return ButtonBase(selector=self._deposit_button, context=self._we)

    @property
    def amount(self):
        return self.parsed_amount[1]

    @property
    def parsed_amount(self):
        matched = re.match(r'^(£|\$|€|Kr|US\$)([0-9.,]+)$', self.amount_str, re.U)
        if matched is not None and matched.group(2) is not None:
            currency_symbol = matched.group(1)
            amount = float(matched.group(2))
            return currency_symbol, amount
        else:
            raise VoltronException(f'Failed parsing amount string: "{self.amount_str}"')

    def has_amount(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._amount_we is not None and self._amount_we.is_displayed(),
            name=f'Amount status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def amount_str(self):
        self.has_amount(timeout=20)
        return self._amount_we.get_attribute('innerHTML')

    @property
    def _amount_we(self):
        amount_we = self._find_element_by_selector(selector=self._amount, timeout=2)
        if not amount_we:
            raise VoltronException('Cannot get Amount value')
        return amount_we

    def is_amount_truncated(self):
        return self.is_truncated(selector=self._amount)

    @property
    def currency_symbol(self):
        return self.parsed_amount[0]

    @property
    def available_to_use(self):
        return ComponentBase(selector=self._available_to_use, context=self._we)


class CoralMyBalanceDesktop(CoralMyBalance):
    _url_pattern = r'^http[s]?:\/\/.+\/?'
