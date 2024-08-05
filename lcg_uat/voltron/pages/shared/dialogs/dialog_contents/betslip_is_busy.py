from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class BetslipIsBusy(Dialog):
    _text = 'xpath=.//*[@class="modal-header"]'
    _continue_button = 'xpath=.//*[@data-uat="popUpButton"]'
    _description = 'xpath=.//*[@class="text-center"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def description(self):
        return self._wait_for_not_empty_web_element_text(selector=self._description, timeout=3)
