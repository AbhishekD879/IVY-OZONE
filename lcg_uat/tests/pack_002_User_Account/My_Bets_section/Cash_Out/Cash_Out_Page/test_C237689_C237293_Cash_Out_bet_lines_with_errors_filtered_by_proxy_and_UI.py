import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.medium
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.slow
@pytest.mark.timeout(1000)
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-47840')   # Ladbrokes dev0 BPP
class Test_C237689_C237293_Cash_Out_bet_lines_with_errors_filtered_by_proxy_and_UI(BaseCashOutTest):
    """
    TR_ID: C237689
    TR_ID: C237293
    VOL_ID: C9697911
    NAME: Cash Out bet lines with errors filtered by proxy and UI
    DESCRIPTION: Place Single and Multiple bets with available cash out
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Single and Multiple bets with available cash out
    """
    keep_browser_open = True
    events = None
    created_event_name, created_event_name2 = None, None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place Single and Multiple bets with available cash out
        """
        # Verify CashOut tab configuration in CMS
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')

        self.__class__.events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        selection_ids = [event.selection_ids[event.team1] for event in self.events]
        self.__class__.created_event_name = '%s %s' % (self.events[0].event_name, self.events[0].local_start_time)
        self.__class__.created_event_name2 = '%s %s' % (self.events[1].event_name, self.events[1].local_start_time)
        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash out' tab has opened
        """
        self.site.open_my_bets_cashout()

    def test_002_suspend_event(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashoutValue: "CASHOUT_LINE_SUSPENDED" in **getbetDetail** response for **Single** Cash Out bet
        DESCRIPTION: (Suspend event or market or selection for event with placed bet)
        """
        self.ob_config.change_event_state(event_id=self.events[0].event_id)

    def test_003_verify_event_with_placed_bet(self):
        """
        DESCRIPTION: Verify events for placed Single and Multiple bets
        EXPECTED: The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: *   Message of **CASH OUT SUSPENDED** is shown below bet line details.
        """
        bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=5)
        self.assertFalse(single_bet.buttons_panel.cashout_button.is_enabled(expected_result=False),
                         msg='Cash Out button is not disabled')

        cashout_suspended = single_bet.buttons_panel.cashout_button.label
        self.assertEqual(cashout_suspended, vec.bet_history.CASHOUT_BET.cash_out_bet_suspended,
                         msg=f'Actual message: "{cashout_suspended}", is not the same '
                             f'as expected: "{vec.bet_history.CASHOUT_BET.cash_out_bet_suspended}"')

        event_names = [self.created_event_name, self.created_event_name2]
        bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=event_names)
        self.assertFalse(multiple_bet.buttons_panel.cashout_button.is_enabled(expected_result=False),
                         msg='Cash Out button is not disabled')

        not_available_message = multiple_bet.buttons_panel.cashout_button.label
        self.assertEqual(not_available_message, vec.bet_history.CASHOUT_BET.cash_out_bet_suspended,
                         msg=f'Actual message: "{not_available_message}", is not the same '
                             f'as expected: "{vec.bet_history.CASHOUT_BET.cash_out_bet_suspended}"')

    def test_004_navigate_to_another_page_and_return_back_to_cash_out_tab_on_my_bets_page_or_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to another page and return back to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * Single bet is shown with the same error message as in step #3
        EXPECTED: * cashoutValue: "CASHOUT_SELN_SUSPENDED" is received in **getbetDetails** response
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')
        self.test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget()
        self.test_003_verify_event_with_placed_bet()

    def test_005_in_ob_backoffice_unsuspend_event(self):
        """
        DESCRIPTION: In OB Backoffice unsuspend event
        EXPECTED: 'CASH OUT' button and slider are shown under bet details instead of error message
        """
        self.ob_config.change_event_state(event_id=self.events[0].event_id, active=True, displayed=True)

        bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.assertTrue(single_bet.buttons_panel.full_cashout_button.is_enabled(),
                        msg='Full Cash Out button is not enabled')

        event_names = [self.created_event_name, self.created_event_name2]
        bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=event_names, number_of_bets=5)
        self.assertTrue(multiple_bet.buttons_panel.full_cashout_button.is_enabled(),
                        msg='Full Cash Out button is not enabled')

    def test_006_disable_cashout_for_event(self):
        """
        DESCRIPTION: Disable cashout for event
        """
        event = self.events[0]
        self.ob_config.change_event_cashout_status(event_id=event.event_id, cashout_available=False)

    def test_007_wait_5_seconds(self):
        """
        DESCRIPTION: Wait 5 seconds
        EXPECTED: Bet disappears from the 'Cash Out' tab
        """
        sleep(6)  # +1 second because on 5th second those bets actually are in progress of disappearing

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type == 'desktop':
            self.site.wait_content_state('Homepage', timeout=30)
            self.site.open_my_bets_cashout()

        single_bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
            raise_exceptions=False,
            number_of_bets=5)

        event_names = [self.created_event_name, self.created_event_name2]
        multiple_bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=event_names, raise_exceptions=False)

        if self.is_cashout_tab_enabled:
            self.assertFalse(single_bet,
                             msg=f'Event: "{self.created_event_name}" single Bet is shown on Cashout page')
            self.assertFalse(multiple_bet, msg='Multiple Bet is shown on Cashout page')
        else:
            self.assertTrue(single_bet,
                            msg=f'Event: "{self.created_event_name}" single Bet is not shown on Cashout page')
            self.assertFalse(single_bet.buttons_panel.has_full_cashout_button(expected_result=False),
                             msg=f'Full Cash Out button is enabled for event "{self.created_event_name}"')

            self.assertTrue(multiple_bet, msg='Multiple Bet is not shown on Cashout page')
            self.assertFalse(multiple_bet.buttons_panel.has_full_cashout_button(expected_result=False),
                             msg='Full Cash Out button is enabled')
