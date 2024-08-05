from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class RemovePlayer(Dialog):
    _remove_player = 'xpath=.//*[@data-crlat="button.Remove"]'
    _cancel_player = 'xpath=.//*[@data-crlat="button.Cancel"]'
    _pop_up_text = 'xpath=.//*[@data-crlat="popUpText"]'

    @property
    def remove_player(self):
        return ButtonBase(selector=self._remove_player, context=self._we)

    @property
    def cancel(self):
        return ButtonBase(selector=self._cancel_player, context=self._we)

    @property
    def pop_up_text(self):
        return self._get_webelement_text(selector=self._pop_up_text)
