from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class LossLimitDialog(ComponentBase):
    _im_happy = 'xpath=.//*[contains(@class, "btn btn-light")]'

    @property
    def im_happy_with_limit(self):
        return ButtonBase(selector=self._im_happy, context=self._we)
