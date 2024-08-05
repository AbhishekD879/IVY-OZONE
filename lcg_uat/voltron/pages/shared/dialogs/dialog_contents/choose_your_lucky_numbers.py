from collections import OrderedDict
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class LottoChooseLuckyNumbers(Dialog):
    _dialog_popup_title = 'xpath=.//*[@data-crlat="dTitle"]'
    _close_button = 'xpath=.//*[@data-uat="popUpCloseButton"]'
    _done_btn = 'xpath=.//*[@data-crlat="doneButton"]'
    _lucky_dips = 'xpath=.//*[@data-crlat="luckyDipsButton"]' # Lucky buttons appear on the choose numbers page after adding one line. Adding another line to the line summary page triggers their appearance on the choose numbers page.
    _reset_btn = 'xpath=.//*[@data-crlat="resetButton"]'
    _item = 'xpath=.//*[@data-crlat="numbersButton"]'
    _list_item_type = ButtonBase

    @property
    def dialog_popup_title(self):
        return self._get_webelement_text(selector=self._dialog_popup_title)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def number_selectors_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        number_selectors = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            number_selectors.update({f'{list_item.name}': list_item})
        return number_selectors

    @property
    def lucky_buttons_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._lucky_dips, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def done_button(self):
        return ButtonBase(selector=self._done_btn, context=self._we)

    @property
    def reset_button(self):
        return ButtonBase(selector=self._reset_btn, context=self._we)