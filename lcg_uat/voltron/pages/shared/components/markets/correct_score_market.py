from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.market_section_base import MarketSection
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton


class Score(ComponentBase):
    @property
    def score_value(self):
        return self._get_webelement_text(we=self._we)


class TeamResultsDropDown(ComponentBase):
    _item = 'xpath=.//option'
    _list_item_type = Score

    @property
    def selected_item(self):
        select = SelectBase(web_element=self._we, selector=self._selector)
        return select.first_selected_option.text

    def select_score_by_text(self, text):
        select = SelectBase(web_element=self._we, selector=self._selector)
        select.select_by_visible_text(text=text)

    @property
    def available_options(self):
        select = SelectBase(web_element=self._we, selector=self._selector)
        return select.available_options


class Outcome(ComponentBase):
    _outcome_name_alphabets = 'xpath=.//*[@data-crlat="outcomeEntity.name"]'
    _outcome_name_digits = 'xpath=.//*[@data-crlat="outcomeNameDigits"]'
    _output_price_button = 'xpath=.//*[contains(@data-crlat, "betButton")]'

    @property
    def caption(self):
        caption = self._get_webelement_text(selector=self._outcome_name_alphabets) + ' ' + self._get_webelement_text(
            selector=self._outcome_name_digits)
        return caption

    @property
    def name(self):
        return self.caption

    @property
    def bet_button(self):
        return BetButton(selector=self._output_price_button, context=self._we)


class Outcomes(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = Outcome

    @property
    def outcomes_prices(self):
        return [outcome.bet_button.outcome_price_text for outcome in self.items_as_ordered_dict.values()]


class CorrectScoreOutcomeTable(ComponentBase):
    _outcomes = 'xpath=.//*[@data-crlat="market.outcomes"]'
    _home_outcomes = 'xpath=.//*[@id="border"][1]/div[@id="lads-high"] | //*[@data-crlat="eventsTable"]/div[1]/div/price-odds-button'
    _draw_outcomes = 'xpath=.//*[@id="border"][2]/div[@id="lads-high"]|//*[@data-crlat="eventsTable"]/div[2]/div/price-odds-button'
    _away_outcomes = 'xpath=.//*[@id="border"][3]/div[@id="lads-high"]|//*[@data-crlat="eventsTable"]/div[3]/div/price-odds-button'

    @property
    def outcomes_list(self):
        outcomes = self._find_elements_by_selector(selector=self._outcomes)
        if len(outcomes) == 3:
            return outcomes
        return 'Expected 3 outcomes sections but found %s' % (len(outcomes))

    @property
    def home_outcomes(self):
        #return Outcomes(web_element=self.outcomes_list[0])
        elements = self._find_elements_by_selector(selector=self._home_outcomes)
        return elements


    @property
    def draw_outcomes(self):
        #return Outcomes(web_element=self.outcomes_list[1])
        elements = self._find_elements_by_selector(selector=self._draw_outcomes)
        return elements

    @property
    def away_outcomes(self):
        #return Outcomes(web_element=self.outcomes_list[2])
        elements = self._find_elements_by_selector(selector=self._away_outcomes)
        return elements


class CorrectScoreMarket(MarketSection):
    _team_home = 'xpath=.//*[@data-crlat="homeTeam.name"]'
    _team_away = 'xpath=.//*[@data-crlat="awayTeam.name"]'
    _team_a_scores = 'xpath=.//*[@data-crlat="maxValues.awayTeam"]|.//*[@class="team-col"][3]//select[@id="odd-value"]'
    _team_h_scores = 'xpath=.//*[@data-crlat="maxValues.homeTeam"] | .//*[@class="team-col"][1]//select[@id="odd-value"]'
    _correct_score_outcomes_table = 'xpath=.//*[@data-crlat="containerInnerContent"] | .//*[contains(@class,"container-inner-content")]'
    _correct_score_outcomes_table_type = CorrectScoreOutcomeTable
    _combined_outcome = 'xpath=.//*[@data-crlat="combinedOutcome"]'

    @property
    def outcome_table(self):
        return self._correct_score_outcomes_table_type(self._correct_score_outcomes_table, context=self._we)

    @property
    def team_home(self):
        return self._get_webelement_text(selector=self._team_home)

    @property
    def team_away(self):
        return self._get_webelement_text(selector=self._team_away)

    @property
    def team_home_scores(self):
        return TeamResultsDropDown(self._team_h_scores, context=self._we)

    @property
    def team_away_scores(self):
        return TeamResultsDropDown(self._team_a_scores, context=self._we)

    @property
    def combined_outcome_button(self):
        return ButtonBase(selector=self._combined_outcome, context=self._we)
