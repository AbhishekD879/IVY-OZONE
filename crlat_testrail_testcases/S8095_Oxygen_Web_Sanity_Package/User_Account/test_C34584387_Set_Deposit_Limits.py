import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C34584387_Set_Deposit_Limits(Common):
    """
    TR_ID: C34584387
    NAME: Set Deposit Limits
    DESCRIPTION: Verify that the customer can successfully set "Deposit limits"
    DESCRIPTION: AUTOMATED [C46287316]
    PRECONDITIONS: - No limits are currently set to user
    PRECONDITIONS: - Step 10 - text on pop-up can be changeable by GVC.
    """
    keep_browser_open = True

    def test_001_login_to_oxygen_and_navigate_to_my_account_menu___gambling_controls(self):
        """
        DESCRIPTION: Login to Oxygen and navigate to My Account menu -> Gambling Controls
        EXPECTED: 'Gambling Controls' page is displayed
        """
        pass

    def test_002_pick_deposit_limits_option_should_be_picked_by_default_and_tap_on_choose_button(self):
        """
        DESCRIPTION: Pick 'Deposit limits' option (should be picked by default) and tap on 'Choose' button
        EXPECTED: * 'Set deposit limits' page is displayed
        EXPECTED: * 'Daily', 'Weekly' and 'Monthly' deposit limit textfields are displayed with Current limit value under each textfield
        EXPECTED: ![](index.php?/attachments/get/11918116)
        """
        pass

    def test_003_enter_daily_limit_value_higher_than_the_weekly_deposit_limit(self):
        """
        DESCRIPTION: Enter 'Daily' limit value higher than the 'Weekly' Deposit limit
        EXPECTED: "Weekly deposit limit has to be equal or higher than daily deposit limit." - displayed under 'Weekly' limit dropdown
        """
        pass

    def test_004_enter_monthly_limit_value_lower_than_the_weekly_deposit_limit(self):
        """
        DESCRIPTION: Enter 'Monthly' limit value lower than the 'Weekly' Deposit limit
        EXPECTED: "Monthly deposit limit has to be equal or higher than weekly deposit limit." - displayed under 'Monthly' limit dropdown
        """
        pass

    def test_005_add_correct_dailyweeklymonthly_eg_1005001000_and_click_on_save_button(self):
        """
        DESCRIPTION: Add correct Daily/Weekly/Monthly (e.g. 100/500/1000) and click on "Save" button
        EXPECTED: * "DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: Your limits have been changed." message is displayed on green background with the tick icon
        EXPECTED: * 'Current limit' values are changed under each dropdown
        """
        pass

    def test_006_try_to_increase_the_weekly_deposit_limit_eg_800(self):
        """
        DESCRIPTION: Try to increase the Weekly Deposit limit (e.g. 800)
        EXPECTED: * "Confirmation sent." header with "Your requested limits will be available within 24 hours." message and active 'Cancel the change request' button is displayed on blue background with information sign.
        EXPECTED: * 'Weekly' field is populated with the value entered  and greyed out
        EXPECTED: * 'Current limit' for 'Weekly' limit is still showing limit entered in step 5
        """
        pass

    def test_007_press_cancel_the_change_request_button_on_blue_information_message(self):
        """
        DESCRIPTION: Press 'Cancel the change request' button on blue information message
        EXPECTED: * 'Cancel limit change request' dialogue is displayed
        EXPECTED: * "You are about to cancel the recent requested change to your limits. Are you sure want to do that?" message is shown
        EXPECTED: * No/Yes buttons are displayed
        """
        pass

    def test_008_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: * "Your request was cancelled." header with "You can now change the limits again and confirm your new request." message is displayed on blue background with information sign.
        EXPECTED: * 'Weekly' field is populated with the value entered in step 5 and is active
        EXPECTED: * 'Current limit' for 'Weekly' limit is showing limit entered in step 5
        """
        pass

    def test_009_press_on_remove_limits_green_button(self):
        """
        DESCRIPTION: Press on 'Remove limits' green button
        EXPECTED: * "Confirmation sent." header with "Your requested limits will be available within 24 hours." message and active 'Cancel the change request' button is displayed on blue background with information sign.
        EXPECTED: * All field are populated with the 'Set your <daily/weekly/monthly> limit' grey placeholder and are disabled
        EXPECTED: * 'Current limit' values are showing limits entered in step 5
        """
        pass

    def test_010_1_close_deposit_limit_page2_navigate_to_my_account_menu___cashier___deposit_and_try_to_deposit_an_amount_higher_than_the_daily_deposit_limit_set_in_step_5(self):
        """
        DESCRIPTION: 1) Close 'Deposit limit' page
        DESCRIPTION: 2) Navigate to My Account menu -> Cashier -> Deposit and try to deposit an amount Higher than the Daily Deposit Limit set in step 5
        EXPECTED: * "Warning: self-set deposit limit exceeded" header with message "{USERNAME} You have exceeded the daily deposit limit of {CURRENCY CODE and VALUE} previously set by you.
        EXPECTED: Click the below button to increase your deposit limits.
        EXPECTED: Click the Deposit button below to submit your request again with the revised deposit amount of {CURRENCY CODE and VALUE} (CURRENCY CODE and VALUE} excluding the 0.00 GBP fee).
        EXPECTED: If you prefer, you can cancel this deposit request and return to the Deposits page" is displayed on blue background.
        EXPECTED: * DEPOSIT {CURRENCY CODE and VALUE} NOW button is displayed
        EXPECTED: * The deposit is not successful. The amount is not added to the customer's balance.
        EXPECTED: ![](index.php?/attachments/get/46550755)
        EXPECTED: ![](index.php?/attachments/get/58929068)
        """
        pass
