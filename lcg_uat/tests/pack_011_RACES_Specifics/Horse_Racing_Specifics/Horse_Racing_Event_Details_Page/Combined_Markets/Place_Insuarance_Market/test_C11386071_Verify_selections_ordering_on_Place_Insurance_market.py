import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec


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
class Test_C11386071_Verify_selections_ordering_on_Place_Insurance_market(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C11386071
    NAME: Verify selections ordering on 'Place Insurance' market
    DESCRIPTION: This test case verifies selections ordering on 'Place Insurance' market
    PRECONDITIONS: 1) Horse Racing events with 'Place Insurance': '2ND'/ 3RD / 4TH' markets (templateMarketName='Insurance 2 Places', templateMarketName="Insurance 3 Places", templateMarketName="Insurance 4 Places") are available
    PRECONDITIONS: 2) To observe LiveServe changes make sure:
    PRECONDITIONS: - LiveServ updates is checked on 'Class' and 'Type' levels in TI
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: 3) To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [
        ('insurance_2_places',),
        ('insurance_3_places',),
        ('insurance_4_places',)
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

    def test_001_navigate_to_edp_and_open_place_insurance_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'Place Insurance' market tab
        EXPECTED: 'Place Insurance' market tab is opened
        """
        self.__class__.tab_name = vec.sb.INSURANCE_MARKETS
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertIn(self.tab_name, market_tabs.keys(),
                      msg=f'"{self.tab_name}" tab was not found in the tabs list "{market_tabs.keys()}"')

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)

    def test_002_verify_place_insurance_market_headers(self):
        """
        DESCRIPTION: Verify 'Place Insurance' market headers
        EXPECTED: 2ND 3RD 4TH 'Place Insurance' market headers are displayed
        """
        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertIn(self.tab_name, event_markets_list,
                      msg=f'"{self.tab_name}" market was not found')

        self.__class__.event_market = event_markets_list[self.tab_name]
        market_headers = self.event_market.section_header.items_as_ordered_dict

        self.assertTrue(market_headers, msg='No market headers found')

        self.softAssert(self.assertListEqual, list(market_headers.keys()), vec.racing.PLACE_INSURANCE_FIXTURE_HEADERS,
                        msg=f'Market headers "{list(market_headers.keys())}" are not the same '
                        f'as expected "{vec.racing.PLACE_INSURANCE_FIXTURE_HEADERS}"')

    def test_003_verify_selections(self):
        """
        DESCRIPTION: Verify selections
        EXPECTED: * Available selections are displayed in the grid, odds of each are shown in correct market section (2ND, 3RD, 4TH)
        EXPECTED: * Selection name, runner number, silks and trainer are displayed for each selection (if available)
        EXPECTED: * If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: * Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        """
        self.__class__.market_outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(self.market_outcomes,
                        msg=f'No combined market: "{self.tab_name}" selections found')

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
        EXPECTED: * Selections are ordered by odds in first available market (e.g. 2ND/3RD/4TH) in ascending order (lowest to highest)
        EXPECTED: If odds of selections are the same -> display by runnerNumber (in ascending order)
        EXPECTED: If prices are absent for selections - display by runnerNumber (in ascending order)
        """
        runner_numbers = []
        for outcome_name, outcome in self.market_outcomes.items():
            runner_numbers.append(outcome.runner_number)

        self.softAssert(self.assertEqual, runner_numbers, self.expected_runners_order,
                        msg=f'Runners order "{runner_numbers}" is not the same '
                        f'as expected "{self.expected_runners_order}"')

    def test_005_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_1___4(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 1 - 4
        EXPECTED:
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

        self.test_001_navigate_to_edp_and_open_place_insurance_market_tab()
        self.test_002_verify_place_insurance_market_headers()

        self.__class__.market_outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(self.market_outcomes,
                        msg=f'No combined market: "{self.tab_name}" selections found')

        for outcome in self.market_outcomes.values():
            if outcome.bet_button.outcome_price_text != 'SP':
                self.assertRegexpMatches(outcome.bet_button.outcome_price_text, self.decimal_pattern,
                                         msg=f'Price value "{outcome.bet_button.outcome_price_text}" does '
                                             f'not match fractional pattern: "{self.decimal_pattern}"')

        self.test_004_verify_selections_ordering()
