from voltron.pages.shared.dialogs.dialog_base import Dialog


class WhatIsCashout(Dialog):
    _description = 'xpath=.//*[@data-uat="popUpText"]'

    @property
    def description(self):
        return self._wait_for_not_empty_web_element_text(selector=self._description, timeout=3)
