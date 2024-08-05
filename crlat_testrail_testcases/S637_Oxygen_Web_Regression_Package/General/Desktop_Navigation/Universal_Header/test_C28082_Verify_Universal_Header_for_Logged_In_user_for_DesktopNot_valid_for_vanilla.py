import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28082_Verify_Universal_Header_for_Logged_In_user_for_DesktopNot_valid_for_vanilla(Common):
    """
    TR_ID: C28082
    NAME: Verify Universal Header for Logged In user for Desktop(Not valid for vanilla)
    DESCRIPTION: Please note: this test case is not valid for Vanilla.
    DESCRIPTION: This test case verifies Universal Header UI and functionality when user is logged in on Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: 1. Make sure you have few users registered
    PRECONDITIONS: 2. User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_verify_universal_header_displaying(self):
        """
        DESCRIPTION: Verify Universal Header displaying
        EXPECTED: Universal Header is displayed on every page across the app
        """
        pass

    def test_003_verify_universal_header_content(self):
        """
        DESCRIPTION: Verify Universal Header content
        EXPECTED: The following items are displayed in the Universal header:
        EXPECTED: *   'Main Navigation' menu (CMS configurable)
        EXPECTED: *   'Sports Sub Navigation' menu (CMS configurable)
        EXPECTED: *   'Coral' logo
        EXPECTED: *   'Odds Format' selector
        EXPECTED: *   'Help' link
        EXPECTED: *   'Contact Us' link
        EXPECTED: *   'Balance' item with currency symbol and user's balance amount
        EXPECTED: *   'Quick Deposit' item
        EXPECTED: *   'My Account' item
        """
        pass

    def test_004_navigate_to_any_page_in_app_and_click_on_coral_logo(self):
        """
        DESCRIPTION: Navigate to any page in app and click on 'Coral' logo
        EXPECTED: User is navigated to Homepage after clicking 'Coral' logo
        """
        pass

    def test_005_click_on_quick_deposit_item(self):
        """
        DESCRIPTION: Click on 'Quick Deposit' item
        EXPECTED: 'Deposit' page is opened in the Main View
        """
        pass

    def test_006_click_on_my_account_item(self):
        """
        DESCRIPTION: Click on 'My Account' item
        EXPECTED: *   Right Slider menu doesn't appear on Desktop
        EXPECTED: *   'My Account' page is opened in the Main View
        """
        pass

    def test_007_verify_odds_format_selector(self):
        """
        DESCRIPTION: Verify 'Odds Format' selector
        EXPECTED: 'Fractional' option is selected by default
        """
        pass

    def test_008_click_on_odds_format_selector(self):
        """
        DESCRIPTION: Click on 'Odds Format' selector
        EXPECTED: * Dropdown list with 'Fractional' and 'Decimal' options is opened
        EXPECTED: * Possible to choose appropriate Odds Format from dropdown list
        """
        pass
