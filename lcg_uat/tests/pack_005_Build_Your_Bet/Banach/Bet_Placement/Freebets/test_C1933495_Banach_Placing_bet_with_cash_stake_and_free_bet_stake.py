import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec
from random import uniform


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod no user with freebet tokens on prod
# @pytest.mark.crl_hl
@pytest.mark.build_your_bet
@pytest.mark.bet_placement
@pytest.mark.banach
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C1933495_Banach_Placing_bet_with_cash_stake_and_free_bet_stake(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C1933495
    NAME: Banach Placing bet with cash stake and free bet stake
    DESCRIPTION: Test case verifies successful Banach bet placement using freebet and cash stake
    PRECONDITIONS: Banach free bets tokens - a standard offer with default sportsbook token reward should be configured and active, with all channels ticked- it will include new Banach OB channels. Ahhoc tokens with default offer ID will not work for Banach bets. Only adhoc tokens created with associated Banach offer as mentioned above.
    PRECONDITIONS: [To add freebet to user account][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: To check Odds value: Network tab -> price request
    PRECONDITIONS: **User has added at least two combinable selections to BYB Dashboard***
    PRECONDITIONS: **User has selected Banach free bet and entered cash stake on Betslip**
    """
    keep_browser_open = True
    bet_amount = 0.5
    currency = '£'
    default_freebets_message = vec.sb.FREE_BETS_AVAILABLE
    proxy = None
    freebet_value = f'{uniform(4, 5):.2f}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as user that has freebets
        DESCRIPTION: Find event with Banach markets
        DESCRIPTION: Add two combinable selections to BYB Dashboard
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market()

        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value)

        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance

        self.navigate_to_edp(event_id=self.event_id, timeout=50)
        # self.device.refresh_page() # TODO w/a because of issue with loading of Banach markets for the first time EDP is opened, works after refresh
        # self.site.wait_splash_to_hide()
        # self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting,
                                            selection_index=0)
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.both_teams_to_score,
                                            selection_name='Yes')

        summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        summary_block.place_bet.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='BYB Dashboard panel is displayed')
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip is not shown')

        byb_betslip_panel = self.site.byb_betslip_panel.selection.content

        byb_betslip_panel.amount_form.enter_amount(value=self.bet_amount)

        self.assertTrue(byb_betslip_panel.has_use_free_bet_link(), msg='"Use Free Bet" link is not present')

        byb_betslip_panel.use_free_bet_link.click()
        self.__class__.selected_freebet_value = self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))

        self.__class__.expected_total_stake = self.bet_amount + float(self.selected_freebet_value)

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap PLACE BET button
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - User balance is updated
        """
        self.site.byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=15),
                        msg='BYB Bet Receipt is not displayed')

        request = wait_for_result(lambda: self.get_web_socket_response_by_id(response_id=self.response_51101,
                                                                             delimiter='42'),
                                  name=f'WS message with code {self.response_51101} to appear',
                                  timeout=25,
                                  poll_interval=1)
        self.assertTrue(request, msg=f'Response with frame ID #{self.response_51101} not received')
        self._logger.debug(f'*** Request data "{request}" for "{self.response_51101}"')

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=15),
                        msg='BYB Bet Receipt is not displayed')

        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount)

    def test_002_verify_channel_used_for_byb_bet_builder_bets(self):
        """
        DESCRIPTION: Verify channel used for BYB/Bet builder bets
        EXPECTED: Channel: "e" is present in '50011' request in 'remotebetslip' websocket
        """
        response = wait_for_result(
            lambda: self.get_web_socket_response_by_id(response_id=self.response_50011, delimiter='42'),
            name=f'WS message with code {self.response_50011} to appear',
            timeout=30,
            poll_interval=1)
        self.assertTrue(response, msg=f'Response with frame ID #{self.response_50011} not received')
        self.assertEqual(response.get('channel'), 'e',
                         msg=f'Channel: "e" is not present in "{self.response_50011}" request among "{response}"')

    def test_003_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet receipt
        EXPECTED: Bet receipt contains correct info for the following items:
        EXPECTED: - Title Bet receipt
        EXPECTED: - Names of markets with selections
        EXPECTED: - Odds
        EXPECTED: - Bet id
        EXPECTED: - Freebet stake
        EXPECTED: - Total Stake (Free bet + Cash stake) and Total Est. Returns
        EXPECTED: - buttons "Reuse selection" and "Done"
        """
        bet_receipt_selection = self.site.byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in Build Your Bet receipt')
        self.assertTrue(bet_receipt_content.odds, msg='Odds value not found')

        self.assertEqual(bet_receipt_content.bet_id_label, vec.betslip.BET_ID,
                         msg=f'Bet id label "{bet_receipt_content.bet_id_label}" '
                             f'is not the same as expected "{vec.betslip.BET_ID}"')
        self.assertTrue(bet_receipt_content.bet_id_value, msg='Bet ID value not found')

        self.assertEqual(bet_receipt_selection.total_stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg=f'Total Stake label "{bet_receipt_selection.total_stake_label}" '
                             f'is not the same as expected "{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}"')
        self.assertIn(self.currency, bet_receipt_selection.total_stake)

        total_stake = float(bet_receipt_selection.total_stake_value) + float(bet_receipt_selection.freebet_stake_value)
        self.assertEqual(total_stake, self.expected_total_stake,
                         msg=f'Actual Total Stake value: "{total_stake}" does '
                             f'not match with expected: "{self.expected_total_stake}"')
        self.assertEqual(bet_receipt_selection.total_est_returns_label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Total Est. Returns label "{bet_receipt_selection.total_est_returns_label}" '
                             f'is not the same as expected "{vec.bet_history.TOTAL_RETURN}"')
        self.assertIn(self.currency, bet_receipt_selection.total_est_returns)
        self.assertTrue(bet_receipt_selection.total_est_returns_value, msg='Total Est. Returns value not found')

        self.assertTrue(bet_receipt_selection.has_freebet_icon(), msg='No FB icon present')
        self.assertIn(self.currency, bet_receipt_selection.freebet_stake.text)
        self.assertEqual(bet_receipt_selection.freebet_stake_value, self.selected_freebet_value,
                         msg=f'Actual Free Bet Stake value: "{bet_receipt_selection.freebet_stake_value}" '
                             f'not match with expected: "{self.selected_freebet_value}"')

    def test_004_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet receipt
        EXPECTED: Bet receipt is removed
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')
