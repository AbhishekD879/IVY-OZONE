from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase, DefaultBetButton
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.waiters import wait_for_result


class PlaceBetButton(DefaultBetButton):
    _output_price = 'xpath=.//*[@data-crlat="value"]'
    _odd_place_bet = 'xpath=.//*[@class="btn-odds placeBet"]'

    @property
    def odd_place_bet(self):
        return self._find_element_by_selector(self._odd_place_bet, context=self._we)


class FootballFieldItems(ComponentBase):
    _item_name = 'xpath=.//*[contains(@class,"market-name")]'
    _item_icon = 'xpath=.//*[@data-crlat="playerIcon"]'
    _added_player = 'xpath=.//*[@data-crlat="playerName"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._item_name, context=self._we)

    @property
    def icon(self):
        return ButtonBase(selector=self._item_icon, context=self._we)

    @property
    def added_player_name(self):
        return self._get_webelement_text(selector=self._added_player, context=self._we)


class FootballField(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="player"]'
    _list_item_type = FootballFieldItems
    _place_button = 'xpath=.//*[@data-crlat="placeBtn"]'
    _player_odds = 'xpath=.// *[ @class ="odds-label"] // *[@ data-crlat="value"]'

    @property
    def place_bet_button(self):
        return PlaceBetButton(selector=self._place_button, context=self._we)

    @property
    def player_odds(self):
        return self._find_element_by_selector(self._player_odds, context=self._we)


class FormationCarouselItems(ButtonBase):
    _item_name = 'xpath=.//*[@data-crlat="formationName"]'
    _icon = 'xpath=.//*[@data-crlat="formationIcon"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._item_name, context=self._we)


class FormationCarousel(ComponentBase):
    _list_item_type = FormationCarouselItems
    _item = 'xpath=.//*[@data-crlat="formationCell"]'


class SubHeader(ComponentBase):
    team_home_name = 'xpath=.//div[@class="team-name-home"]'
    team_away_name = 'xpath=.//div[@class="team-name-away"]'
    _value = 'xpath=.//*[@data-crlat="formationValue"]'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self.team_home_name, context=self._we) + " V " + self._get_webelement_text(selector=self.team_away_name, context=self._we)

    @property
    def formation_value(self):
        return self._get_webelement_text(selector=self._value, context=self._we)


class PitchBody(ComponentBase):
    _football_field_content = 'xpath=.//*[@data-crlat="footballField"]'
    _formation_carousel_container = 'xpath=.//*[@data-crlat="formationContainer"]'
    _sub_header_content = 'xpath=.//*[@data-crlat="shContent"]'
    _error_message = 'xpath=.//*[@data-crlat="errorMessage"]'
    _value = 'xpath=.//*[@data-crlat="formationValue"]'

    @property
    def football_field(self):
        return FootballField(selector=self._football_field_content, context=self._we)

    @property
    def formation_value(self):
        return self._get_webelement_text(selector=self._value, context=self._we)

    @property
    def formation_carousel(self):
        return FormationCarousel(selector=self._formation_carousel_container, context=self._we)

    @property
    def sub_header(self):
        return SubHeader(selector=self._sub_header_content, context=self._we)

    def wait_for_error_message(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._error_message) and self._find_element_by_selector(
                selector=self._error_message).is_displayed(),
            name=f'5-A-Side error message displayed status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def error_message_text(self):
        return TextBase(selector=self._error_message, context=self._we)


class PitchHeader(ComponentBase):
    _close_button = 'xpath=.//*[@data-crlat="drawer.closeButton"]'
    _title = 'xpath=.//*[@data-crlat="titleText"] |  .//*[@class="five-a-side-text"]'
    _instruction = 'xpath=.//*[@data-crlat="subtitleText"]'

    @property
    def title(self):
        return self._find_element_by_selector(self._title, context=self._we)

    @property
    def instruction_text(self):
        return self._get_webelement_text(self._instruction, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    def has_close_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_button,
                                                   timeout=0) is not None,
            name=f'Close button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class JorneyPanel(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class, "close-icon")]'  # change to 'xpath=.//*[@data-crlat="btnClose"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=1, context=self._we)


class PitchOverlay(ComponentBase):
    _pitch_body = 'xpath=.//*[@data-crlat="drawer.body"]'
    _header = 'xpath=.//*[@data-crlat="drawer.header"]'
    _has_journey_panel = 'xpath=.//*[contains(@class, "five-a-side-journey")]'  # change to 'xpath=.//*[@data-crlat="journeyPanel"]'
    _team_name = 'xpath=.//*[@class="player-team"]'

    @property
    def team_name(self):
        return self._find_element_by_selector(self._team_name, context=self._we)

    @property
    def content(self):
        return PitchBody(selector=self._pitch_body, context=self._we, timeout=3)

    @property
    def header(self):
        return PitchHeader(selector=self._header, context=self._we)

    @property
    def journey_panel(self):
        return JorneyPanel(selector=self._has_journey_panel, context=self._we, timeout=3)

    @property
    def has_journey_panel(self):
        journey_panel = self._find_element_by_selector(selector=self._has_journey_panel, context=self._we, timeout=0)
        return ComponentBase(web_element=journey_panel, timeout=0).is_displayed() if journey_panel else False
