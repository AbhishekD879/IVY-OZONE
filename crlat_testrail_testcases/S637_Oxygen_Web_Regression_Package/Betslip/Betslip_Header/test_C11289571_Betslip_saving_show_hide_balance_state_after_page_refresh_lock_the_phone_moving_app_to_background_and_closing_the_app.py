import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C11289571_Betslip_saving_show_hide_balance_state_after_page_refresh_lock_the_phone_moving_app_to_background_and_closing_the_app(Common):
    """
    TR_ID: C11289571
    NAME: Betslip: saving show/hide balance state after page refresh, lock the phone, moving app to background and closing the app
    DESCRIPTION: This test case verifies that show/hide balance saves the state after page refresh, lock the phone, move app to background, close the app
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have added selections to Betslip
    PRECONDITIONS: - Account balance should be hidden
    PRECONDITIONS: - Betslip should be opened
    """
    keep_browser_open = True

    def test_001_verify_account_balance_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify account balance displaying in betslip
        EXPECTED: Account balance is hidden
        """
        pass

    def test_002_refresh_the_page_and_verify_account_balance_displaying_in_betslip(self):
        """
        DESCRIPTION: Refresh the page and verify account balance displaying in betslip
        EXPECTED: Account balance is hidden
        """
        pass

    def test_003___move_app_to_background_and_open_again__verify_account_balance_displaying_in_betslip(self):
        """
        DESCRIPTION: - Move app to background and open again
        DESCRIPTION: - Verify account balance displaying in betslip
        EXPECTED: Account balance is hidden
        """
        pass

    def test_004___lock_and_unlock_the_phone__verify_account_balance_displaying_in_betslip(self):
        """
        DESCRIPTION: - Lock and unlock the phone
        DESCRIPTION: - Verify account balance displaying in betslip
        EXPECTED: Account balance is hidden
        """
        pass

    def test_005_iosandroid_wrappers__kill_the_app_and_launch_againweb_application__close_the_browser_and_open_it_again__verify_account_balance_displaying_in_betslip(self):
        """
        DESCRIPTION: **IOS/Android wrappers:**
        DESCRIPTION: - Kill the app and launch again
        DESCRIPTION: **Web application**
        DESCRIPTION: - Close the browser and open it again
        DESCRIPTION: - Verify account balance displaying in betslip
        EXPECTED: Account balance is hidden
        """
        pass
