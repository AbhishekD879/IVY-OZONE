from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class BetReceiptInfo(ComponentBase):
    _date = 'xpath=.//*[@data-crlat="displayDate"]'
    _bet_receipt = 'xpath=.//*[@data-crlat="betReceipt"]'
    _bet_id = 'xpath=.//*[@data-uat="betId"]'

    @property
    def date(self):
        return TextBase(selector=self._date, context=self._we)

    @property
    def bet_receipt(self):
        return TextBase(selector=self._bet_receipt, context=self._we)

    @property
    def bet_id(self):
        return self._get_webelement_text(selector=self._bet_id)
