import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.bet_placement
@pytest.mark.creditcard
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29121_Overask_and_Quick_Deposit_functionality(BaseBetSlipTest):
    """
    TR_ID: C29121
    NAME: Overask and Quick Deposit functionality
    DESCRIPTION: This test case verifies Overask and Quick Deposit interaction
    """
    keep_browser_open = True
    username = None
    max_bet = 2.00
    addition = 10.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with max bet set to trigger Overask
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.eventID, self.__class__.team1, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.selection_ids
        self.__class__.created_event_name = event_params.team1 + ' v ' + event_params.team2

    def test_001_login_to_application_with_user_who_has_registered_deposit_method(self):
        """
        DESCRIPTION: Login to application with user who has registered deposit method
        """
        self.__class__.username = tests.settings.quick_deposit_user
        self.site.login(username=self.username)

    def test_002_add_selection_to_betslip_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection to Betslip and enter Stake value which is higher then user's balance and higher then max allowed stake for the selection
        EXPECTED: *   'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: *   'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

        section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(section.items())[0]

        self.__class__.deposit_amount = self.max_bet + self.addition
        self.__class__.expected_user_balance = self.site.header.user_balance + self.deposit_amount
        stake_value = self.site.header.user_balance + self.deposit_amount
        self.stake.amount_form.input.value = stake_value

        expected_message_text = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.deposit_amount)

        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Info panel message: "{actual_message_text}" '
                             f'is not as expected: "{expected_message_text}"')

        self.__class__.deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(self.deposit_button.is_enabled(), msg=f'"{self.deposit_button.name}" button is not enabled')
        self.assertEqual(self.deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{self.deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_003_tap_on_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Tap on 'MAKE A QUICK DEPOSIT' button
        EXPECTED: *   'Quick Deposit' section is expanded
        EXPECTED: *   'Amount' field is filled with needed amount for a bet
        """
        self.deposit_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is not displayed')

        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        actual_amount_field_value = self.quick_deposit.amount.input.value
        expected_amount_field_value = "{0:.2f}".format(self.deposit_amount)
        self.assertEqual(actual_amount_field_value, expected_amount_field_value,
                         msg=f'Amount field value: "{actual_amount_field_value}"'
                             f'is not as expected: "{expected_amount_field_value}"')

    def test_004_enter_correct_cvv_code(self):
        """
        DESCRIPTION: Enter correct 'CVV' code
        EXPECTED: *   'DEPOSIT & PLACE BET' button becomes enabled
        """
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            keyboard = self.quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv
        deposit_button = self.quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')

    def test_005_click_on_deposit_and_bet_button(self):
        """
        DESCRIPTION: Click on 'DEPOSIT & PLACE BET' button
        EXPECTED: *   Money are deposited successfully
        EXPECTED: *   Overask review process is started
        """
        self.quick_deposit.deposit_and_place_bet_button.click()

        self.site.close_all_dialogs(async_close=False)
        self.verify_user_balance(expected_user_balance=self.expected_user_balance)

        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

    def test_006_verify_information_which_is_displayed_for_user(self):
        """
        DESCRIPTION: Verify information which is displayed for user after message about successful deposit stops to display
        EXPECTED: *   The bet review notification is shown to the User
        """
        overask_overlay = self.get_betslip_content().overask
        overask_title = overask_overlay.overask_title.is_displayed()
        self.assertTrue(overask_title, msg='Overask title message is not shown')

        overask_exceeds = overask_overlay.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds, msg='Overask exceeds message is not shown')

        overask_offer = overask_overlay.overask_offer.is_displayed()
        self.assertTrue(overask_offer, msg='Overask offer message is not shown')
