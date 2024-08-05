from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class SelectionInfo(ComponentBase):
    _price_info = 'xpath=.//*[@data-crlat="priceInfo"]'
    _event_name = 'xpath=.//*[@data-crlat="eventName"]'

    @property
    def name(self):
        return self.new_price_type

    @property
    def new_price_type(self):
        return ' '.join(self._get_webelement_text(selector=self._price_info).split())

    @property
    def event_name(self):
        return ' '.join(self._get_webelement_text(selector=self._event_name).split())


class OveraskChangedMultiple(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="declinedMultBet"]'
    _list_item_type = SelectionInfo
    _stake_message = 'xpath=.//*[@data-crlat="stakeMsg"]'

    @property
    def stake_message(self):
        return TextBase(selector=self._stake_message, context=self._we, timeout=3).name
