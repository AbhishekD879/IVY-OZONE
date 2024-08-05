from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class CoralUpgradeYourAccount(ComponentBase):
    # todo     VOL-5540  CoralUpgradeYourAccount should be moved to shared and renamed
    _no_thanks_button = 'xpath=.//button[contains(@class, "btn no-thanks")]'
    _upgrade_button = 'xpath=.//*[contains(@class, "btn btn-primary")]'

    @property
    def no_thanks_button(self):
        return ButtonBase(selector=self._no_thanks_button, context=self._we)

    @property
    def upgrade_button(self):
        return ButtonBase(selector=self._upgrade_button, context=self._we)
