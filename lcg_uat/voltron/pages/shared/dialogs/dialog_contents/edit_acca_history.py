from voltron.pages.shared.components.edit_acca_history import EditAccaHistoryBody
from voltron.pages.shared.dialogs.dialog_base import Dialog


class EditAccaHistory(Dialog):
    _acca_history_body = 'xpath=.//*[@data-crlat="emaHistoryList"]'

    @property
    def content(self):
        return EditAccaHistoryBody(selector=self._acca_history_body, context=self._we, timeout=3)
