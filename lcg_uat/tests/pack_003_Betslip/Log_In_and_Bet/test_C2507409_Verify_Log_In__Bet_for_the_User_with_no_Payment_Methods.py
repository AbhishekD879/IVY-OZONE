import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.lad_tst2  # this test case marked as not up to date
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.medium
@vtest
class Test_C2507409_Verify_Log_In_Bet_for_the_User_with_no_Payment_Methods(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C2507409
    NAME: Verify 'Log In & Bet' for the User with no Payment Methods
    PRECONDITIONS: Make sure you have user account with:
    PRECONDITIONS: No payment methods with 0/or insufficient balance
    """
    # TODO adapt for vanilla once story related to BMA-48323 will be completed
    keep_browser_open = True

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        """
        self.__class__.username = tests.settings.user_has_no_pm_0_balance
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection = next((outcome['outcome']['name'] for outcome in outcomes if
                                             outcome['outcome'].get('outcomeMeaningMinorCode') and
                                             outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.selection:
                raise SiteServeException('No Home team found')
            self._logger.info(f'*** Found Football event with selection ids "{self.selection_ids}" and team "{self.selection}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection, self.__class__.selection_ids = event.team1, event.selection_ids

        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.selection]))

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1. Betslip is opened
        EXPECTED: 2. Added single selection(s) present
        EXPECTED: 3. 'Log in & Bet' button is disabled
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertEqual(self.stake_name, self.selection,
                         msg=f'Selection {self.selection} should be present in betslip')

        self.assertEqual(self.get_betslip_content().bet_now_button.name,
                         vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Bet button caption should be "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" should be disabled now.')

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 'Log in & Bet' button becomes enabled
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))

    def test_004_tap_on_log_in_bet_button(self):
        """
        DESCRIPTION: Tap on 'Log in & Bet' button
        EXPECTED: 'Log In' pop-up is opened
        """
        self.get_betslip_content().bet_now_button.click()
        self.__class__.login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)

    def test_005_log_in_with_user_that_has_no_payment_methods(self):
        """
        DESCRIPTION: Log in with user that has **no payment methods**
        EXPECTED: 1. Quick Deposit popup appears
        EXPECTED: 2. Bet is NOT placed
        """
        self.login_dialog.username = self.username
        self.login_dialog.password = tests.settings.default_password
        self.login_dialog.click_login()
        dialog_closed = self.login_dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Failed to close Login dialog')
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=5)
        if dialog:
            dialog.close_dialog()
            dialog.wait_dialog_closed()

        self.__class__.quick_deposit_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_QUICK_DEPOSIT)
        self.assertTrue(self.quick_deposit_dialog, msg='"Quick Deposit" pop-up is not displayed')

    def test_006_close_quick_deposit_popup(self):
        """
        DESCRIPTION: Close 'Quick Deposit' popup
        """
        self.quick_deposit_dialog.close_dialog()
        dialog_closed = self.quick_deposit_dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Failed to close Quick Deposit dialog')
        self.site.close_all_dialogs(async_close=False)

    def test_007_click_bet_now_button(self):
        """
        DESCRIPTION: Click 'BET NOW' button
        EXPECTED: 1. User is navigated to 'Deposit' page, 'Add Credit/Debit Cards' tab for **Coral** brand
        EXPECTED: 2. User is navigated to Account One system for **Ladbrokes** brand
        EXPECTED: 3. Bet is NOT placed
        """
        self.assertEqual(self.get_betslip_content().bet_now_button.name, vec.betslip.BET_NOW)
        self.get_betslip_content().bet_now_button.click()
        self.assertTrue(self.site.deposit.is_displayed(), msg='User is not navigated to the deposit page')
