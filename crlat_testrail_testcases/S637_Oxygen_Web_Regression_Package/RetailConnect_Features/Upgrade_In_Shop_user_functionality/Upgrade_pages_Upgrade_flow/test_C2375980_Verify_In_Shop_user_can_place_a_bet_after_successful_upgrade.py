import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.retail
@vtest
class Test_C2375980_Verify_In_Shop_user_can_place_a_bet_after_successful_upgrade(Common):
    """
    TR_ID: C2375980
    NAME: Verify In-Shop user can place a bet after successful upgrade
    DESCRIPTION: This test case verifies automatic user's re-login after upgrade and possibilities for the user to place a bet
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: Upgrade an in-shop user. Ways to upgrade an in-shop user:
    PRECONDITIONS: 1. Load Oxygen App
    PRECONDITIONS: 2. Log in to the system as an in-shop user
    """
    keep_browser_open = True

    def test_001_add_several_selection_to_betslip(self):
        """
        DESCRIPTION: Add several selection to betslip
        EXPECTED: Selection are added correctly
        EXPECTED: (Note: there is not QuickBet for In-Shop user)
        """
        pass

    def test_002_verify_upgrade_your_account__bet_now_button(self):
        """
        DESCRIPTION: Verify ''UPGRADE YOUR ACCOUNT & BET NOW'' button
        EXPECTED: * ''UPGRADE YOUR ACCOUNT & BET NOW'' button is displayed at the bottom of Betslip (always active)
        """
        pass

    def test_003_tap_upgrade_your_account__bet_now_button(self):
        """
        DESCRIPTION: Tap ''UPGRADE YOUR ACCOUNT & BET NOW'' button
        EXPECTED: User is redirected to 'Upgrade your account' page
        """
        pass

    def test_004_fill_all_required_fields_correctly_use_unique_data_for_mail_and_phone_number_and_tap_the_confirm_button(self):
        """
        DESCRIPTION: Fill all required fields correctly (use unique data for mail and phone number) and tap the 'Confirm' button
        EXPECTED: Successful message dialog is shown
        """
        pass

    def test_005_close_the_successful_message(self):
        """
        DESCRIPTION: Close the successful message
        EXPECTED: * **User is logged into the SB app**
        EXPECTED: * Closing the Pop-up re-directs the user to the betslip (home page is opened on background)
        EXPECTED: * A user is registered in IMS as Multi-Channel customer (find user by newly settled username)
        EXPECTED: [Expected result after vanilla migration]
        EXPECTED: * **User is logged out**
        """
        pass

    def test_006_log_in_to_the_application_with_new_username(self):
        """
        DESCRIPTION: Log in to the application with new username
        EXPECTED: User is logged in
        """
        pass

    def test_007_verify_betslip_content(self):
        """
        DESCRIPTION: Verify Betslip content
        EXPECTED: * Betslip contains previously added selections
        EXPECTED: * 'Bet Now' button is displayed at the bottom ('PLACE BET' button for vanilla)
        """
        pass

    def test_008_verify_user_can_place_a_bet_using_selections_in_betslip(self):
        """
        DESCRIPTION: Verify user can place a bet using selections in betslip
        EXPECTED: 
        """
        pass

    def test_009_add_payment_method_and_make_depositrhm___deposit___add_payment_method__make_a_deposit(self):
        """
        DESCRIPTION: Add payment method and make deposit:
        DESCRIPTION: RHM -> DEPOSIT -> ADD PAYMENT METHOD ->MAKE A DEPOSIT
        EXPECTED: Users balance is updated
        """
        pass

    def test_010__get_back_to_betslip_enter_stake_value_tap_bet_now_button_place_bet_button_for_vanilla(self):
        """
        DESCRIPTION: * Get back to betslip
        DESCRIPTION: * Enter stake value
        DESCRIPTION: * Tap 'Bet Now' button ('PLACE BET' button for vanilla)
        EXPECTED: * Bet is placed
        EXPECTED: * Bet receipt is displayed
        """
        pass
