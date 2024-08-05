from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceipt, BetReceiptSection, BetReceiptSectionsList


class LadbrokesBetReceiptSection(BetReceiptSection):
    _acca_sign_post = 'xpath=.//*[@data-crlat="label.acca-insurance"]'


class LadbrokesBetReceiptSectionsList(BetReceiptSectionsList):
    _list_item_type = LadbrokesBetReceiptSection


class LadbrokesBetReceipt(BetReceipt):

    @property
    def bet_receipt_sections_list(self):
        return LadbrokesBetReceiptSectionsList(selector=self._betreceipt_sections_list, context=self._we, timeout=30)
