from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.base import ComponentBase


class BetFilterRows(ComponentBase):
    _name = 'xpath=.//*[@id="betFliterRadioParamText"]'
    _radio_button = 'xpath=.//*[@id="betFliterRadio"]'
    _filter_text = 'xpath=.//*[@id="betFliterRadioSubParamText"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def radio_button(self):
        return self._find_element_by_selector(selector=self._radio_button)

    @property
    def filter_text(self):
        return self._get_webelement_text(selector=self._filter_text)


class YourBetting(Dialog):
    _pop_up_title = 'xpath=.//*[@data-uat="popUpTitle"]'
    _go_betting_button = 'xpath=.//*[@data-crlat="button.GO BETTING"]'
    _cancel_button = 'xpath=.//button[contains(text(), "Cancel")]'
    _item = 'xpath=.//*[@class="row"]'
    _list_item_type = BetFilterRows

    @property
    def pop_up_title(self):
        return self._get_webelement_text(selector=self._pop_up_title)

    @property
    def go_betting_button(self):
        return self._find_element_by_selector(selector=self._go_betting_button)

    @property
    def cancel_button(self):
        return self._find_element_by_selector(selector=self._cancel_button)
