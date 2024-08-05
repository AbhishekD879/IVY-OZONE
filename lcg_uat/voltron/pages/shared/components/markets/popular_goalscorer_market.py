from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.market_section_base import SwitcherMarketSection


class Outcome(ComponentBase):
    _event_name = 'xpath=.//*[@data-crlat="outcomeEntity.name" or @data-crlat="oddsNames"]'
    _bet_button = 'xpath=.//*[contains(@data-crlat, "betButton")]'

    @property
    def event_name(self):
        return self._find_element_by_selector(selector=self._event_name).text

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)


class PopularGoalscorerTable(ComponentBase):
    _columns = 'xpath=.//*[@data-crlat="oddsHeader"]'
    _players = 'xpath=.//*[@data-crlat="oddsNames"]'
    _fixture_header = 'xpath=.//*[@data-crlat="eventOddsHeader"]'
    _fixture_header_type = FixtureHeader
    _item = 'xpath=.//*[@data-crlat="oddsCard.sportTemplate" or @data-crlat="oddsCard"]'
    _list_item_type = Outcome

    @property
    def fixture_headers(self):
        fixture_headers = []
        columns = self._find_elements_by_selector(selector=self._fixture_header)
        for header in columns:
            fixture_headers.append(header.text)
        return fixture_headers

    @property
    def columns(self):
        column_names = []
        columns = self._find_elements_by_selector(selector=self._columns)
        for column in columns:
            column_names.append(column.text)
        return column_names

    @property
    def players(self):
        player_names = []
        players = self._find_elements_by_selector(selector=self._players)
        for player in players:
            player_names.append(player.text)
        return player_names


class PopularGoalscorerMarket(SwitcherMarketSection):
    _outcome_table = 'xpath=.//*[@data-crlat="containerInnerContent.table"]'
    _outcome_table_type = PopularGoalscorerTable

    @property
    def outcome_table(self):
        return self._outcome_table_type(self._outcome_table, context=self._we)
