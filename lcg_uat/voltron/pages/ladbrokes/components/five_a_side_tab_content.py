from voltron.pages.ladbrokes.components.five_a_side_pitch import PitchOverlay
from voltron.pages.ladbrokes.components.five_a_side_player_card import PlayerCard
from voltron.pages.ladbrokes.components.five_a_side_players_list import PlayersOverlay
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result


class BuildTeam(ComponentBase):
    # cannot replace by data-clat because there is no element in static html
    _build_team_button = 'xpath=.//*[@class="build"]'

    @property
    def build_button(self):
        return ButtonBase(selector=self._build_team_button, context=self._we)


class FiveASideTabContent(TabContent):
    _team_launcher_content = 'xpath=.//*[@data-crlat="teamLauncher"]'
    _pitch_content = 'xpath=.//*[@data-crlat="pitchContent"]'
    _players_overlay = 'xpath=.//*[@data-crlat="playerListContent"]'
    _player_card = 'xpath=.//*[@data-crlat="playerCardContent"]'
    _betslip_panel = 'xpath=.//*[@data-crlat="quickbetPanel" and contains(@class, "slide-up")]'
    _new_label = 'xpath=.//*[@class="badge-new"]'
    _five_a_side_title = 'xpath=.//*[contains(text(),"5-A-Side Team")]'
    _five_a_side_text = 'xpath=.//*[contains(text(),"Pick any 5")]'

    @property
    def new_label(self):
        return self._find_element_by_selector(selector=self._new_label, context=self._we, timeout=0)

    @property
    def five_a_side_title(self):
        return self._get_webelement_text(selector=self._five_a_side_title)

    @property
    def five_a_side_text(self):
        return self._get_webelement_text(selector=self._five_a_side_text)

    def _wait_active(self, timeout=0):
        """
        Overriding method from TabContent
        """
        pass

    @property
    def team_launcher(self):
        return BuildTeam(selector=self._team_launcher_content, context=self._we)

    @property
    def pitch_overlay(self):
        return PitchOverlay(selector=self._pitch_content, context=self._we)

    @property
    def players_overlay(self):
        return PlayersOverlay(selector=self._players_overlay, context=self._we)

    @property
    def player_card(self):
        return PlayerCard(selector=self._player_card, context=self._we)

    def wait_for_pitch_overlay(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._pitch_content, timeout=0) is not None,
            expected_result=expected_result,
            name='5-A-Side overlay to be displayed',
            timeout=timeout)

    def wait_for_players_overlay(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._players_overlay, timeout=0) is not None,
            expected_result=expected_result,
            name='Players overlay to be displayed',
            timeout=timeout)

    def wait_for_players_card(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._player_card, timeout=0) is not None,
            expected_result=expected_result,
            name='Players card to be displayed',
            timeout=timeout)

    def wait_for_players_card_closed(self, expected_result=False, timeout=2):
        return wait_for_result(
            lambda:
            self._find_element_by_selector(selector=self._player_card, timeout=0) is not None and
            self._find_element_by_selector(selector=self._player_card, timeout=0).is_displayed(),
            expected_result=expected_result,
            name='Players card to be closed',
            timeout=timeout)
