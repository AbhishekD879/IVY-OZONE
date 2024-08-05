from abc import abstractmethod
from time import sleep
from voltron.pages.shared.components.markets.correct_score_market import CorrectScoreMarket
from voltron.pages.shared.components.markets.market_section_base import SwitcherMarketSection
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class TeamResultsIncrement(ComponentBase):
    _decrease = 'xpath=.//*[@class="alignment"]'
    _score = 'xpath=.//*[@class="alignment1"]'
    _increase = 'xpath=.//*[@class="alignment1"]/following-sibling::button[@class="alignment"]'

    @property
    def selected_item(self):
        select_score = self._find_element_by_selector(selector=self._score, timeout=5)
        return select_score.text

    @property
    def score_decrease(self):
        return self._find_element_by_selector(selector=self._decrease, timeout=5)

    @property
    def score_increase(self):
        return self._find_element_by_selector(selector=self._increase, timeout=5)

    def select_score_by_text(self, text):
        score = True
        while score:
            selected_score = self.selected_item
            if text == selected_score:
                score = False
            else:
                self.score_increase.click()
                sleep(1.5)

    @abstractmethod
    def available_options(self):
        """Method that should provide available options"""


class BYBGroupingSelectionButtons(GroupingSelectionButtons):
    _item = 'xpath=.//*[contains(@class, "switch-btn_correctscore")]'


class BYBCorrectScoreMarket(CorrectScoreMarket, SwitcherMarketSection):
    _grouping_selection_buttons = 'xpath=.//*[@class="switchers_correctscore switchers-1"]'
    _grouping_selection_buttons_type = BYBGroupingSelectionButtons
    _team_home = 'xpath=.//*[@data-crlat="homeTeamLabel"]'
    _team_away = 'xpath=.//*[@data-crlat="awayTeamLabel"]'
    _team_a_scores = 'xpath=.//*[@data-crlat="awayTeamLabel"]/preceding-sibling::div[@class="btn-group1"]'
    _team_h_scores = 'xpath=.//*[@data-crlat="homeTeamLabel"]/preceding-sibling::div[@class="btn-group1"]'
    _add_to_betslip_btn = 'xpath=.//*[@class="btn-group btn btn-active" or @class="btn-group btn btn-active-lads"]'
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def has_grouping_buttons(self):
        return self._find_elements_by_selector(self._grouping_selection_buttons, timeout=5) != []

    @property
    def grouping_buttons(self):
        if self.has_grouping_buttons:
            self._wait_active()
            return self._grouping_selection_buttons_type(self._grouping_selection_buttons, timeout=1, context=self._we)
        else:
            raise VoltronException('No Grouping Buttons object found')

    @property
    def team_home_scores(self):
        return TeamResultsIncrement(self._team_h_scores, context=self._we)

    @property
    def team_away_scores(self):
        return TeamResultsIncrement(self._team_a_scores, context=self._we)