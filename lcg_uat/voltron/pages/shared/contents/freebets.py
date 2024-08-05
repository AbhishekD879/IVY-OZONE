from collections import OrderedDict
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class Balance(ComponentBase):
    _cash_balance = 'xpath=.//*[@data-crlat="cashBalance"]'
    _total_balance = 'xpath=.//*[@data-crlat="totalBalance"]'

    @property
    def cash_balance(self):
        balance = self._find_element_by_selector(selector=self._cash_balance, timeout=0)
        if balance:
            return float(self.strip_currency_sign(balance.text).replace(',', ''))

    @property
    def total_balance(self):
        balance = self._find_element_by_selector(selector=self._total_balance, timeout=0)
        if balance:
            return float(self.strip_currency_sign(balance.text).replace(',', ''))


class FreebetsHeader(ComponentBase):
    _total_freebet_balance = 'xpath=.//*[@data-crlat="fbValue"]'
    _header_title = 'xpath=.//*[@data-crlat="fbValue"]'
    _fb_icon = 'xpath=.//*[@data-crlat="fbIcon"]'

    def has_fb_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._fb_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Expires status to be {expected_result}')

    @property
    def total_balance(self):
        balance = self._find_element_by_selector(selector=self._total_freebet_balance, timeout=0)
        if balance:
            return float(self.strip_currency_sign(balance.text.replace(' FREE BET', '')))

    @property
    def total_balance_with_currency(self):
        balance = self._get_webelement_text(selector=self._total_freebet_balance, timeout=0)
        if balance:
            return balance.replace(' FREE BET', '')
    @property
    def header_title(self):
        header = self._get_webelement_text(selector=self._header_title, timeout=0)
        header_name=header.split()
        return f'{header_name[-2]} {header_name[-1]}'

class FreebetsItem(ComponentBase):
    _freebet_title = 'xpath=.//*[@data-crlat="freebetName"]'
    _used_by = 'xpath=.//*[@data-crlat="usedBy"]'
    _expires = 'xpath=.//*[@data-crlat="expires"]'
    _freebet_value = 'xpath=.//*[@data-crlat="amount"]'

    @property
    def freebet_title(self):
        self.scroll_to_we()
        return self._get_webelement_text(selector=self._freebet_title, timeout=0)

    @property
    def name(self):
        return self.freebet_title

    def has_expires(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._expires,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Expires status to be {expected_result}')

    @property
    def expires(self):
        expire_date = self._find_element_by_selector(selector=self._expires, timeout=2)
        if expire_date:
            return expire_date.text
        return ''

    @property
    def used_by(self):
        self.scroll_to_we()
        date = self._find_element_by_selector(selector=self._used_by, timeout=1)
        if date:
            return datetime.strptime(date.text, '%d/%m/%Y %H:%M:%S')
        return ''

    @property
    def freebet_value(self):
        self.scroll_to_we()
        value = self._find_element_by_selector(selector=self._freebet_value, timeout=1)
        if value:
            return float(self.strip_currency_sign(value.text).replace(' Free Bet', ''))


class FreebetsSection(ComponentBase):
    _freebets_header = 'xpath=.//*[@data-crlat="fbItem"]/free-bet-label'
    _item = 'xpath=.//*[@data-crlat="fbItem"]'
    _title = 'xpath=.//*[@data-crlat="fbGroupTitle"]'
    _list_item_type = FreebetsItem
    _no_freebets = 'xpath=.//*[@data-crlat="noFreebets"]'
    _go_betting = 'xpath=.//*[@data-crlat="fbLink"]'

    @property
    def go_betting(self):
        return ButtonBase(selector=self._go_betting, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)} {list_item.name}': list_item})
        return items_ordered_dict

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def section_header(self):
        return FreebetsHeader(selector=self._freebets_header, context=self._we)

    @property
    def no_freebets_message(self):
        message = self._find_element_by_selector(selector=self._no_freebets, timeout=3)
        if message:
            wait_for_result(lambda: message.is_displayed() and message.text != '',
                            name='"No Freebets Message" is displayed',
                            timeout=1)
            return self._get_webelement_text(we=message, timeout=1)
        else:
            raise VoltronException('"No Freebets Message" is not shown')


class Freebets(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/freebets'
    _balance = 'xpath=.//*[@data-crlat="freebetBalance"]'
    _item = 'xpath=.//*[contains(@class,"free-bet-group__container")]'
    _list_item_type = FreebetsSection
    _free_bets_available = 'xpath=.//*[@class="free-bet-available"]'
    _my_freebets = 'xpath=.//*[contains(@data-crlat, "myFreebets")] | //free-bet-empty'
    _freebet_details = 'xpath=.//*[@data-crlat="freebetDetails"]'

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._my_freebets, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def balance(self):
        return Balance(selector=self._balance, context=self._we, timeout=1)

    @property
    def freebets_content(self):
        return FreebetsSection(selector=self._my_freebets, context=self._we)

    @property
    def available_free_bets_count(self):
        return self._get_webelement_text(selector=self._free_bets_available, timeout=1).split()[-1].strip('()')