import pytest
import tests
from datetime import datetime
from tests.base_test import vtest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.mobile_only
@pytest.mark.login
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.each_way
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C874314_Place_Horse_Racing_Single_bet(BaseRacing, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C874314
    VOL_ID: C46795215
    NAME: Place Horse Racing Single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single E/W bet on Horse Racing
    """
    keep_browser_open = True
    has_cash_out_label = False
    expected_currency = '£'

    def get_event_win_e_w_market(self, events):
        for event in events:
            if next((market.get('market') for market in event['event']['children']
                     if market.get('market', {}).get('isEachWayAvailable') == 'true' and market.get('market', {}).get('templateMarketName') == 'Win or Each Way'), None):
                return event

        raise SiteServeException('No events with "Win or Each Way" market and "isEachWayAvailable"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Quick Bet should be deactivated (navigate to Menu -> Settings).
        PRECONDITIONS: NOTE:
        PRECONDITIONS: **to be verified manually
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            self.__class__.eventID = event_params.event_id
            self.__class__.event_name = self.horseracing_autotest_uk_name_pattern \
                if self.brand == 'ladbrokes' else self.horseracing_autotest_uk_name_pattern.upper()
            self.__class__.event_off_time = event_params.event_off_time
            self._logger.info(f'*** Created Event "{self.event_name}" with time "{self.event_off_time}"')
        else:
            each_way_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            events = self.get_active_events_for_category(category_id=self.category_id,
                                                         additional_filters=each_way_filter,
                                                         all_available_events=True)
            event = self.get_event_win_e_w_market(events)
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = event['event']['name']
            self.__class__.event_off_time = self.get_date_time_formatted_string(
                date_time_obj=datetime.strptime(event['event']['startTime'], self.ob_format_pattern),
                time_format='%H:%M', hours=0)
            self._logger.info(
                f'*** Found Event "{self.event_name}" with ID "{self.eventID}" with time "{self.event_off_time}"')

        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, query_builder=self.ss_query_builder)[0]
        event = resp['event']
        self.__class__.event_type_flag_codes = event['typeFlagCodes'].split(',')
        self.__class__.meeting_name = event['typeName'].upper() if self.brand != 'ladbrokes' else event['typeName']
        e_w_market = next((market.get('market') for market in event['children']
                           if market.get('market', {}).get('isEachWayAvailable') == 'true' and
                           market.get('market', {}).get('templateMarketName') == 'Win or Each Way'), None)
        if not e_w_market:
            raise SiteServeException('E/W Market was not found')

        self.__class__.ew_coef = self.calculate_each_way_coef(e_w_market)

        self.site.login()
        self.__class__.initial_user_balance = self.site.header.user_balance
        self.site.toggle_quick_bet()

    def test_001_navigate_to_horse_racing_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page from the Menu
        EXPECTED: Navigate to Horse Racing Page from the Menu
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        if self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()

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
            selection_name, selection = list(self.outcomes.items())[0]
            selection.bet_button.click()
            try:
                self.site.quick_bet_panel.close()
            except VoltronException:
                pass
            self.site.open_betslip()

    def test_003_add_a_stake_and_click_on_bet_now_button_or_place_bet_button(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£), click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed
        EXPECTED: The currency is in £.
        """
        if self.site.cookie_banner:
            self.site.cookie_banner.ok_button.click()

        self.__class__.initial_user_balance = self.site.header.user_balance
        section = self.get_betslip_sections().Singles
        _, selection = list(section.items())[0]
        selection.amount_form.input.value = self.bet_amount
        self.assertTrue(selection.has_each_way_checkbox(), msg='Each way checkbox is absent.')
        selection.each_way_checkbox.click()

        self.__class__.betslip_estimated_returns = selection.est_returns
        self.__class__.betslip_selection_name = selection.outcome_name
        self.__class__.betslip_market_name = selection.market_name
        self.__class__.betslip_odds = selection.odds
        self.__class__.betslip_event_name = selection.event_name
        # self.__class__.betslip_bet_type = section.name

        self.__class__.betslip_total_stake = self.get_betslip_content().total_stake
        self.__class__.betslip_currency = self.get_betslip_content().total_stake_currency
        place_bet_button = self.get_betslip_content().bet_now_button

        self.assertEqual(self.betslip_currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{self.betslip_currency}" instead.')
        self.assertTrue(self.get_betslip_content().has_bet_now_button(), msg='Place Bet button is not present.')
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()

        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed.')

    def test_004_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: Single);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet ID (if cashout is available for this event)
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        self.__class__.bet_receipt = self.site.bet_receipt
        bet_receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found.')
        single_section = bet_receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section, msg='No Single sections found.')
        self.assertTrue(single_section.items_as_ordered_dict, msg='No stakes found in singles section.')
        _, selection = list(single_section.items_as_ordered_dict.items())[0]

        # single had been removed from the recipient
        # if self.brand != 'ladbrokes':
        #     bet_type = single_section.bet_type
        #     self.assertEqual(bet_type, self.betslip_bet_type,
        #                      msg=f'Bet type is not the same as on betslip "{self.betslip_bet_type}" and is "{bet_type}"')
        # else:
        #     bet_type = selection.type_name.text
        #     self.assertIn(bet_type, self.betslip_bet_type,
        #                   msg=f'Bet type is not the same as on betslip "{self.betslip_bet_type}" and is "{bet_type}"')
        currency = selection.stake_currency
        self.assertEqual(currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{currency}" instead.')
        selection_name = selection.name
        self.assertEqual(selection_name, self.betslip_selection_name,
                         msg=f'Selection is not the same as on bet slip and equals "{selection_name}"'
                             f'instead of "{self.betslip_selection_name}". ')
        market_name = selection.event_market
        self.assertEqual(market_name, self.betslip_market_name,
                         msg=f'Market name is not the same as on bet slip and equals "{market_name}"'
                             f'instead of "{self.betslip_market_name}". ')
        if self.has_cash_out_label:
            self.assertTrue(selection.cash_out_label.is_displayed(), msg='Cash Out label is not displayed.')
        self.assertTrue(selection.bet_id, msg='Bet ID is not displayed.')

        self.verify_user_balance(expected_user_balance=float(self.initial_user_balance) - float(self.bet_amount * 2),
                                 delta=0.03)
        self.assertEqual(selection.odds, self.betslip_odds, msg='Odds value is not the same as on bet slip.')
        stake = selection.total_stake
        self.__class__.expected_stake = f'{(self.bet_amount * 2):.2f}'
        self.assertEqual(stake, self.expected_stake,
                         msg=f'Stake does not equal "{self.expected_stake}" and is "{stake}" instead.')
        total_stake = self.bet_receipt.footer.total_stake
        self.assertEqual(total_stake, self.expected_stake,
                         msg=f'Total stake does not equal "{self.expected_stake}" and is "{total_stake}" instead.')

        est_returns = self.bet_receipt.footer.total_estimate_returns
        self.assertTrue(est_returns, msg=f'Estimated returns are not displayed')
        self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Bet receipt has no "Reuse Selection" button.')
        self.assertTrue(self.bet_receipt.footer.has_done_button(),
                        msg='Bet receipt has no "Done" button.')

    def test_005_click_on_done_button(self):
        """
        DESCRIPTION: Click on Done button
        EXPECTED: The customer is redirected to Horse Racing Page - User is redirected to homepage because selection was added via deep link
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
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: **Event name and event off time
        EXPECTED: **Event time and date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **Correct Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed (In case if Total stake and Stake values are different);
        """
        bet_type = vec.bet_history.SINGLE_EACH_WAY_BET_TYPE
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, number_of_bets=1)
        currency = bet.stake.currency
        self.assertEqual(currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{currency}" instead.')
        actual_bet_type = bet.bet_type
        self.assertIn(actual_bet_type, bet_type,
                      msg=f'Bet Type is not the same as expected "{bet_type}"'
                          f' and equals "{actual_bet_type}". ')

        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No bet legs found for bet: "{bet_name}"')
        betleg_name, betleg = list(bet_legs.items())[0]
        selection_name = betleg.outcome_name
        self.assertEqual(selection_name, self.betslip_selection_name,
                         msg=f'Selection is not the same as on bet slip and equals "{selection_name}"'
                             f' instead of "{self.betslip_selection_name}". ')
        self.assertEqual(betleg.odds_value, self.betslip_odds, msg='Odds value is not the same as on bet slip.')
        event_name = bet.event_name
        self.assertIn(event_name, self.betslip_event_name,
                      msg=f'Event name is not the same as on betslip "{self.betslip_event_name}" and is "{event_name}".')
        self.assertTrue(betleg.event_start_time, msg='Event start time is not displayed.')
        market_name = betleg.market_name
        self.assertIn(self.betslip_market_name, market_name,
                      msg=f'Market name is not the same as on bet slip and equals "{market_name}"'
                          f' instead of "{self.betslip_market_name}".')
        stake = bet.stake.stake_value
        self.assertEqual(stake, self.expected_stake,
                         msg=f'Stake does not equal "{self.expected_stake}" and is "{stake}" instead.')
        est_returns = bet.est_returns.stake_value
        self.verify_estimated_returns(est_returns=est_returns, odds=self.betslip_odds, bet_amount=self.bet_amount,
                                      delta=0.1, each_way_coef=self.ew_coef)

    def test_008_click_on_user_menu_logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
