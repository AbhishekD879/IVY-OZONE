import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@pytest.mark.quick_deposit
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1783')
@pytest.mark.hotfix
# @pytest.mark.sanity
@pytest.mark.na  # this test case is not applicable as quick deposit feature is removed
@vtest
class Test_C34434115_Quick_Deposit(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C34434115
    NAME: Quick Deposit
    DESCRIPTION: This test case verifies Successful Depositing and Placing Bet functionality on the Betslip page via credit/debit cards.
    PRECONDITIONS: * User account with at least one available previously added credit card
    """
    keep_browser_open = True
    additional_amount = 5.0

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children']
                           if 'Match Betting' in market['market']['templateMarketName']), None)
            if not market:
                raise SiteServeException('No "Match Betting" market has been found')
            outcomes = market['market'].get('children')
            if not outcomes:
                raise SiteServeException('No outcomes has been found')

            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('"Home" has not been found in outcomes')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
        self._logger.info(f'*** Football event with selection ids "{self.selection_ids}" and team "{self.team1}"')

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username,
                                  card_number=tests.settings.quick_deposit_card,
                                  amount=tests.settings.min_deposit_amount)

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name="HomePage")

    def test_002_log_in_with_user_account_from_preconditions(self):
        """
        DESCRIPTION: Log in with user account (from preconditions)
        EXPECTED: User is logged in
        """
        self.site.login(username=self.username)

    def test_003_add_any_selection_to_the_betslip_and_open_betslip_page_widget(self):
        """
        DESCRIPTION: Add any selection to the Betslip and open Betslip page / widget
        EXPECTED: Added selections are displayed within Betslip content area
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_004_enter_stake_which_exceeds_current_user_balance(self):
        """
        DESCRIPTION: Enter 'Stake' which exceeds current user balance
        EXPECTED: * 'Please deposit a min of £XX.XX to continue placing your bet' red message is displayed in Betslip
        EXPECTED: * 'Make a deposit' button is shown and enabled
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.__class__.stake_value = self.user_balance + self.additional_amount

        section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(section.items())[0]
        self.stake.amount_form.input.value = self.stake_value

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        actual_message = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message: "{actual_message}" does not match expected: "{expected_message}"')

        self.__class__.make_deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(self.make_deposit_button.is_enabled(),
                        msg=f'"{self.make_deposit_button.name}" button is not enabled')
        self.assertEqual(self.make_deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{self.make_deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_005_press_make_a_deposit_button(self):
        """
        DESCRIPTION: Press 'Make a deposit' button
        EXPECTED: * 'Quick deposit' feature appears in Betslip
        """
        self.make_deposit_button.click()
        # TODO VANO-1783
        self.assertTrue(self.get_betslip_content().has_deposit_form(),
                        msg='"Quick Deposit" section is not displayed')

    def test_006_enter_valid_cvv_into_cvv2_field_and_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV2' field and tap 'DEPOSIT & PLACE BET' button
        EXPECTED: * User balance is updated and calculated as:
        EXPECTED: (User Balance before deposit) + (Amount of deposit) - (Stake of placed bet)
        EXPECTED: * Bet is placed (If no pop-ups are displayed to user)
        EXPECTED: * Betslip is replaced with a Bet Receipt view
        """
        quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        deposit_amount = quick_deposit.amount.input.value
        if self.device_type == 'mobile':
            quick_deposit.cvv_2.click()
            keyboard = quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv

        deposit_button = quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        deposit_button.click(scroll_to=False)
        switch_to_main_page()
        self.check_bet_receipt_is_displayed()
        expected_user_balance = self.user_balance + float(deposit_amount) - self.stake_value
        self.verify_user_balance(expected_user_balance=expected_user_balance)
