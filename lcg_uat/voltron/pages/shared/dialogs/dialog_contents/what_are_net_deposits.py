from voltron.pages.shared.dialogs.dialog_base import Dialog


class WhatAreNetDeposits(Dialog):
    _description = 'xpath=.//*[@data-crlat="popUpText"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._description, timeout=2)
