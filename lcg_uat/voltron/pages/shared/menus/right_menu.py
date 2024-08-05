import re
from collections import OrderedDict
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import voltron.environments.constants as vec
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import parse_selector
from voltron.utils.js_functions import click
from voltron.utils.js_functions import mouse_event_click
from voltron.utils.waiters import wait_for_result


class Badge(ComponentBase):
    _level_name = 'xpath=.//*[@data-crlat="vipLevelName"]'
    _more_info_link = 'xpath=.//*[@data-crlat="moreInfo"]'

    @property
    def background_color_value(self):
        attr = self._we.get_attribute('class')
        find = re.search('(bronze|silver|gold|platinum)', attr)
        return find.group(1) if find else None

    @property
    def level_name(self):
        return self._get_webelement_text(selector=self._level_name, timeout=2)

    @property
    def more_info_link(self):
        return ButtonBase(selector=self._more_info_link, context=self._we)


class VIPSummary(ComponentBase):
    _balance = 'xpath=.//*[contains(@data-crlat, "userBalance")]'
    _show_hide_balance = 'xpath=.//*[@data-crlat="showHideBalance"]'
    _first_name = 'xpath=.//*[@data-crlat="vipHeaderFirstName"]'
    _last_name = 'xpath=.//*[@data-crlat="vipHeaderLastName"]'
    _badge = 'xpath=.//*[@data-crlat="vipLevelBadge"]'

    @property
    def badge(self):
        return Badge(selector=self._badge)

    @property
    def balance(self):
        return self._get_webelement_text(selector=self._balance, timeout=2)

    @property
    def balance_toggle(self):
        return ButtonBase(selector=self._show_hide_balance)

    def is_balance_shown(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._balance, timeout=0) is not None,
            name='Balance to show',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def first_name(self):
        return self._get_webelement_text(selector=self._first_name, timeout=2)

    @property
    def last_name(self):
        return self._get_webelement_text(selector=self._last_name, timeout=2)


class RightMenuIconBase(IconBase):
    _inner_svg = 'xpath=.//*[local-name()="use" and contains(@*, "#")]'

    def is_displayed(self, expected_result=True, timeout=1, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._inner_svg, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout,
            poll_interval=poll_interval,
            bypass_exceptions=bypass_exceptions)


class RightMenuItemLink(LinkBase):

    def click(self):
        if self.is_safari:
            mouse_event_click(self._we)
        else:
            click(self._we)


class RightMenuItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="title"]'
    _icon = 'xpath=.//*[@data-crlat="icon"]'
    _icon_type = RightMenuIconBase
    _link = 'xpath=.//*[@data-crlat="link"] | .//a[@class="menu-item-link list-nav-link"]'
    _link_type = RightMenuItemLink

    @property
    def link(self):
        return self._link_type(selector=self._link, context=self._we, timeout=3)

    @property
    def name(self):
        text = self._get_webelement_text(selector=self._name)
        if vec.odds_boost.PAGE.title.lower() in text.lower():
            return text.split('\n')[0].strip()
        return text

    @property
    def icon(self):
        return self._icon_type(selector=self._icon, timeout=1, context=self._we)

    def has_icon(self, timeout=1, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._icon, timeout=0) is not None,
            name=f'{self.__class__.__name__} – Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    def click(self):
        self.link.click()


class RightMenu(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="menu.listItem"]'
    _list_item_type = RightMenuItem
    _section_item = 'xpath=.//vn-am-icon-menu//vn-am-items-layout'
    _log_out = 'xpath=.//*[@data-crlat="menu.listItem"]/*[@data-crlat="link"][.//*[contains(text(),"Logout")]]'
    _close_icon = 'xpath=.//*[@data-crlat="sidebarClose"]'
    _hide_balance = 'xpath=.//*[@data-crlat="hideBalance"]'
    _show_balance = 'xpath=.//*[@data-crlat="showBalance"]'
    _balance = 'xpath=.//*[@data-crlat="balanceAmount"]'
    _vip_summary = 'xpath=.//*[@data-crlat="isVip"]'
    _odds_boost_amount = 'xpath=.//*[@data-crlat="oddsBoostCounter"]'
    _context_timeout = 5

    def scroll_menu_to_bottom(self):
        we = self._find_element_by_selector(self._item, context=self._we)
        actions = ActionChains(get_driver())
        actions.move_to_element(we)
        actions.click_and_hold(we)
        actions.send_keys(Keys.END)
        actions.perform()

    def _wait_active(self, timeout=15):
        self._we = self._find_myself(timeout=timeout)
        wait_for_result(lambda: self._we.size.get('height') > 200 and self._we.size.get('width') > 100,
                        timeout=timeout,
                        name='Right menu to appear in expanded size')
        wait_for_result(lambda: len(self._find_elements_by_selector(selector=self._item, timeout=0)) > 1,
                        name='Right Menu to open',
                        timeout=timeout)

    @property
    def log_out_button(self):
        return RightMenuItemLink(selector=self._log_out, timeout=1, context=self._we)

    @property
    def close_icon(self):
        return ButtonBase(selector=self._close_icon, context=self._we)

    def logout(self):
        log_out_button = self.log_out_button
        log_out_button.scroll_to()
        log_out_button.click()

    @property
    def show_balance(self):
        return ButtonBase(selector=self._show_balance)

    @property
    def hide_balance(self):
        return ButtonBase(selector=self._hide_balance)

    @property
    def balance(self):
        return self._get_webelement_text(selector=self._balance)

    @property
    def vip_summary(self):
        return VIPSummary(selector=self._vip_summary, context=self._we)

    def has_vip_summary(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._vip_summary, timeout=0),
                               name=f'{self.__class__.__name__} – VIP Summary displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def odds_boost_amount(self):
        try:
            amount = self._get_webelement_text(selector=self._odds_boost_amount, timeout=0.5)
        except VoltronException:
            amount = '0'
        if not amount:
            amount = '0'
        return amount

    @property
    def section_wise_items(self):
        items_we = self._find_elements_by_selector(selector=self._section_item,
                                                   context=self._we,
                                                   timeout=self._timeout)[:-1]
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            _item_name_selector = 'xpath=.//div[contains(@class,"am-items-header")]'
            (by, val) = parse_selector(_item_name_selector)
            item_name = item_we.find_element(by=by, value=val).text
            (by, val) = parse_selector(self._item)
            child_items = item_we.find_elements(by=by, value=val)
            list_item = {
                self._list_item_type(web_element=item_we).name.upper().replace(" ", ""): self._list_item_type(web_element=item_we) for
                item_we in child_items}
            items_ordered_dict.update({item_name.upper().replace(" ", ""): list_item})
        return items_ordered_dict
