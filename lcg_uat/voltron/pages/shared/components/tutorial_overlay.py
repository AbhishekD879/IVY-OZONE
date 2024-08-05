from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class TutorialOverlayTextPanel(ComponentBase):
    _close_button = 'xpath=.//*[@data-crlat="closeTutorialBtn"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class TutorialOverlay(ComponentBase):
    _text_panel = 'xpath=.//*[@data-crlat="textPanel"]'
    _tutorial_text = 'xpath=.//*[contains(@class,"arr-panel")]/div'
    _timeline_overlay_tutorial_close = 'xpath=.//button[@class="btn tlt-btn" or @class="btn tlt-btn coral-btn"]'

    @property
    def tutorial_arrow_overlay(self):
        return self._find_elements_by_selector(selector=self._tutorial_text)

    @property
    def text_panel(self):
        return TutorialOverlayTextPanel(selector=self._text_panel, context=self._we)

    @property
    def close_icon(self):
        return ButtonBase(selector=self._timeline_overlay_tutorial_close)
