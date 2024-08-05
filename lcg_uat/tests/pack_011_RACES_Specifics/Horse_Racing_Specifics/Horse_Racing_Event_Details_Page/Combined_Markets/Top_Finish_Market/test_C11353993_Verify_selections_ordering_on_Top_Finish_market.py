import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.markets
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C11353993_Verify_selections_ordering_on_Top_Finish_market(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C11353993
    NAME: Verify selections ordering on 'Top Finish' market
    """
    keep_browser_open = True
    markets = [
        ('top_2_finish',),
        ('top_3_finish',),
        ('top_4_finish',)
    ]
    price = '1/2'
    price_2 = '1/3'
    expected_runners_order = ['3', '4', '1', '2', '5']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and login
        """
        event_params = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=5,
                                                          lp_prices={0: self.price,
                                                                     1: '',
                                                                     2: self.price_2,
                                                                     3: self.price_2,
                                                                     4: ''})
        self.__class__.eventID = event_params.event_id

        self.site.login()

    def test_001_navigate_to_edp_and_open_top_finish_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'Top Finish' market tab
        EXPECTED: 'Top Finish' market tab is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertIn(vec.racing.TOP_FINISH_MARKET_NAME, market_tabs.keys(),
                      msg=f'"{vec.racing.TOP_FINISH_MARKET_NAME}" tab was not found in the tabs list "{market_tabs.keys()}"')

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.TOP_FINISH_MARKET_NAME)

    def test_002_verify_top_finish_market_headers(self):
        """
        DESCRIPTION: Verify 'Top Finish' market headers
        EXPECTED: 'TOP 2' 'TOP 3' 'TOP 4' market headers are displayed
        """
        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertIn(vec.racing.TOP_FINISH_MARKET_NAME, event_markets_list,
                      msg=f'"{vec.racing.TOP_FINISH_MARKET_NAME}" market was not found')

        self.__class__.event_market = event_markets_list[vec.racing.TOP_FINISH_MARKET_NAME]
        market_headers = self.event_market.section_header.items_as_ordered_dict

        self.assertTrue(market_headers, msg='No market headers found')

        self.softAssert(self.assertListEqual, list(market_headers.keys()), vec.racing.TOP_FINISH_FIXTURE_HEADERS,
                        msg=f'Market headers "{list(market_headers.keys())}" are not the same '
                        f'as expected "{vec.racing.TOP_FINISH_FIXTURE_HEADERS}"')

    def test_003_verify_selections(self):
        """
        DESCRIPTION: Verify selections
        EXPECTED: Available selections are displayed in the grid, odds of each are shown in correct market section (TOP 2, TOP 3, TOP 4)
        EXPECTED: Selection name, runner number, silks and trainer are displayed for each selection (if available)
        EXPECTED: If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        """
        self.__class__.market_outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(self.market_outcomes, msg=f'No combined market: "{vec.racing.TOP_FINISH_MARKET_NAME}" selections found')

        for outcome in self.market_outcomes.values():
            if outcome.bet_button.outcome_price_text != 'SP':
                self.softAssert(self.assertRegexpMatches,
                                outcome.bet_button.outcome_price_text,
                                self.fractional_pattern,
                                msg=f'Price value "{outcome.bet_button.outcome_price_text}" does '
                                f'not match fractional pattern: "{self.fractional_pattern}"')

    def test_004_verify_selections_ordering(self):
        """
        DESCRIPTION: Verify selections ordering
        EXPECTED: Selections are ordered by odds in first available market (e.g. TOP 2/TOP 3/TOP 4) in ascending order (lowest to highest)
        EXPECTED: If odds of selections are the same -> display by runnerNumber (in ascending order)
        EXPECTED: If prices are absent for selections - display by runnerNumber (in ascending order)
        """
        runner_numbers = []
        for outcome_name, outcome in self.market_outcomes.items():
            runner_numbers.append(outcome.runner_number)

        self.softAssert(self.assertEqual, runner_numbers, self.expected_runners_order,
                        msg=f'Runners order "{runner_numbers}" is not the same '
                        f'as expected "{self.expected_runners_order}"')

    def test_005_change_price_format_to_decimal_in_my_account_and_repeat_steps_1_4(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 1 - 4
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

        self.test_001_navigate_to_edp_and_open_top_finish_market_tab()
        self.test_002_verify_top_finish_market_headers()

        self.__class__.market_outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(self.market_outcomes,
                        msg=f'No combined market: "{vec.racing.TOP_FINISH_MARKET_NAME}" selections found')

        for outcome in self.market_outcomes.values():
            if outcome.bet_button.outcome_price_text != 'SP':
                self.assertRegexpMatches(outcome.bet_button.outcome_price_text, self.decimal_pattern,
                                         msg=f'Price value "{outcome.bet_button.outcome_price_text}" does '
                                             f'not match fractional pattern: "{self.decimal_pattern}"')

        self.test_004_verify_selections_ordering()
