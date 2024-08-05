from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class BetslipFull(Dialog):
    _title = 'xpath=.//*[@data-uat="popUpText"]'

    @property
    def title_text(self):
        return wait_for_result(
            lambda: self._get_webelement_text(selector=self._title),
            name='Dialog name not empty',
            timeout=0.5
        )
