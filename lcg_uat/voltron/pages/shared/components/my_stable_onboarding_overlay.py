from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class MyStableOnboardingOverlay(ComponentBase):
    _close_button = 'xpath=.//*[@data-uat="popUpCloseButton"]'
    _ok_thanks = 'xpath=.//*[@data-crlat="ctaButton"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def ok_thanks(self):
        return ButtonBase(selector=self._ok_thanks, context=self._we)