from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.js_functions import click


class InfomationDialog(Dialog):
    _ok_button = 'xpath=.//*[@data-crlat="button.Ok"]'
    _dialog_content = 'xpath=.//*[@data-crlat="popUpText"]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, context=self._we)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we).replace('\n\n', ' ').replace('\n', ' ')

    def click_ok(self):
        ok_button = self._find_element_by_selector(selector=self._ok_button)
        click(ok_button)
