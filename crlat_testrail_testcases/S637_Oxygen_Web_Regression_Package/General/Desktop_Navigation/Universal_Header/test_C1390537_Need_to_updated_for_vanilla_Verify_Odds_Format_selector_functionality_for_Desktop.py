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
class Test_C1390537_Need_to_updated_for_vanilla_Verify_Odds_Format_selector_functionality_for_Desktop(Common):
    """
    TR_ID: C1390537
    NAME: [Need to updated for vanilla] Verify 'Odds Format' selector functionality for Desktop
    DESCRIPTION: This test case verifies 'Odds Format' selector functionality for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    DESCRIPTION: The example of how the prices are displayed in the Site Server query:
    DESCRIPTION: Decimal: priceDec="1.70"
    DESCRIPTION: Fractional: priceNum="7" priceDen="10". Note: the price will be displayed as 7/10
    DESCRIPTION: AUTOTEST: [C2635853]
    DESCRIPTION: NEEDS TO BE UPDATED: 'Odds Format' is stored in local storage instead of Cookies
    PRECONDITIONS: 1. Cookies should be cleared
    PRECONDITIONS: 2. User must be logged in
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 'Settings/Preferences' menu should be switched off in CMS for 'Account Menu' on Desktop.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_add_lp_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add LP selections to the Betslip
        EXPECTED: 
        """
        pass

    def test_003_verify_odds_format_selector_displaying_in_the_header(self):
        """
        DESCRIPTION: Verify 'Odds Format' selector displaying in the header
        EXPECTED: * 'Fractional' option is selected by default
        EXPECTED: * All 'Price/Odds' buttons display prices in fractional format across the application
        """
        pass

    def test_004_click_on_odds_format_selector(self):
        """
        DESCRIPTION: Click on 'Odds Format' selector
        EXPECTED: * Dropdown list with 'Fractional' and 'Decimal' options is opened
        EXPECTED: * Possible to choose appropriate Odds Format from dropdown list
        """
        pass

    def test_005_hover_the_mouse_over_the_opened_dropdown_list(self):
        """
        DESCRIPTION: Hover the mouse over the opened dropdown list
        EXPECTED: Hover state changes are activated on each item
        """
        pass

    def test_006_choose_decimal_option_in_odds_format_selector(self):
        """
        DESCRIPTION: Choose 'Decimal' option in 'Odds Format' selector
        EXPECTED: * 'Decimal' option is displayed in 'Odds Format' selector
        EXPECTED: * All 'Price/Odds' buttons display prices in decimal format across the application
        EXPECTED: *  Price format is changed on the Betslip to Decimal (New 'buildBet' request is sent)
        """
        pass

    def test_007_log_out_from_the_app(self):
        """
        DESCRIPTION: Log out from the app
        EXPECTED: * 'Odds Format' selector is Not displayed at Universal Header
        EXPECTED: * Odds format is 'remembered' and is the same after logout
        """
        pass

    def test_008_log_in_the_app_again_with_the_same_or_different_user_and_check_odds_format(self):
        """
        DESCRIPTION: Log in the app again (with the same or different user) and check Odds Format
        EXPECTED: Odds format is 'remembered' and is the same after login in
        """
        pass

    def test_009_change_odds_format_and_open_the_app_in_a_new_tab_and_verify_odds_format(self):
        """
        DESCRIPTION: Change Odds format and open the app in a new tab and verify Odds Format
        EXPECTED: Odds format is 'remembered' and is the same in a new tab
        """
        pass

    def test_010_change_odds_format_and_clear_cookies(self):
        """
        DESCRIPTION: Change Odds format and clear cookies
        EXPECTED: Default Odds format 'Fractional' is set
        """
        pass
