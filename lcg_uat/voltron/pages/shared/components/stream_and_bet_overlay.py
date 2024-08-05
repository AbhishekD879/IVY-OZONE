from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class StreamAndBetOverlay(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class,"tutorial-onboarding-close")]'
    _pop_up_content = 'xpath=.//*[@class="pop-up-content"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def pop_up_content(self):
        return StreamAndBetOverlayTextPanel(selector=self._pop_up_content, context=self._we)


class StreamAndBetOverlayTextPanel(ComponentBase):
    _popup_title = 'xpath=.//*[@class="popup-title"]'
    _full_screen_mode_description = 'xpath=.//*[contains(@class,"popup-description-one")][1]'
    _place_your_bet_description = 'xpath=.//*[contains(@class,"popup-description-one")][2]'
    _go_betting = 'xpath=.//*[@class="popup-button"]'

    @property
    def tutorial_arrow_overlay(self):
        return self._find_elements_by_selector(selector=self._tutorial_text)

    @property
    def full_screen_mode_description(self):
        self._get_webelement_text(selector=self._full_screen_mode_description)

    @property
    def place_your_bet_description(self):
        self._get_webelement_text(selector=self._place_your_bet_description)

    @property
    def go_betting(self):
        return ButtonBase(selector=self._go_betting)


