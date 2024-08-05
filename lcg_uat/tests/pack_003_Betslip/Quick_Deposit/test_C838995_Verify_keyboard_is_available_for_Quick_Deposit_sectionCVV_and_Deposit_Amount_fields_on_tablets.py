import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C838995_Verify_keyboard_is_available_for_Quick_Deposit_sectionCVV_and_Deposit_Amount_fields_on_tablets(BaseBetSlipTest):
    """
    TR_ID: C838995
    NAME: Verify keyboard is available for Quick Deposit section('CVV' and 'Deposit Amount' fields) on tablets
    DESCRIPTION: Verify keyboard is available for Quick Deposit section('CVV' and 'Deposit Amount' fields) on tablets
    PRECONDITIONS: User has added at least one Debit/Credit card
    """
    keep_browser_open = True

    def test_001_log_in_to_the_oxygen_app_on_ipad(self):
        """
        DESCRIPTION: Log in to the Oxygen app on iPad;
        EXPECTED: User is logged in
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next((market['market']['children'] for market in event['event']['children']
                            if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name, self.__class__.selection_id = list(selection_ids.items())[0]
        else:

            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[0]
        self.site.login(username=tests.settings.quick_deposit_user)

    def test_002_add_a_selection_to_betslip(self):
        """
        DESCRIPTION: Add a selection to betslip
        EXPECTED: Selection is displayed in Betslip widget
        """
        user_balance = self.site.header.user_balance
        self.site.wait_splash_to_hide(5)
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        if not int(user_balance):
            wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                            name='Quick deposit section to be displayed', timeout=10)
            self.device.refresh_page()
            self.site.open_betslip()
        if self.get_betslip_content().has_deposit_form():
            self.site.betslip.quick_deposit.close_button.click()
        place_bet_button = self.site.betslip.bet_now_button.name
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        self.assertIn(self.selection_name, singles_section.keys(),
                      msg=f'Actual list "{singles_section.items()}" does not contain Added selection "{self.selection_name}"')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = user_balance + 5
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        make_deposit_button = self.site.betslip.make_quick_deposit_button.name
        self.assertNotEqual(place_bet_button, make_deposit_button,
                            msg=f'Place bet button name: "{place_bet_button}" is not changed to Make deposit button: {make_deposit_button}')

    def test_003_enter_a_stake_higher_than_the_current_balance_of_a_user(self):
        """
        DESCRIPTION: Enter a stake higher than the current balance of a user
        EXPECTED: 'PLACE BET' button changes to 'MAKE A DEPOSIT'
        EXPECTED: 'Message about deposit amount needed in order to place bet is shown'
        """
        # Covered in the above step test_003

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button'
        """
        self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit popup is not displayed')

    def test_005_tap_at_cvv_field(self):
        """
        DESCRIPTION: Tap at CVV field
        EXPECTED: - Cursor is focused in CVV field
        EXPECTED: - Device Keyboard appears
        """
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.quick_deposit.cvv_2.click()
        self.assertTrue(self.quick_deposit.keyboard.is_displayed(), msg='Betslip keyboard is not shown')

    def test_006_tap_at_deposit_amount_field(self):
        """
        DESCRIPTION: Tap at 'Deposit Amount' field
        EXPECTED: - Cursor is focused in Amount field
        EXPECTED: - Device Keyboard appears
        """
        self.quick_deposit.amount.input.click()
        self.assertTrue(self.quick_deposit.keyboard.is_displayed(), msg='Betslip keyboard is not shown')

    def test_007_fill_in_all_required_fields_and_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Fill in all required fields and tap "DEPOSIT & PLACE BET" button
        EXPECTED: Deposit and Bet is done successfully
        """
        self.quick_deposit.cvv_2.click()
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value='1234')
        self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        self.quick_deposit.deposit_and_place_bet_button.click()
        self.check_bet_receipt_is_displayed()
