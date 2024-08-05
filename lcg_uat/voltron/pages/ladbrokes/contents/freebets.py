from datetime import datetime
from voltron.pages.shared.contents.freebets import Balance
from voltron.pages.shared.contents.freebets import Freebets
from voltron.pages.shared.contents.freebets import FreebetsItem
from voltron.pages.shared.contents.freebets import FreebetsSection


class LadbrokesBalance(Balance):
    _no_freebets = 'xpath=.//*[@data-crlat="noEventsFound"]'

    @property
    def no_freebets_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._no_freebets)


class LadbrokesFreebetsItem(FreebetsItem):
    _freebet_title = 'xpath=.//*[@data-crlat="fbDesc"]'
    _freebet_value = 'xpath=.//*[@data-crlat="fbValue"]'

    @property
    def freebet_title(self):
        self.scroll_to_we()
        return self._get_webelement_text(selector=self._freebet_value, timeout=0)

    @property
    def freebet_text(self):
        return self._get_webelement_text(selector=self._freebet_value, timeout=0)

    @property
    def freebet_value(self):
        self.scroll_to_we()
        value = self._find_element_by_selector(selector=self._freebet_value, timeout=1)
        if value:
            return float(self.strip_currency_sign(value.text.replace(' FREE BET', '')))

    @property
    def used_by(self):
        self.scroll_to_we()
        date = self._find_element_by_selector(selector=self._used_by, timeout=1)
        if date:
            return datetime.strptime(date.text, '%d/%m/%Y %H:%M:%S')
        return ''


class LadbrokesFreebetsSection(FreebetsSection):
    _item = 'xpath=.//*[@data-crlat="fbItem"]'
    _list_item_type = LadbrokesFreebetsItem


class LadbrokesFreebets(Freebets):

    @property
    def balance(self):
        return LadbrokesBalance(selector=self._balance, context=self._we, timeout=1)

    @property
    def freebets_content(self):
        return LadbrokesFreebetsSection(selector=self._my_freebets, context=self._we)
