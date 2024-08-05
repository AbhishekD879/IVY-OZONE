from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase, DefaultBetButton
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.components.markets.market_section_base import MarketSection


class CorrectScoreTeams(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="correctScoreTeamsItem"]'
    _list_item_type = ButtonBase


class PlayerScorersList(SelectBase):
    _player = 'xpath=.//option'

    @property
    def selected_item(self):
        select = Select(self._we)
        return select.first_selected_option.text

    def select_player_by_index(self, index):
        select = Select(self._we)
        select.select_by_index(index=index)


class TeamResultsDropDown(SelectBase):
    _team_scorer = 'xpath=.//option'

    @property
    def selected_item(self):
        select = Select(self._we)
        return select.first_selected_option.text

    def select_score_by_index(self, index):
        select = Select(self._we)
        self._logger.debug(f'*** Selecting score {self._get_webelement_text(we=self._we)}')
        select.select_by_index(index=index)

    def select_value(self, value):
        try:
            self._select_control.select_by_value(value=value)
        except NoSuchElementException:
            self._select_control.select_by_index(0)


class ScorecastMarket(MarketSection):
    _first_scorer = 'xpath=.//*[@data-crlat="scorecastMarkets" and text()="First Scorer"]'
    _last_scorer = 'xpath=.//*[@data-crlat="scorecastMarkets" and text()="Last Scorer"]'
    _team_names = 'xpath=.//*[@data-crlat="goalscorerTeamItem"]'
    _player_scorers_list = 'xpath=.//*[@data-crlat="playerScorersList"]'
    _home_team_results_list = 'xpath=.//*[@data-crlat="scorecastTeamScore.home"]'
    _away_team_results_list = 'xpath=.//*[@data-crlat="scorecastTeamScore.away"]'
    _correct_score_teams = 'xpath=.//*[@data-crlat="correctScoreTeams"]'
    _correct_score_teams_type = CorrectScoreTeams
    _add_to_betslip_btn = 'xpath=.//*[@data-crlat="addToBetslipBtn"]'
    _output_price = 'xpath=.//*[@data-crlat="outputPrice"]'

    @property
    def player_scorers_list(self):
        we = self._find_element_by_selector(selector=self._player_scorers_list)
        return PlayerScorersList(web_element=we)

    @property
    def home_team_results_dropdown(self):
        return TeamResultsDropDown(selector=self._home_team_results_list)

    @property
    def away_team_results_dropdown(self):
        return TeamResultsDropDown(selector=self._away_team_results_list)

    @property
    def first_scorer_tab(self):
        return ButtonBase(selector=self._first_scorer, context=self._we, timeout=1)

    @property
    def last_scorer_tab(self):
        return ButtonBase(selector=self._last_scorer, context=self._we, timeout=1)

    @property
    def team_names(self):
        team_names = self._find_elements_by_selector(selector=self._team_names)
        if len(team_names) == 2:
            self._logger.info('*** Found teams: {0} and {1}'.format(team_names[0].text, team_names[1].text))
        elif len(team_names) == 1:
            self._logger.info('*** Found team: {0}'.format(team_names[0].text))
        return team_names

    @property
    def first_goalscorer_team_button(self):
        return ButtonBase(web_element=self.team_names[0])

    @property
    def first_goal_scorer_team_attribute_text(self):
        return self.first_goalscorer_team_button.get_attribute('text')

    @property
    def last_goalscorer_team_button(self):
        return ButtonBase(web_element=self.team_names[1])

    @property
    def correct_score_teams(self):
        return self._correct_score_teams_type(self._correct_score_teams, context=self._we)

    @property
    def add_to_betslip(self):
        return DefaultBetButton(selector=self._add_to_betslip_btn, context=self._we)

    @property
    def output_price(self):
        return self._get_webelement_text(selector=self._output_price, context=self._we, timeout=1)
