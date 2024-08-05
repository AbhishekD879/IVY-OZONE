import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C832536_Verify_navigating_to_Gaming_by_back_button_from_My_Account_pages(Common):
    """
    TR_ID: C832536
    NAME: Verify navigating to Gaming by back button from My Account pages
    DESCRIPTION: This test case verifies navigation to the Gaming by back button from account pages.
    PRECONDITIONS: User must be logged in.
    PRECONDITIONS: User must be on Gaming site.
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_go_to_gaming(self):
        """
        DESCRIPTION: Go to 'Gaming'
        EXPECTED: 'Gaming' homepage is loaded
        """
        pass

    def test_003_click_on_user_balance(self):
        """
        DESCRIPTION: Click on User balance
        EXPECTED: Gaming My Account page is displayed
        """
        pass

    def test_004_go_to_deposit(self):
        """
        DESCRIPTION: Go to 'Deposit'
        EXPECTED: Oxygen 'Deposit' page is opened
        """
        pass

    def test_005_tap_on_back__button(self):
        """
        DESCRIPTION: Tap on back '<' button
        EXPECTED: User comes back to the  Gaming homepage
        """
        pass

    def test_006_click_on_user_balance_and_navigate_to_withdraw(self):
        """
        DESCRIPTION: Click on User balance and navigate to 'Withdraw'
        EXPECTED: Oxygen 'Withdraw' page is opened
        """
        pass

    def test_007_tap_on_back__button(self):
        """
        DESCRIPTION: Tap on back '<' button
        EXPECTED: User comes back to the  Gaming homepage
        """
        pass

    def test_008_repeat_steps_3_and_5_with__cancel_withdraw__my_account__my_history__settings__contact_us(self):
        """
        DESCRIPTION: Repeat steps 3 and 5 with:
        DESCRIPTION: - Cancel withdraw
        DESCRIPTION: - My account
        DESCRIPTION: - My history
        DESCRIPTION: - Settings
        DESCRIPTION: - Contact us
        EXPECTED: User comes back to the  Gaming homepage from the following pages
        """
        pass

    def test_009_repeat_steps_3_8_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 3-8 for Desktop
        EXPECTED: User comes back to the Gaming 'My Account' page
        """
        pass
