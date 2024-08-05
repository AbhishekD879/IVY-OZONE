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
class Test_C11250798_Betslip_show_hide_balance_functionality(Common):
    """
    TR_ID: C11250798
    NAME: Betslip: show/hide balance functionality
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies show/hide balance functionality on a Betslip header
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - Betslip should be opened and have some selections added
    """
    keep_browser_open = True

    def test_001_verify_balance_displaying(self):
        """
        DESCRIPTION: Verify balance displaying
        EXPECTED: Account balance is displayed in format '£xx,xxx.xx'
        """
        pass

    def test_002_tap_account_balance_area_and_verify_available_options(self):
        """
        DESCRIPTION: Tap 'Account Balance' area and verify available options
        EXPECTED: Drop down with 2 options appears:
        EXPECTED: - Hide Balance
        EXPECTED: - Deposit
        """
        pass

    def test_003_tap_hide_balance_and_verify_balance_displaying(self):
        """
        DESCRIPTION: Tap 'Hide Balance' and verify balance displaying
        EXPECTED: Account balance is replaced with 'Balance' word
        """
        pass

    def test_004_tap_balance_button_and_verify_available_options(self):
        """
        DESCRIPTION: Tap 'Balance' button and verify available options
        EXPECTED: Drop down with 2 options appears:
        EXPECTED: - Show Balance
        EXPECTED: - Deposit
        """
        pass

    def test_005_tap_show_balance_and_verify_balance_displaying(self):
        """
        DESCRIPTION: Tap 'Show Balance' and verify balance displaying
        EXPECTED: Account balance is displayed in format '£xx,xxx.xx'
        """
        pass
