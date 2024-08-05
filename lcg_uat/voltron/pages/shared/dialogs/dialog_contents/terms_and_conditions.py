from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.exceptions.voltron_exception import VoltronException


class TermsAndConditions(Dialog):
    _text = 'xpath=.//*[@data-crlat="termsAndConditionText"]'
    _ok_button = 'xpath=.//*[@data-crlat="acceptTermsButton"]'
    _default_action = 'click_ok'
    _view_button = 'xpath=.//*[@data-crlat="viewTermsButton"]'

    @property
    def text(self):
        try:
            we = self._find_elements_by_selector(selector=self._text, timeout=0)
        except Exception:
            raise VoltronException(message='Error getting dialog text')
        return we.text

    def click_ok(self):
        ButtonBase(selector=self._ok_button).click()

    def default_action(self):
        self.click_ok()

    def click_view_terms(self):
        ButtonBase(selector=self._view_button).click()
