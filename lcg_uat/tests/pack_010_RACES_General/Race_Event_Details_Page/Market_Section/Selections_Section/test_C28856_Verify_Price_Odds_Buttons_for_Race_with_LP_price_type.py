import operator
import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod It's almost unreal to find HR event with the same price for selections and event if we find it
# - it'll take many time to work with all existing events and selections to find and verify it
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28856_Verify_Price_Odds_Buttons_for_Race_with_LP_price_type(BaseRacing):
    """
    TR_ID: C28856
    NAME: Verify Price/Odds Buttons for Race with LP price type
    DESCRIPTION: Verify Price/Odds Buttons for <Race> with LP price type
    PRECONDITIONS: There is <Race> event with LP prices available, there are some selections with the same Price/Odds
    """
    keep_browser_open = True
    lp_prices = {0: '1/2', 1: '1/2', 2: '1/5', 3: '1/3'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event in OB TI
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=4,
                                                          lp_prices=self.lp_prices)
        self._logger.info('*** Created event with parameters {}'.format(event_params))
        self.__class__.eventID = event_params.event_id
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.selection_names = self.selection_ids.keys()

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No one market tab found')

    def test_002_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify Price/Odds buttons
        EXPECTED: Prices are correct for each selection, values correspond to the **'priceNum'** and **'priceDec'** attributes
        DESCRIPTION: Verify order of selections
        EXPECTED: *  Selections are ordered by price in ascending order (lowest to highest)
        EXPECTED: *  If odds of selections are the same then order by runner number is used
        """
        outcome_prices = []
        outcome_numbers = []
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one event section with outcomes found')
        for section_name, section in sections.items():
            outcomes = section.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No one outcome found for section: "{section_name}"')
            for outcome_name, outcome in outcomes.items():
                self.assertTrue(outcome.bet_button.outcome_price_text,
                                msg=f'Outcome "{outcome_name}" does not have price')
                outcome_prices.append(outcome.bet_button.outcome_price_text)
                outcome_numbers.append(outcome.runner_number)
        outcome_number_price = dict(zip(outcome_numbers, outcome_prices))
        outcome_number_price_list = [(k, v) for k, v in outcome_number_price.items()]
        self._logger.debug(f'Outcome number with price from UI: {outcome_number_price_list}')

        created_events = dict(zip(['1', '2', '3', '4'], self.lp_prices.values()))
        sorted_events_list = sorted(sorted(created_events.items()), key=operator.itemgetter(1), reverse=True)

        self._logger.debug(f'*** Created events with prices: {sorted_events_list}')

        self.assertListEqual(sorted_events_list, outcome_number_price_list,
                             msg=f'Created selections {sorted_events_list} is not '
                                 f'equal to expected {outcome_number_price_list}')
