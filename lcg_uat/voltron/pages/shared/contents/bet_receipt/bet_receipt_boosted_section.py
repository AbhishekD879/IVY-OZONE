from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import IconBase


class BetReceiptBoostedSection(ComponentBase):
    _boosted_icon = 'xpath=.//*[@data-crlat="boostIcon"]'
    _boosted_text = 'xpath=.//*[@data-crlat="boostText"]'

    @property
    def icon(self):
        return IconBase(selector=self._boosted_icon, context=self._we)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._boosted_text, context=self._we)
