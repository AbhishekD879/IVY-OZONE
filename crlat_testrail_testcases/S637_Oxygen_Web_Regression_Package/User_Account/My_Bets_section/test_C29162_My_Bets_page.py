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
class Test_C29162_My_Bets_page(Common):
    """
    TR_ID: C29162
    NAME: My Bets page
    DESCRIPTION: This test case verifies My Bets page
    DESCRIPTION: Design:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f0e0920f1230172b7f095
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f22d544fe0d63959b3162
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_my_bets_button(self):
        """
        DESCRIPTION: Tap 'My bets' button
        EXPECTED: * Page with header 'My Bets' and Back button is opened
        EXPECTED: * 'Cash Out'(if available), 'Open Bets' and 'Settled bets' tabs are present
        EXPECTED: * 'Open bets'  tab is selected by default - Available from OX99
        """
        pass

    def test_003_navigate_through_tabs(self):
        """
        DESCRIPTION: Navigate through tabs
        EXPECTED: 'Cash Out(if available)', 'Open Bets' and 'Settled bets' tabs are opened, information is displayed correctly.
        """
        pass

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User gets back to page he/she navigated from
        """
        pass
