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
class Test_C36533575_Self_Exclusion(Common):
    """
    TR_ID: C36533575
    NAME: Self Exclusion
    DESCRIPTION: This test case verifies self-exclusion feature
    PRECONDITIONS: - App is loaded
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: - User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option and continues
    PRECONDITIONS: ! BE AWARE - that you'll NOT be able to login after self-exclusion, so use/create disposable test account
    """
    keep_browser_open = True

    def test_001_scroll_down_and_click_the_self_exclusion_link(self):
        """
        DESCRIPTION: Scroll down and click the 'Self-exclusion' link
        EXPECTED: User is redirected to Gambling controls page with 'Self Exclusion' option selected by default.
        """
        pass

    def test_002_click_the_choose_button(self):
        """
        DESCRIPTION: Click the 'Choose' button
        EXPECTED: User is redirected to 'Self-Exclusion' page with self-exclusion duration and reason selection
        """
        pass

    def test_003_select_self_exclusion_duration_and_select_the_reason(self):
        """
        DESCRIPTION: Select self-exclusion duration and Select the reason
        EXPECTED: Options successfully selected
        """
        pass

    def test_004_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: User is redirected to Self-Exclusion password confirmation page
        """
        pass

    def test_005_enter_correct_password_and_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Enter correct password and Click the 'Self Exclude' button
        EXPECTED: Self exclusion confirmation overlay appears
        """
        pass

    def test_006_tick_both_tickboxes_and_click_the_yes_button(self):
        """
        DESCRIPTION: Tick both tickboxes and Click the 'YES' button
        EXPECTED: - User is self-excluded.
        EXPECTED: - Self-exclusion confirmation page appears.
        """
        pass

    def test_007_click_on_x_close_button_and_logout(self):
        """
        DESCRIPTION: Click on ‘X’ close button and Logout
        EXPECTED: User is logged out
        """
        pass

    def test_008_try_to_login_with_the_same_account(self):
        """
        DESCRIPTION: Try to login with the same account
        EXPECTED: - User is not able to login
        EXPECTED: - Corresponding message about blocked account is shown
        """
        pass
