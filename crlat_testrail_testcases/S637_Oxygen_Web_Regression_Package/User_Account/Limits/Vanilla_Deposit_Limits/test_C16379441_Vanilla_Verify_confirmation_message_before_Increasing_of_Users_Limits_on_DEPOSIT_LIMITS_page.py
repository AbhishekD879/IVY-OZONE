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
class Test_C16379441_Vanilla_Verify_confirmation_message_before_Increasing_of_Users_Limits_on_DEPOSIT_LIMITS_page(Common):
    """
    TR_ID: C16379441
    NAME: [Vanilla] Verify confirmation message before Increasing of User's Limits on 'DEPOSIT LIMITS' page 
    DESCRIPTION: This test case verifies appearing of confirmation message after the 24 hours has elapsed before Increasing of Users' Limits on 'Limits' page.
    PRECONDITIONS: - Users' limits are lower than 99 00000
    PRECONDITIONS: - 2 users have changed Deposit Limits less than 24 hours ago
    """
    keep_browser_open = True

    def test_001_wait_till_24_hours_elapse_from_the_moment_of_increasing_of_users_limits(self):
        """
        DESCRIPTION: Wait till 24 hours elapse from the moment of Increasing of User's Limits
        EXPECTED: 
        """
        pass

    def test_002_log_into_the_application(self):
        """
        DESCRIPTION: Log into the application
        EXPECTED: * User is logged in
        EXPECTED: * 'Deposit Limits' pop-up appears after log in
        """
        pass

    def test_003_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: 'Deposit Limits' pop-up is no more shown
        EXPECTED: Limits are not changed
        """
        pass

    def test_004_go_to_the_account_menu_gambling_controls_deposit_limits_page(self):
        """
        DESCRIPTION: Go to the 'ACCOUNT' menu->'GAMBLING CONTROLS'->'DEPOSIT LIMITS' page
        EXPECTED: - 'Deposit Limits' page is open with the message: "Your requested change of deposit limits is available now. To activate your new limits, please confirm below."
        EXPECTED: - There is SAVE button available.
        """
        pass

    def test_005_tap_save_button(self):
        """
        DESCRIPTION: Tap 'SAVE' button
        EXPECTED: User's limits of deposit are properly set up.
        """
        pass

    def test_006_log_in_with_the_second_user_and_repeat_steps_1_5(self):
        """
        DESCRIPTION: Log in with the second user and repeat steps 1-5
        EXPECTED: 
        """
        pass

    def test_007_tap_save_button(self):
        """
        DESCRIPTION: Tap 'SAVE' button
        EXPECTED: After tapping 'SAVE' button:
        EXPECTED: * user's limit is changed to value, which was set 24 hours ago
        """
        pass
