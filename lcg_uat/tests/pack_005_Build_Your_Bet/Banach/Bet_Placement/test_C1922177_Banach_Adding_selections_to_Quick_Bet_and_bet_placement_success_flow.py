import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_build_your_bet
@pytest.mark.build_your_bet
@pytest.mark.back_button
@pytest.mark.build_your_bet_dashboard
@pytest.mark.bet_placement
@pytest.mark.banach
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.login
@vtest
@pytest.mark.issue("https://jira.egalacoral.com/browse/LCRCORE-22033")
class Test_C1922177_Banach_Adding_selections_to_Quick_Bet_and_bet_placement_success_flow(BaseBanachTest):
    """
    TR_ID: C1922177
    NAME: Banach. Successful bet placement and Bet receipt
    DESCRIPTION: Test case verifies successful Banach bet placement and Bet receipt
    PRECONDITIONS: CMS config:
    PRECONDITIONS: 1) Build Your Bet tab is available on Event Details Page :
    PRECONDITIONS: a) Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: b) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: c) Event belonging to Banach league is mapped (on Banach side)
    PRECONDITIONS: 2) Match Markets switcher is turned on : BYB > BYB switchers > enable Match Markets
    PRECONDITIONS: Requests:
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet:
    PRECONDITIONS: wss://remotebetslip-dev1.coralsports.dev.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket
    PRECONDITIONS: Build Your Bet tab on event details page is loaded and no selection added to dashboard
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 1
    currency = '£'
    all_selection_names = []
    blocked_hosts = ['*spark-br.*']
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Use request https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        # self.device.refresh_page()  # TODO w/a because of issue with loading of Banach markets for the first time EDP is opened, works after refresh
        # self.site.wait_splash_to_hide()

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that has enough funds to place a bet
        EXPECTED: User is logged in
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_002_add_a_few_selections_from_different_markets_to_dashboard(self):
        """
        DESCRIPTION: Add a few selections from different markets to dashboard
        EXPECTED: Selections are added to dashboard. Price and "Place bet" text are displayed on the button on the dashboard
        """
        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')

        match_betting_selection_names = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(), msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)

        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.__class__.summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary

        odds = self.summary_block.place_bet.value
        self.assertTrue(odds, msg='Can not get odds for given selections')

        self.assertEqual(self.summary_block.place_bet.text, vec.yourcall.PLACE_BET,
                         msg=f'Place bet button text: "{self.summary_block.place_bet.text}" '
                             f'is not the same as expected: "{vec.yourcall.PLACE_BET}"')

    def test_003_tap_on_the_place_bet_button_with_odds(self):
        """
        DESCRIPTION: Tap on the place bet button with odds
        EXPECTED: - In WS client sends message with code 50001 containing selections ids and receives message from quick bet with code 51001 with price
        EXPECTED: - On UI Betslip with price field and numeric keyboard appears
        """
        self.summary_block.place_bet.scroll_to()
        self.summary_block.place_bet.click()
        # self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
        #                  msg='Dashboard panel is displayed')
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip not appears')

        byb_betslip_panel = self.site.byb_betslip_panel
        selections = byb_betslip_panel.selection.content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in BYB betslip')
        self.__class__.all_selection_names = list(selections.keys())

        self.assertTrue(byb_betslip_panel.back_button.is_displayed(), msg='"BACK" button not displayed')
        self.assertTrue(byb_betslip_panel.place_bet.is_displayed(), msg='"PLACE BET" button not displayed')

        content = byb_betslip_panel.selection.content

        self.assertTrue(content.odds, msg='Odds value not found')
        self.assertTrue(content.amount_form.is_displayed(), msg='Amount input field not displayed')

    def test_004_enter_a_stake_and_tap_button_place_bet(self):
        """
        DESCRIPTION: Enter a stake and tap button "Place bet"
        DESCRIPTION: Verify channel used for BYB/Bet builder bets
        EXPECTED: - In WS client sends message with code 50011 containing price, stake, currency info and receives message with from quick bet with code 51101 containing "response code":1, bet id, receipt, stake.
        EXPECTED: Channel: "e" is present in '50011' request in 'remotebetslip' websocket
        EXPECTED: (Example:
        EXPECTED: betId:462764
        EXPECTED: betNo:1
        EXPECTED: betPotentialWin:"11.0"
        EXPECTED: date:"0001-01-01T00:00:00" - is not used
        EXPECTED: numLines:1
        EXPECTED: receipt:
        EXPECTED: "O/0196666/0000113"
        EXPECTED: totalStake:
        EXPECTED: "2.0")
        EXPECTED: - On UI bet receipt is displayed
        """
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)
        self.site.byb_betslip_panel.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                        msg='Build Your Bet Receipt is not displayed')

        request = wait_for_result(lambda: self.get_web_socket_response_by_id(response_id=self.response_51101, delimiter='42'),
                                  name=f'WS message with code {self.response_51101} to appear',
                                  timeout=45,
                                  poll_interval=1)

        self.assertTrue(request, msg=f'Response with frame ID #{self.response_51101} not received')
        self._logger.debug(f'*** Request data "{request}" for "{self.response_51101}"')

        response_50011 = wait_for_result(
            lambda: self.get_web_socket_response_by_id(response_id=self.response_50011, delimiter='42'),
            name=f'WS message with code {self.response_50011} to appear',
            timeout=30,
            poll_interval=1)
        self.assertTrue(response_50011, msg=f'Response with frame ID #{self.response_50011} not received')
        self.assertEqual(response_50011.get('channel'), 'e',
                         msg=f'Channel: "e" is not present in "{self.response_50011}" request among "{response_50011}"')

    def test_005_verify_bet_receipt_on_ui(self):
        """
        DESCRIPTION: Verify Bet receipt on UI
        EXPECTED: Bet receipt contains correct info for the following items:
        EXPECTED: - Title Bet receipt
        EXPECTED: - Names of markets with selections
        EXPECTED: - Odds
        EXPECTED: - Bet id
        EXPECTED: - Total Stake and Total Est. Returns
        """
        bet_receipt_selection = self.site.byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in Build Your Bet receipt')

        selection_keys = list(selections.keys())
        expected_selection_keys = self.all_selection_names
        self.assertListEqual(selection_keys, expected_selection_keys,
                             msg=f'Incorrect market names.\nActual list: {selection_keys}'
                             f'\nExpected list: {expected_selection_keys}')
        self.assertTrue(bet_receipt_content.odds, msg='Odds value not found')

        self.assertEqual(bet_receipt_content.bet_id_label, vec.betslip.BET_ID,
                         msg=f'Bet id label text is: "{bet_receipt_content.bet_id_label}" expecting "{vec.betslip.BET_ID}"')
        self.assertTrue(bet_receipt_content.bet_id_value, msg='Bet ID value not found')

        self.assertEqual(bet_receipt_selection.total_stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg=f'Total Stake label text is: "{bet_receipt_selection.total_stake_label}", '
                             f'instead of "{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}"')
        self.assertIn(self.currency, bet_receipt_selection.total_stake)
        self.assertEqual(float(bet_receipt_selection.total_stake_value), self.bet_amount,
                         msg=f'Actual Total Stake value: "{float(bet_receipt_selection.total_stake_value)}" '
                             f'not match with expected: "{self.bet_amount}"')
        self.assertEqual(bet_receipt_selection.total_est_returns_label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Total Est. Returns label text is: "{bet_receipt_selection.total_est_returns_label}", '
                             f'instead of "{vec.bet_history.TOTAL_RETURN}"')
        self.assertIn(self.currency, bet_receipt_selection.total_est_returns)
        self.assertTrue(bet_receipt_selection.total_est_returns_value, msg='Total Est. Returns value not found')

    def test_006_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet receipt
        EXPECTED: Bet receipt is removed
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')
