from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.dialogs.dialog_contents.infomation_dialog import InfomationDialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class LadbrokesAccaInsuranceOfferDialog(InfomationDialog):
    _more_button = 'xpath=.//*[@data-crlat="button.More"]'
    _dialog_title = 'xpath=.//*[@data-uat="popUpTitle"]'
    _ok_button = 'xpath=.//*[@data-crlat="button.OK"]'

    @property
    def more_button(self):
        return ButtonBase(selector=self._more_button, context=self._we)

    @property
    def dialog_title(self):
        return TextBase(selector=self._dialog_title, context=self._we, timeout=5)
