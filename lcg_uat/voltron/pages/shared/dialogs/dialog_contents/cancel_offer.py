from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class CancelOffer(Dialog):
    _cancel_offer_button = 'xpath=.//*[@data-crlat="button.CANCEL OFFER"]'
    _no_return_button = 'xpath=.//*[@data-crlat="button.NO, RETURN"]'
    _cancel_offer_msg = 'xpath=.//*[@data-crlat="popUpText"]'

    @property
    def cancel_offer_button(self):
        return ButtonBase(selector=self._cancel_offer_button, context=self._we)

    @property
    def no_return_button(self):
        return ButtonBase(selector=self._no_return_button, context=self._we)

    @property
    def cancel_offer_msg(self):
        return ButtonBase(selector=self._cancel_offer_msg, context=self._we)
