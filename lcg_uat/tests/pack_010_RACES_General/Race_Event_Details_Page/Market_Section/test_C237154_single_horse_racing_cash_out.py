import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.prod
@pytest.mark.hl
# @pytest.mark.tst2  # not running on tst due to constant troubles with partial cashout appearance
# @pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.cash_out
@pytest.mark.ob_smoke
@pytest.mark.reg157_fix
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.login
@pytest.mark.portal_dependant
@vtest
class Test_C237154_Verify_Single_Horse_Racing_Successful_Full_Cash_Out(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C237154
    NAME: Verify Single Horse Racing Successful Full Cash Out process
    """
    keep_browser_open = True
    start_stake_amount = None
    expected_user_balance = None
    bet_info = None
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Horse Racing test event with Cash Out available
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

        event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                    additional_filters=cashout_filter)[0]
        self._logger.debug(f'*** Found Horseracing event "{event}"')
        start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                      ob_format_pattern=self.ob_format_pattern,
                                                      ss_data=True,
                                                      future_datetime_format=self.event_card_future_time_format_pattern)
        market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
        outcomes_resp = market['market']['children']
        self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id']
                                        for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}

        self.__class__.cashout_bet_name = f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - ' \
                                          f'[{event["event"]["name"]} {start_time_local}]'

    def test_001_login_to_oxygen_app(self):
        """
        DESCRIPTION: Login to Oxygen application
        """
        username = tests.settings.betplacement_user
        self.site.login(username=username)

    def test_002_add_selection_and_place_bet(self):
        """
        DESCRIPTION: Add Horse Racing test event selection, and place single bet
        EXPECTED: Bet was placed successful
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.__class__.bet_info = self.place_and_validate_single_bet()
        self.site.bet_receipt.footer.click_done()

    def test_003_navigate_to_cash_out_page(self):
        """
        DESCRIPTION: Navigate to Cash Out page
        EXPECTED: Test event cash out section is present
        """
        self.site.open_my_bets_cashout()
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.cashout_bet_name, list(bets.keys()),
                      msg=f'Bet "{self.cashout_bet_name}" is not present on Cash Out page '
                      f'among bets "{list(bets.keys())}"')

        self.__class__.bet = bets[self.cashout_bet_name]
        self.__class__.start_stake_amount = self.bet.stake.stake_value

    def test_004_perform_partial_cash_out(self):
        """
        DESCRIPTION: Perform partial cash out of test event
        EXPECTED: The success message is displayed instead of 'CASH OUT' button and slider
        EXPECTED: with the following information:
        EXPECTED:  - Green box with "tick" in a circle and message of "CASH OUT SUCCESSFUL" are shown below bet line details.
        EXPECTED:  - The icon and text are centered within green box.
        EXPECTED:  - Underneath the green box, another message is displayed:
        EXPECTED:  "Your Cash Out attempt was successful <currency symbol><value>."
        """
        user_balance = self.site.header.user_balance
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), msg='PARTIAL CASHOUT slider was not appeared')
        cashout_amount = self.bet.buttons_panel.partial_cashout_button.amount.value
        self._logger.info(f'*** Doing partial cashout, amount is: "{cashout_amount}"')
        self.bet.buttons_panel.wait_for_cashout_slider()
        try:
            self.bet.buttons_panel.partial_cashout_button.click()
        except VoltronException as e:
            if 'Can not click on PartialCashoutButton' in e:
                self.bet.buttons_panel.partial_cashout_button.click()
            pass
        confirmation_amount = self.bet.buttons_panel.cashout_button.amount.value
        self.assertEqual(cashout_amount, confirmation_amount,
                         msg=f'Amount on "confirmation" "{confirmation_amount}" '
                             f'and "partial cashout" button "{cashout_amount}" is not the same')
        self.bet.buttons_panel.cashout_button.click()
        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=expected_message, timeout=30),
                        msg=f'Message "{expected_message}" is not shown')
        self.__class__.expected_user_balance = float(user_balance) + float(cashout_amount)
        expected_stake_amount = '{0:.2f}'.format(round(float(self.start_stake_amount) * 0.5, 2))
        wait_for_result(lambda: self.bet.stake.stake_value != self.start_stake_amount,
                        name='Stake amount to update',
                        timeout=5)
        stake_amount = self.bet.stake.stake_value
        self.assertNotEqual(self.start_stake_amount, stake_amount,
                            msg=f'Stake amount: "{stake_amount}" was not updated')
        self.assertEqual(expected_stake_amount, stake_amount,
                         msg=f'\nStake amount: "{stake_amount}"'
                             f'\ndoes not match with required: "{expected_stake_amount}"')

    def test_005_check_balance_is_updated(self):
        """
        DESCRIPTION: Check balance is updated (previous value + cashout amount)
        """
        self.verify_user_balance(expected_user_balance=self.expected_user_balance)

    def test_006_perform_full_cash_out(self):
        """
        DESCRIPTION: Perform full cash out of test event
        DESCRIPTION: Check bet not displayed anymore
        EXPECTED: Test event cash out section is present
        EXPECTED: Bet disappeared after full cash out
        """
        cashout_amount = self.bet.buttons_panel.full_cashout_button.amount.value
        self.bet.buttons_panel.full_cashout_button.click()
        amount = self.bet.buttons_panel.cashout_button.amount.value
        self.assertEqual(cashout_amount, amount,
                         msg=f'Incorrect Cashout value "{cashout_amount}" instead of "{amount}"')
        self.bet.buttons_panel.cashout_button.click()
        self.__class__.expected_user_balance += float(cashout_amount)
        expected_message = vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=expected_message),
                        msg=f'Message "{expected_message}" is not shown')

    def test_007_check_balance_is_updated(self):
        """
        DESCRIPTION: Check balance is updated (previous value + cashout amount)
        """
        self.verify_user_balance(expected_user_balance=self.expected_user_balance)
