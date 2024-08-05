import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C1406196_Place_Horse_Racing_EW_Single_bet(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C1406196
    NAME: Place Horse Racing EW Single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single E/W bet on Horse Racing
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    PRECONDITIONS: Quick Bet should be deactivated (navigate to Menu -> Settings).
    """
    keep_browser_open = True
    expected_currency = '£'

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active events
        DESCRIPTION: Log in with a user that has a positive balance
        """
        if tests.settings.backend_env == 'prod':
            each_way_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=each_way_filter)[0]
            self.__class__.event_id = event['event']['id']
            market = next((market['market'] for market in event['event']['children']), None)
            if not market:
                raise SiteServeException('There are no available outcomes')
            self.__class__.event_name = event['event']['name']
            meeting_name = event['event']['typeName']
            self.__class__.event_off_time = self.get_date_time_formatted_string(
                date_time_obj=datetime.strptime(event['event']['startTime'], self.ob_format_pattern),
                time_format='%H:%M', hours=0)
            self._logger.info(f'*** Found RacingEvent "{self.event_name}" with time "{self.event_off_time}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
            self.__class__.event_id = event_params.event_id
            self.__class__.event_off_time = event_params.event_off_time
            self.__class__.event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            meeting_name = self.horseracing_autotest_uk_name_pattern
            self._logger.info(f'*** Created Racing Event "{self.event_name}" with time "{self.event_off_time}"')

        self.__class__.meeting_name = meeting_name if self.brand == 'ladbrokes' else meeting_name.upper()

        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id, query_builder=self.ss_query_builder)[0]
        event = resp['event']
        self.__class__.event_type_flag_codes = event['typeFlagCodes'].split(',')
        self.__class__.ew_coef = \
            int(event['children'][0]['market']['eachWayFactorNum']) / int(
                event['children'][0]['market']['eachWayFactorDen'])

        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance
        self.site.toggle_quick_bet()

    def test_001_navigate_to_horse_racing_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page from the Menu
        EXPECTED: Navigate to Horse Racing Page from the Menu
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_002_add_a_horse_racing_selection_to_bet_slip_eg_from_the_next_races_widget(self):
        """
        DESCRIPTION: Add a Horse racing selection to bet slip (e.g. from the "NEXT RACES" widget)
        EXPECTED: The selection is added to bet slip
        EXPECTED: The customer is automatically redirected to bet slip
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        sections_nw = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        section_nw_name, section_nw = list(sections_nw.items())[0]
        if section_nw_name:
            self.__class__.outcomes = section_nw.items_as_ordered_dict
            self.__class__.selection_name, selection = list(self.outcomes.items())[0]
            selection.bet_button.click()
            try:
                self.site.quick_bet_panel.close()
            except VoltronException:
                pass
            self.site.open_betslip()

    def test_003_add_a_stake_and_click_on_bet_now_button_or_place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£), tick the "Each Way" checkbox and then click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed
        EXPECTED: The currency is in £.
        """
        self.__class__.bet_info = self.place_and_validate_single_bet(
            number_of_stakes=1, each_way=True, ew_coef=self.ew_coef)

    def test_004_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet ID (if cashout is available for this event)
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        self.__class__.bet_receipt = self.site.bet_receipt
        bet_receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        single_section = bet_receipt_sections.get(vec.betslip.SINGLE)
        self.assertTrue(single_section, msg='No Single sections found')
        self.assertTrue(single_section.items_as_ordered_dict, msg='No stakes found in singles section')
        _, selection = list(single_section.items_as_ordered_dict.items())[0]

        # bet type as been removed for single bet
        # if self.brand != 'ladbrokes':
        #     bet_type = single_section.bet_type
        # else:
        #     bet_type = selection.type_name.text
        # self.assertEqual(bet_type, vec.betslip.SINGLE,
        #                  msg=f'Bet type is not the same as on betslip '
        #                      f'"{vec.betslip.SINGLE}" and is "{bet_type}"')
        self.assertEqual(selection.stake_currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{selection.stake_currency}" instead')
        self.assertEqual(selection.name, self.selection_name,
                         msg=f'Selection is not the same as on bet slip and equals "{selection.name}"'
                             f'instead of "{self.selection_name}"')
        self.__class__.expected_market_name = self.bet_info[self.selection_name]['market_name']
        self.assertEqual(selection.event_market, self.expected_market_name,
                         msg=f'Market name is not the same as on bet slip and equals "{selection.event_market}"'
                             f'instead of "{self.expected_market_name}"')
        self.assertTrue(selection.bet_id, msg='Bet ID is not displayed')

        self.verify_user_balance(expected_user_balance=float(self.user_balance) - float(self.bet_amount * 2))
        self.__class__.expected_odds = self.bet_info[self.selection_name]['odds']
        self.assertEqual(selection.odds, self.expected_odds, msg='Odds value is not the same as on Betslip')
        stake = selection.total_stake
        self.__class__.expected_stake = f'{(self.bet_amount * 2):.2f}'
        self.assertEqual(stake, self.expected_stake,
                         msg=f'Stake does not equal {self.expected_stake} and is {stake} instead')
        total_stake = self.bet_receipt.footer.total_stake
        betslip_total_stake = f'{self.bet_info["total_stake"]:.2f}'
        self.assertEqual(total_stake, betslip_total_stake,
                         msg=f'Total stake does not equal {betslip_total_stake} and is {total_stake} instead')

        est_returns = self.bet_receipt.footer.total_estimate_returns
        exp_est_returns = self.bet_info["total_estimate_returns"]
        self.__class__.betslip_est_returns = f'{exp_est_returns:.2f}' if exp_est_returns != 'N/A' else exp_est_returns

        self.verify_estimated_returns(est_returns=est_returns,
                                      odds=[selection.odds],
                                      each_way_coef=self.ew_coef,
                                      bet_amount=self.bet_amount)
        self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Bet receipt has no "Reuse Selection" button')
        self.assertTrue(self.bet_receipt.footer.has_done_button(), msg='Bet receipt has no "Done" button')

    def test_005_click_on_done_button(self):
        """
        DESCRIPTION: Click on Done button
        EXPECTED: The customer is redirected to Horse Racing Page
        """
        self.bet_receipt.footer.done_button.click()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_006_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_007_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: **Bet Receipt unique ID (only on settled bets tab )
        EXPECTED: Selection Details:
        EXPECTED: **Selection Name where the bet has been placed
        EXPECTED: **Event name and event off time
        EXPECTED: **Event time and date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms
        EXPECTED: **Correct Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed (for E/W);
        """
        bet_type = vec.bet_history.SINGLE_EACH_WAY_BET_TYPE
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, number_of_bets=1, event_names=self.event_name)
        currency = bet.stake.currency
        self.assertEqual(currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{currency}" instead')
        actual_bet_type = bet.bet_type
        self.assertIn(actual_bet_type, bet_type,
                      msg=f'Bet Type is not the same as expected "{bet_type}" and equals "{actual_bet_type}"')
        self.assertEqual(bet.selection_name, self.selection_name,
                         msg=f'Selection is not the same as on bet slip and equals "{bet.selection_name}"'
                             f' instead of "{self.selection_name}"')
        self.assertEqual(bet.odds_value, self.expected_odds, msg='Odds value is not the same as on Betslip')
        event_name = bet.event_name
        self.assertEqual(event_name.strip(), self.event_name.strip(),
                         msg=f'Event name is not the same as expected "{self.event_name.strip()}" and is "{event_name.strip()}"')
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'Bet: "{bet_name}" leg not found')
        event_time = next(i.event_time for i in bet_legs.values())
        self.assertTrue(event_time, msg='Event time is not displayed')
        market_name = bet.market_name
        self.assertIn(self.expected_market_name, market_name,
                      msg=f'Bet market name: "{market_name}" not contain expected: "{self.expected_market_name}"')
        stake_value = bet.stake.value.strip(self.expected_currency)
        self.assertEqual(stake_value, self.expected_stake,
                         msg=f'Stake does not equal "{self.expected_stake}" and is "{stake_value}" instead')
        self.verify_estimated_returns(est_returns=bet.est_returns.stake_value,
                                      odds=[bet.odds_value],
                                      each_way_coef=self.ew_coef,
                                      bet_amount=self.bet_amount)

    def test_008_click_on_user_menu_logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
