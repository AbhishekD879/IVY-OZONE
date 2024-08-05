from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class FanZoneBanner(ComponentBase):
    _let_me_see = 'xpath=.//*[contains(@class, "let_me_see")]'
    _welcome_text = 'xpath=.//*[@class="fz_welcome_text"]'
    _fanzone_name = 'xpath=.//*[@class="fz_name"]'

    @property
    def let_me_see(self):
        return ButtonBase(selector=self._let_me_see, context=self._we, timeout=5)

    @property
    def welcome_text(self):
        return self._get_webelement_text(selector=self._welcome_text, context=self._we, timeout=5)

    @property
    def fanzone_name(self):
        return self._get_webelement_text(selector=self._fanzone_name, context=self._we, timeout=5)
