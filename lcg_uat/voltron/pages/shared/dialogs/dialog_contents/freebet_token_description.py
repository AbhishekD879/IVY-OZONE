from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase

from voltron.pages.shared.dialogs.dialog_base import Dialog


class FreebetDialogTableRow(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="freebetOfferName"]'
    _expiry_date = 'xpath=.//*[@data-crlat="freebetTokenExpiryDate"]'
    _value = 'xpath=.//*[@data-crlat="freebetTokenValue"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def expiry_date(self):
        return self._get_webelement_text(selector=self._expiry_date, context=self._we)

    @property
    def value(self):
        return self._get_webelement_text(selector=self._value, context=self._we)


class FreebetTokenDescription(Dialog):
    _default_action = 'click_ok'
    _ok_button = 'xpath=.//*[@data-uat="popUpButton"]'
    _freebet_sum = 'xpath=.//*[@data-crlat="freeBetsSum"]'
    _item = 'xpath=.//*[@data-crlat="freebetsDialogItem"]'
    _list_item_type = FreebetDialogTableRow

    @property
    def items_as_ordered_dict(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            name = f'{items_we.index(item_we)} {list_item.name}'
            items_ordered_dict.update({name: list_item})
        return items_ordered_dict

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button)

    def click_ok(self):
        ok_button = self.ok_button
        ok_button.scroll_to_we()
        ok_button.click()

    @property
    def freebet_sum(self):
        return self.strip_currency_sign(self._get_webelement_text(selector=self._freebet_sum, context=self._we))
