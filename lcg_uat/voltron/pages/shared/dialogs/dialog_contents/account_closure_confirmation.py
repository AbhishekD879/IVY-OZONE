from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase, TextBase


class ConfirmationText(ComponentBase):
    _prefix = 'xpath=.//*[@data-crlat="prefix"]'
    _time_out_link = 'xpath=.//*[@data-crlat="time-out-link"]'
    _or = 'xpath=.//*[@data-crlat="or"]'
    _reality_check_link = 'xpath=.//*[@data-crlat="reality-check-link"]'

    @property
    def text(self):
        prefix = self._get_webelement_text(selector=self._prefix, timeout=0)
        time_out_link = self._get_webelement_text(selector=self._time_out_link, timeout=0)
        or_part = self._get_webelement_text(selector=self._or, timeout=0)
        reality_check_link = self._get_webelement_text(selector=self._reality_check_link, timeout=0)
        return f'{prefix} {time_out_link} {or_part} {reality_check_link}'

    @property
    def time_out_link(self):
        return LinkBase(selector=self._time_out_link, context=self._we)

    @property
    def reality_check_link(self):
        return LinkBase(selector=self._reality_check_link, context=self._we)


class AccountClosureConfirmation(Dialog):
    _confirmation_description = 'xpath=.//*[@data-crlat="confirmartion-description"]'
    _confirm_check_box = 'xpath=.//*[@data-crlat="check-confirmation"]'
    _confirm_text = 'xpath=.//*[@data-crlat="confirmation-text"]'
    _error_message = 'xpath=.//*[@data-crlat="error"]'
    _yes_button = 'xpath=.//*[@data-crlat="button-yes"]'
    _cancel_button = 'xpath=.//*[@data-crlat="button-cancel"]'

    @property
    def confirm_check_box(self):
        return CheckBoxBase(selector=self._confirm_check_box, context=self._we)

    @property
    def error_message(self):
        return TextBase(selector=self._error_message, context=self._we)

    @property
    def yes_button(self):
        return ButtonBase(selector=self._yes_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def confirmation_description(self):
        return ConfirmationText(selector=self._confirmation_description, context=self._we)

    @property
    def confirm_text(self):
        return self._get_webelement_text(selector=self._confirm_text, context=self._we)
