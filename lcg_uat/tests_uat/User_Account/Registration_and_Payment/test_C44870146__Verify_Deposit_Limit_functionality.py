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
class Test_C44870146__Verify_Deposit_Limit_functionality(Common):
    """
    TR_ID: C44870146
    NAME: "-Verify Deposit Limit functionality
    DESCRIPTION: "-Verify Deposit Limit URL navigate user to Deposit limit page and When click on 'X' navigate back to sportsbook application
    DESCRIPTION: Verify deposit limit message and verify user can't deposit more then the deposit limit enabled to the user."
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_tap_avatar_icon___my_account_menu_item(self):
        """
        DESCRIPTION: Tap 'Avatar' icon -> 'My Account' menu item
        EXPECTED: 'My Account'  page is opened
        EXPECTED: Click on Gambling Controls menu
        """
        pass

    def test_002_choose_deposit_limits_menu_item(self):
        """
        DESCRIPTION: Choose 'Deposit Limits' menu item
        EXPECTED: 'Deposit Limits' page is opened
        """
        pass

    def test_003_verify__x_close_on_deposit_limit_page(self):
        """
        DESCRIPTION: Verify  'X' Close on deposit limit page
        EXPECTED: Clicking on X should take user to home page
        """
        pass

    def test_004_verify_drop_down(self):
        """
        DESCRIPTION: Verify drop-down
        EXPECTED: There are three drop-down lists for the following deposit limit time periods:
        EXPECTED: 'Daily Deposit Limit:'
        EXPECTED: 'Weekly Deposit Limit:'
        EXPECTED: 'Monthly Deposit Limit:'
        """
        pass

    def test_005_choose_any_amount_and_select_save(self):
        """
        DESCRIPTION: Choose any amount and select 'SAVE'
        EXPECTED: Verify if the user is able to 'Cancel the change request'
        EXPECTED: Verify the message on the popup
        EXPECTED: Validate Yes and Cancel buttons on the popup
        """
        pass

    def test_006_verify_remove_limits(self):
        """
        DESCRIPTION: Verify 'REMOVE LIMITS'
        EXPECTED: Note: It takes 24 hours for this change to come into effect.
        """
        pass

    def test_007_verify_exceeding_of_weeklymonthly_and_daily_limit_for_deposit(self):
        """
        DESCRIPTION: Verify exceeding of Weekly,Monthly and Daily Limit for Deposit
        EXPECTED: Enter amount that exceeds  Deposit Limits for the user
        EXPECTED: for e.g enter amount greater than 9999999 and see if a error message is shown stating ' You can set  your daily, weekly or monthly limit to a maximum of 9999999 .......'
        """
        pass

    def test_008_tap_save_after_changing_deposit_limits(self):
        """
        DESCRIPTION: Tap 'SAVE' after changing Deposit limits
        EXPECTED: Confirmation sent.
        """
        pass
