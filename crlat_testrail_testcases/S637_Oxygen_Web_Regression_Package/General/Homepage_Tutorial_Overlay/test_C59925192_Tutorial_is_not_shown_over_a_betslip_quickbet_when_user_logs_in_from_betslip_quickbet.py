import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59925192_Tutorial_is_not_shown_over_a_betslip_quickbet_when_user_logs_in_from_betslip_quickbet(Common):
    """
    TR_ID: C59925192
    NAME: Tutorial is not shown over a betslip/quickbet when user logs in from betslip/quickbet
    DESCRIPTION: Information that Homepage Tutorial Overlay was shown is saved in Local Storage: name - OX.tutorial, value - true. Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
    DESCRIPTION: ![](index.php?/attachments/get/119596341)
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_clear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application
        EXPECTED: Do not login to application and go to the Homepage/Football Landing page
        """
        pass

    def test_002_add_any_selection_to_betslip(self):
        """
        DESCRIPTION: Add any Selection to Betslip.
        EXPECTED: Selection is added to Betslip
        """
        pass

    def test_003_open_betslip_and_provide_a_stake_that_is_smallerbigger_than_user_balance_ie_150gbp(self):
        """
        DESCRIPTION: Open Betslip and provide a stake that is smaller/bigger than user balance (i.e. 150GBP)
        EXPECTED: 'Stake' field contains provided amount
        """
        pass

    def test_004_click_on_login__place_bet_and_log_in_as_a_user_with_little_balance_lower_than_provided_stake(self):
        """
        DESCRIPTION: Click on "Login & Place Bet" and log in as a user with little balance (lower than provided stake)
        EXPECTED: User remains on betslip, but no Tutorial overlay is shown
        """
        pass

    def test_005_log_out_from_appclear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Log out from App
        DESCRIPTION: Clear browser cookies and load Oxygen application
        EXPECTED: Do not login to application and go to the Homepage/Football Landing page
        """
        pass

    def test_006_add_any_selection_to_quickbet(self):
        """
        DESCRIPTION: Add any Selection to Quickbet
        EXPECTED: Selection is added to Quickbet
        """
        pass

    def test_007_provide_a_stake_that_is_smallerbigger_than_user_balance_ie_150gbp(self):
        """
        DESCRIPTION: Provide a stake that is smaller/bigger than user balance (i.e. 150GBP)
        EXPECTED: 'Stake' field contains provided amount
        """
        pass

    def test_008_click_on_login__place_bet_and_log_in_as_a_user_with_little_balance_lower_than_provided_stake(self):
        """
        DESCRIPTION: Click on "Login & Place Bet" and log in as a user with little balance (lower than provided stake)
        EXPECTED: User remains on Quickbet, but no Tutorial overlay is shown
        """
        pass
