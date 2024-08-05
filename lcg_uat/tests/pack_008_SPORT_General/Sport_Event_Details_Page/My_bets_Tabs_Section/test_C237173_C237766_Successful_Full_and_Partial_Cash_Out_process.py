import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.crl_tst2  # Coral only, partial CashOut shouldn't be executed on non-prod envs
# @pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C237173_C237766_Successful_Full_and_Partial_Cash_Out_process(BaseCashOutTest):
    """
    TR_ID: C237173
    TR_ID: C237766
    NAME: Verify Successful Full and Partial Cash Out process
    """
    keep_browser_open = True
    bet_amount = 3

    def test_001_create_event(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id, all_available_events=True)
        self.__class__.selection_id = None
        for event in events:
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                continue
            else:
                self._logger.debug(f'*** Football event with event id "{self.eventID}" and team "{self.team1}"')
                selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                self.__class__.selection_id = selection_ids[self.team1]
                break

        if not self.selection_id:
            raise SiteServeException('Unable to get Selection Id for Football Event')

    def test_002_login_to_application(self):
        """
        DESCRIPTION: Login to application
        """
        username = tests.settings.betplacement_user

        self.site.login(username=username)

    def test_003_place_bet_for_events(self):
        """
        DESCRIPTION: Place bet for test event
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_004_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.eventID)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_005_tap_on_partial_cash_out_button(self):
        """
        DESCRIPTION: Tap on 'Partial CashOut' button
        EXPECTED: 'Partial CashOut' slider is appear
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.__class__.bet_name, self.__class__.bet = self.site.sport_event_details.my_bets.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.team1, number_of_bets=1)
        self.__class__.start_cashout_amount = self.bet.buttons_panel.full_cashout_button.amount.value
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), msg='PARTIAL CASHOUT slider was not appeared')

    def test_006_trigger_successful_partial_cash_out(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button for default 50% partial cash out value
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Green box with "tick" in a circle and message of "SUCCESSFUL CASH OUT <currency symbol><value>" are shown below bet line details. The icon and text are centered within green box.
        EXPECTED: * Underneath the green box, another message is displayed: "Your Cash Out
        EXPECTED: Stake and Est. Returns values are decreased within bet accordion and bet line, new values are shown
        """
        start_est_returns_amount = self.bet.est_returns.stake_value
        cashout_amount = float(self.bet.buttons_panel.partial_cashout_button.amount.value)

        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        success_message = vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=success_message, timeout=10),
                        msg=f'Message "{success_message}" was not shown')

        self.verify_user_balance(expected_user_balance=self.user_balance + cashout_amount)

        expected_est_returns = '{0:.2f}'.format(round(float(start_est_returns_amount) * 0.5, 2))
        expected_cash_out_amount = '£{0:.2f}'.format(round(float(self.start_cashout_amount) * 0.5, 2))
        actual_est_returns = f'{self.bet.est_returns.stake_value}'
        self.assertAlmostEqual(float(actual_est_returns), float(expected_est_returns), delta=0.011,
                               msg=f'Bet: "{self.bet_name}" estimated returns: "{actual_est_returns}" '
                               f'does not match with expected: "{expected_est_returns}" within delta: "{0.011}"')

        end_cashout_amount = str(self.bet.buttons_panel.full_cashout_button.amount)
        self.assertEqual(end_cashout_amount, expected_cash_out_amount,
                         msg=f'Bet: "{self.bet_name}" Cash Out value after partial cash out is: '
                             f'"{end_cashout_amount}", expected: "{expected_cash_out_amount}"')

    def test_007_trigger_successful_full_cash_out(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' and 'Partial CashOut' buttons with the following information:
        EXPECTED: * Green box with "tick" in a circle and message of "SUCCESSFUL CASH OUT <currency symbol><value>" are shown below bet line details. The icon and text are centered within green box.
        EXPECTED: Once the success message completely fades out at the same time the bet is removed from the 'My Bets' tab
        """
        self.__class__.user_balance = self.site.header.user_balance
        cashout_amount = float(self.bet.buttons_panel.full_cashout_button.amount.value)
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        success_message = vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=success_message, timeout=10),
                        msg=f'Message "{success_message}" was not shown')
        self.verify_user_balance(expected_user_balance=self.user_balance + cashout_amount)

        result = wait_for_result(lambda:
                                 self.site.sport_event_details.my_bets.accordions_list.get_bet(
                                     bet_type='SINGLE',
                                     event_names=self.team1)[1].buttons_panel.has_full_cashout_button(),
                                 expected_result=False,
                                 name=f'Bet: "{self.bet_name}" Cashout Panel disappears',
                                 timeout=5)
        self.assertFalse(result, msg=f'Bet: "{self.bet_name}" Cashout Panel still displayed after Full cash out')
