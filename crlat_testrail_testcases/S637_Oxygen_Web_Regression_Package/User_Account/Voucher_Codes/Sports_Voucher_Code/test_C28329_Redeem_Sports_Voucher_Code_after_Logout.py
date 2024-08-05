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
class Test_C28329_Redeem_Sports_Voucher_Code_after_Logout(Common):
    """
    TR_ID: C28329
    NAME: Redeem Sports Voucher Code after Logout
    DESCRIPTION: This test scenario verifies that a user is logged out by server automatically when his/her session is over on the server
    DESCRIPTION: Voucher Codes functionality is controlled by GVC side
    PRECONDITIONS: NOTE :
    PRECONDITIONS: to generate Sports Voucher Codes contact GVC team
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger an event when the session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab -> open 'Redeem Voucher' page
    PRECONDITIONS: *   Login to Oxygen in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab ->> Log in popup is shown
    PRECONDITIONS: *   Close Log in popup
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in(self):
        """
        DESCRIPTION: Log In
        EXPECTED: 
        """
        pass

    def test_003_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu icon
        EXPECTED: Right Menu is opened
        """
        pass

    def test_004_tap_offers__free_bets_button(self):
        """
        DESCRIPTION: Tap 'Offers & Free Bets' button
        EXPECTED: 'Offers & Free Bets' page is opened
        """
        pass

    def test_005_tap_voucher_codes_button(self):
        """
        DESCRIPTION: Tap 'Voucher Codes' button
        EXPECTED: 'Redeem Voucher' page is opened
        """
        pass

    def test_006_enter_any_voucher_code_insports_voucher_codefield(self):
        """
        DESCRIPTION: Enter any Voucher Code in** 'Sports Voucher Code:' **field
        EXPECTED: 
        """
        pass

    def test_007_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_008_verify_sports_voucher_code_section(self):
        """
        DESCRIPTION: Verify ** 'Sports Voucher Code:' ** section
        EXPECTED: *   User is logged out from the application automatically without performing any actions
        EXPECTED: *   User is not able to see the content of ** 'Sports Voucher Code:' ** section
        EXPECTED: *   User is redirected to the Homepage
        """
        pass
