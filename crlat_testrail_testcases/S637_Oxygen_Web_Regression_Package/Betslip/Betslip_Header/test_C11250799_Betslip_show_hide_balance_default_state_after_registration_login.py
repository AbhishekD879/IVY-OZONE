import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C11250799_Betslip_show_hide_balance_default_state_after_registration_login(Common):
    """
    TR_ID: C11250799
    NAME: Betslip: show/hide balance default state after registration/login
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies show/hide balance default values after user registration or login
    PRECONDITIONS: Application should be opened
    """
    keep_browser_open = True

    def test_001___register_new_user_add_some_selections_to_betslip_and_open_betslip__verify_balance_displaying(self):
        """
        DESCRIPTION: - Register new user, add some selections to betslip and open betslip
        DESCRIPTION: - Verify balance displaying
        EXPECTED: Account balance is displayed in format '£xx,xxx.xx'
        """
        pass

    def test_002___tap_account_balance_area_and_tap_hide_balance_button__refresh_the_page_and_open_betslip__verify_balance_displaying(self):
        """
        DESCRIPTION: - Tap 'Account Balance' area and tap 'Hide Balance' button
        DESCRIPTION: - Refresh the page and open betslip
        DESCRIPTION: - Verify balance displaying
        EXPECTED: Word 'Balance' is displayed instead of account balance
        """
        pass

    def test_003___logout_and_login_again__open_betslip_and_verify_balance_displaying(self):
        """
        DESCRIPTION: - Logout and login again
        DESCRIPTION: - Open betslip and verify balance displaying
        EXPECTED: Account balance is displayed in format '£xx,xxx.xx'
        """
        pass
