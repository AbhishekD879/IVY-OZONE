import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C401603_Betslip_View_with_NO_selections_added_on_Mobile(Common):
    """
    TR_ID: C401603
    NAME: Betslip View with NO selections added on Mobile
    DESCRIPTION: This test case verifies the header of the Betslip with no selections added
    DESCRIPTION: AUTOTEST [C527791]
    PRECONDITIONS: User account with positive balance
    PRECONDITIONS: Applies for Mobile
    """
    keep_browser_open = True

    def test_001_log_in_with_user_from_preconditions(self):
        """
        DESCRIPTION: Log in with User from Preconditions
        EXPECTED: User is logged in
        """
        pass

    def test_002_click_betslip_icon_on_the_header(self):
        """
        DESCRIPTION: Click Betslip icon on the header
        EXPECTED: - Betslip is opened
        EXPECTED: - "Your betslip is empty" message in bold is shown at the top of Betslip content and "Please add one or more selections to place a bet" message is displayed below
        EXPECTED: - "GO BETTING" button is displayed
        EXPECTED: - User balance is displayed at the top right corner of the 'Betslip' header
        EXPECTED: - 'Quick Deposit' link is not available in the Betslip header, only when user taps the balance button drop down with 'Hide Balance' and 'Deposit' options appear
        EXPECTED: - 'FB' icon is NOT displayed in the right corner of the balance bar in the 'Betslip' header
        """
        pass

    def test_003_tap_go_betting_button_and_verify_users_redirection_to_the_homepage(self):
        """
        DESCRIPTION: Tap 'GO BETTING' button and verify user's redirection to the Homepage
        EXPECTED: - User is redirected to the Homepage after the button tapping
        EXPECTED: - if previously Homepage was already opened than Betslip is closed and user stays on the Homepage
        """
        pass
