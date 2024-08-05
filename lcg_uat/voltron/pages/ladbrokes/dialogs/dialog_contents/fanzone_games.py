from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class FanzoneGames(Dialog):
    _close_btn = 'xpath=.//*[@class="close-button"]'
    _games_title = 'xpath=.//*[@class="games-title"]'
    _games_text = 'xpath=.//*[@class="games-text"]'
    _play_button='xpath=.//*[@class="play-button"]'

    @property
    def close_btn(self):
        return ButtonBase(selector=self._close_btn, timeout=2)

    @property
    def play_button(self):
        return ButtonBase(selector=self._play_button, timeout=2)

    @property
    def games_title(self):
        return self._get_webelement_text(selector=self._games_title)

    @property
    def games_text(self):
        return self._get_webelement_text(selector=self._games_text)