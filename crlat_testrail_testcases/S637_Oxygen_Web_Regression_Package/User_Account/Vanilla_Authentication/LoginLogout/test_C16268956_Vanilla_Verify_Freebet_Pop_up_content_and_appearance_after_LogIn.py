import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C16268956_Vanilla_Verify_Freebet_Pop_up_content_and_appearance_after_LogIn(Common):
    """
    TR_ID: C16268956
    NAME: [Vanilla] Verify Freebet Pop-up content and appearance after LogIn
    DESCRIPTION: Verify Freebet pop-up content and appearance after successful log in;
    DESCRIPTION: How to add free bets: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account;
    PRECONDITIONS: Steps to see required info in Development Tool:
    PRECONDITIONS: 'Network' -> 'user' request
    """
    keep_browser_open = True

    def test_001_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log In' button
        EXPECTED: 'Log In' pop-up is displayed
        """
        pass

    def test_002_enter_valid_credentials_for_a_user_with_a_positive_balance_and__freebets___and_tapclick_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials for a user with a positive balance and  freebets >  and tap/click 'Log in' button
        EXPECTED: - User is logged in successfully
        EXPECTED: - 'Free Bet' pop-up is shown
        """
        pass

    def test_003_compare_information_displayed_in_pop_up_with_data_received_from_preconditions(self):
        """
        DESCRIPTION: Compare information displayed in pop-up with data received from Preconditions
        EXPECTED: The data must match:
        EXPECTED: *   Free bet decription = "freebetOfferName"
        EXPECTED: *   Expiry date = "freebetTokenExpiryDate"
        EXPECTED: *   Value = "freebetTokenValue"
        EXPECTED: *   Total sum of Free bets at the top of table;
        """
        pass

    def test_004_check_buttons_on_free_bet_pop_up(self):
        """
        DESCRIPTION: Check buttons on  'Free Bet' pop-up;
        EXPECTED: Pop-up includes an X and an OK button to close the pop-up;
        """
        pass

    def test_005_close_the_pop_up_selecting_x_or_ok_button(self):
        """
        DESCRIPTION: Close the pop-up, selecting X or OK button;
        EXPECTED: Pop-up is closed;
        """
        pass

    def test_006_log_out_and_log_in_with_the_same_user(self):
        """
        DESCRIPTION: Log out and log in with the same user
        EXPECTED: User is logged in successfully.
        EXPECTED: Free Bet pop-up is not shown;
        """
        pass

    def test_007_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application;
        EXPECTED: User is logged out successfully;
        """
        pass

    def test_008_add_new_freebet_for_user__via_ob_office(self):
        """
        DESCRIPTION: Add new freebet for user:
        DESCRIPTION: - via OB Office;
        EXPECTED: Free bet is received
        """
        pass

    def test_009_log_in_with_the_same_user(self):
        """
        DESCRIPTION: Log in with the same user
        EXPECTED: User is logged in successfully.
        EXPECTED: Free Bet pop-up is shown with information of all available for user freebets
        """
        pass

    def test_010_use_one_free_bet__successfully_put_a_stake_in_betslip(self):
        """
        DESCRIPTION: Use one free bet ( successfully put a stake in betslip)
        EXPECTED: Free bet is used and not available for user anymore (cannot be chosen during bet placement as it disappears);
        """
        pass

    def test_011_log_out_and_log_in_with_the_same_user(self):
        """
        DESCRIPTION: Log out and log in with the same user
        EXPECTED: - User is logged in successfully
        EXPECTED: - Free Bet pop-up is not shown;
        EXPECTED: (dev tools - Application storage > OX.freeBetTooltipSeenQuickbet-[username] :: true)
        """
        pass

    def test_012_log_out_from_the_system(self):
        """
        DESCRIPTION: Log out from the system;
        EXPECTED: User Logged out;
        """
        pass

    def test_013_add_one_more_free_bet_with_short_expiration_term_5_min(self):
        """
        DESCRIPTION: Add one more free bet with short expiration term (5 min);
        EXPECTED: The freebet is added;
        """
        pass

    def test_014_add_one_more_freebet_with_any_desired_term_of_expiration(self):
        """
        DESCRIPTION: Add one more freebet with any desired term of expiration;
        EXPECTED: Freebet is added;
        """
        pass

    def test_015_wait_until_added_in_step_13_freebet_will_be_expired_eg_5_min(self):
        """
        DESCRIPTION: Wait until added in step 13 freebet will be expired; (e.g. 5 min)
        EXPECTED: Expiration term is passed;
        """
        pass

    def test_016_login_into_the_system_again(self):
        """
        DESCRIPTION: Login into the system again;
        EXPECTED: User should see next items after login:
        EXPECTED: 1. Freebet pop-up is shown;
        EXPECTED: 2. Expired freebet is NOT displayed in the pop-up list;
        EXPECTED: 3. Added in step 14 freebet is present in pop-up list;
        """
        pass
