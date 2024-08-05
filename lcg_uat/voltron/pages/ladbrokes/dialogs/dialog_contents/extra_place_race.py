from voltron.pages.shared.dialogs.dialog_base import Dialog


class ExtraPlaceDialog(Dialog):
    _pop_up_title = 'xpath=.//*[@data-uat="popUpTitle"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._pop_up_title, context=self._we)
