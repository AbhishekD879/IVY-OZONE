import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
# @pytest.mark.prod  As bet needs to be settled, cannot script it on prod.
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870306_Verify_void_bet_behaviour_for_HR_Place_a_bet_on_HR_and_settle_it_as_void_selection_verify_on_the_my_bets_settle_bet_and_bet_history(BaseBetSlipTest):
    """
    TR_ID: C44870306
    NAME: Verify 'void' bet behaviour for HR. (Place a bet on HR and settle it as void selection, verify on the my bets settle bet and bet history)
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Open bet configuration required
    """
    keep_browser_open = True
    bet_amount = 2  # to differentiate the user balance before and after betplacement

    def test_001_launch_the_appsite_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the app/site and login with valid Credentials
        EXPECTED: Successfully app launched and able to log in
        """
        self.site.login()
        self.site.wait_content_state('Homepage')
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_place_a_bet_on_hr(self):
        """
        DESCRIPTION: Place a bet on HR
        EXPECTED: placed bet successfully
        """
        event_params = self.ob_config.add_UK_racing_event()
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.market_id = event_params.market_id
        self.__class__.event_id = event_params.event_id
        self.__class__.event_name = event_params.ss_response['event']['name']

        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_003_void_the_bet_in_open_bet_and_check_the_status_in_my_bets_and_bet_history(self):
        """
        DESCRIPTION: 'Void' the bet in open bet and check the status in my bets and bet history
        EXPECTED: User should see the 'void'bet in my bets in settled tab and bet history
        """
        self.ob_config.update_selection_result(event_id=self.event_id, market_id=self.market_id,
                                               selection_id=self.selection_id, result='V')
        self.navigate_to_page(name='Homepage')
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name='HISTORY')
        self.site.wait_splash_to_hide(7)
        self.site.right_menu.click_item(item_name='Betting History')
        self.site.wait_content_state(state_name='BetHistory')
        self.site.close_all_dialogs(timeout=5)
        sleep(7)  # settled bet takes time to show on FE
        self.device.refresh_page()
        bets = self.site.bet_history.tab_content.accordions_list
        self.assertTrue(bets.items_as_ordered_dict, msg='No bets are available in settled bets tab')
        _, bet = bets.get_bet(bet_type='SINGLE', selection_ids=self.selection_id)
        settled_bet_status = bet.bet_status
        self.assertEqual(settled_bet_status, vec.betslip.CANCELLED_STAKE,
                         msg=f'Actual bet status: "{settled_bet_status}" is not same as Expected bet status: "{vec.betslip.CANCELLED_STAKE}"')

    def test_004_check_the_header_balance_update(self):
        """
        DESCRIPTION: Check the header balance update
        EXPECTED: Header balance should be updated
        """
        self.device.refresh_page()
        updated_balance = self.site.header.user_balance
        self.assertEqual(updated_balance, self.user_balance,
                         msg=f'Actual balance: "{updated_balance}" is not updated as Expected balance: "{self.user_balance}"')