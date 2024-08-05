from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class UpgradeYourAccount(Dialog):
    _no_thanks_link = 'xpath=.//*[@data-crlat="noThanksLink"]'
    _default_action = 'click_no_thanks_link'

    @property
    def no_thanks_link(self):
        return LinkBase(selector=self._no_thanks_link, context=self._we)

    def click_no_thanks_link(self):
        self.no_thanks_link.click()
