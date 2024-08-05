from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.siteserve_client import racing_form, price_history, prune, simple_filter

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # we can't trigger live updates on prod and hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.liveserv_updates
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C236728_Verify_Price_Change_and_Previous_Odds_on_EDP_Fractional(BaseRacing):
    """
    TR_ID: C236728
    NAME: Verify Price Change and Previous Odds on EDP - Fractional
    DESCRIPTION: This test case verify displaying of Previous odds under Price/Odds button for Fractional Format
    """
    keep_browser_open = True
    markets = [('top_2_finish',)]
    price = ['1/10', '1/7', '1/5', '1/3']

    def get_historic_prices(self, query):
        response = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, query_builder=query)

        historic_prices = response[0]['event']['children'][0]['market']['children'][0]['outcome']['children']
        live_prices = []
        for price in historic_prices:
            historic_price = price.get('historicPrice')
            if historic_price:
                live_prices.append(f'{historic_price.get("livePriceNum")}/{historic_price.get("livePriceDen")}')

        return live_prices

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create virtual racing event
        EXPECTED: Virtual Racing event added
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, markets=self.markets,
                                                   lp_prices={0: self.price[0]})
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_trigger_price_changing_for_some_outcome_and_check_previous_odds(self):
        """
        DESCRIPTION: Trigger price changing for some outcome and check Previous Odds
        EXPECTED: 'Price/Odds' button immediately displays new price
        EXPECTED: Previous price/odd is displayed under Price/odds button immediately
        """
        edp = self.site.racing_event_details
        sections = edp.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.__class__.selection_name, self.__class__.selection = list(outcomes.items())[0]
        self.__class__.selection_id = self.selection_ids['win_or_each_way'][self.selection_name]

        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[1])
        result = wait_for_result(lambda: self.selection.previous_price == self.price[0],
                                 name=f'Previous price {self.price[0]} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=50)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[1],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[1]}"')

    def test_003_repeat_step_2_several_times_and_check_previous_odds(self):
        """
        DESCRIPTION: Repeat step №2 several times and check Previous Odds
        EXPECTED: New Odds are displayed correctly
        EXPECTED: Previous Odds are updated successfully each time
        EXPECTED: Only 2 last Previous Odds are displayed in format X/X>X/X (older one goes first)
        """
        expected_previous_price = f'{self.price[0]} > {self.price[1]}'
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[2])

        result = wait_for_result(lambda: self.selection.previous_price == expected_previous_price,
                                 name=f'Previous price {expected_previous_price} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=15)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[2],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[2]}"')

        expected_previous_price = f'{self.price[1]} > {self.price[2]}'
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[3])

        result = wait_for_result(lambda: self.selection.previous_price == expected_previous_price,
                                 name=f'Previous price {expected_previous_price} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=15)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[3],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[3]}"')

    def test_004_verify_previous_odds_correctness(self):
        """
        DESCRIPTION: Verify Previous Odds correctness
        EXPECTED: Previous Odds correspond to livePriceNum and livePriceDen attributes from tag <historicPrice .../>
        EXPECTED: Previous odds are ordered according to 'displayOrder' attribute (the biggest - the last)
        """
        query = self.ss_query_builder\
            .add_filter(racing_form(LEVELS.EVENT))\
            .add_filter(racing_form(LEVELS.OUTCOME))\
            .add_filter(price_history())\
            .add_filter(prune())\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.start_date_minus))

        result = wait_for_result(lambda: len(self.get_historic_prices(query)) == 3,
                                 name=f'Waiting for all three historic prices are recorded in SiteServe.',
                                 timeout=10)
        self.assertTrue(result, 'Not all historic prices were recorded in SiteServe. '
                                'Expected amount of historic prices is 3')

        live_prices = self.get_historic_prices(query)
        expected_old_price_value = None
        try:
            expected_old_price_value = f'{live_prices[-2]} > {live_prices[-1]}'
        except IndexError as e:
            self._logger.warning(f'*** Overriding exception {e}')
        self.assertEqual(self.selection.previous_price, expected_old_price_value,
                         msg=f'Old price value {self.selection.previous_price} '
                             f'is not the same as retrieved from from SiteServe {expected_old_price_value}')

    def test_005_trigger_price_changing_for_some_outcome_from_market_tab_which_is_not_active_at_the_moment(self):
        """
        DESCRIPTION: Trigger price changing for some outcome from Market tab which is not active at the moment
        """
        markets_properties = self.markets[0]
        market_name = markets_properties[0]
        self.__class__.selection_id = self.selection_ids[market_name][self.selection_name]
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[1])

    def test_006_open_this_market(self):
        """
        DESCRIPTION: Open this Market
        EXPECTED: 'Price/Odds' button displays new price
        EXPECTED: Updated Previous Odds are displayed there as well
        """
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.TOP_FINISH_MARKET_NAME)

        edp = self.site.racing_event_details
        sections = edp.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        top_finish_selection_name, self.__class__.top_finish_selection = list(outcomes.items())[0]

        result = wait_for_result(lambda: self.top_finish_selection.previous_price == self.price[0],
                                 name=f'Previous price {self.price[0]} to appear. '
                                      f'Current is {self.top_finish_selection.previous_price}',
                                 timeout=15)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.top_finish_selection.bet_button.name, self.price[1],
                         msg=f'Bet button price "{self.top_finish_selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[1]}"')

    def test_007_suspend_one_outcome_and_then_trigger_price_change_for_it(self):
        """
        DESCRIPTION: Suspend one outcome and then trigger price change for it
        EXPECTED: 'Price/Odds' button is disabled
        EXPECTED: 'Price/Odds' button displays new price
        EXPECTED: Updated Previous Odds are displayed there as well
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[2])
        result = wait_for_result(lambda: self.top_finish_selection.bet_button.name == self.price[2],
                                 name=f'Price {self.price[2]} to appear. '
                                      f'Current is {self.top_finish_selection.previous_price}',
                                 timeout=15)
        self.assertTrue(result, msg='Price was not changed')
        expected_previous_price = f'{self.price[0]} > {self.price[1]}'
        self.assertEqual(self.top_finish_selection.previous_price, expected_previous_price,
                         msg=f'Previous price "{self.top_finish_selection.previous_price}" '
                             f'is not the same as expected "{expected_previous_price}"')
        self.assertFalse(self.top_finish_selection.bet_button.is_enabled(), msg='Bet button is not disabled')
