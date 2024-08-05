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
class Test_C28356_Verify_Odds_Format_change(Common):
    """
    TR_ID: C28356
    NAME: Verify Odds Format change
    DESCRIPTION: This test case verifies Odds Format change.
    DESCRIPTION: The example of how the prices are displayed in the Site Server query:
    DESCRIPTION: **Decimal:** priceDec="1.70"
    DESCRIPTION: **Fractional:** priceNum="7" priceDen="10". Note: the price will be displayed as 7/10
    PRECONDITIONS: User must be logged in
    """
    keep_browser_open = True

    def test_001_coraltap_an_avatar_iconladbrokestap_an_avatar_icon_or_balance_button(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap an avatar icon
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap an avatar icon or balance button
        EXPECTED: **Coral:** / **Ladbrokes:**
        EXPECTED: **Mobile** 'Menu' page / **DESKTOP** 'Menu' pop-up is opened
        """
        pass

    def test_002_tap_on_settings_item(self):
        """
        DESCRIPTION: Tap on 'Settings' item
        EXPECTED: **Coral:** / **Ladbrokes:**
        EXPECTED: - **Mobile** 'Settings' page / **DESKTOP** 'Settings' pop-up is opened with items
        EXPECTED: - My Account Details
        EXPECTED: - Change Password
        EXPECTED: - Marketing Preferences ( CORAL ) / Communication Preferences ( LADBROKES )
        EXPECTED: - Betting Settings
        """
        pass

    def test_003_tap_on_the_betting_settings_item(self):
        """
        DESCRIPTION: Tap on the 'Betting Settings' item
        EXPECTED: **Coral:**
        EXPECTED: - 'Preferences' page is opened
        EXPECTED: - 'Select Odds Format' option is present with buttons 'Fractional' and 'Decimal'
        EXPECTED: - '<' Back button is present
        EXPECTED: **Ladbrokes:**
        EXPECTED: - **Desktop** 'Account Settings' page is opened
        EXPECTED: - **Mobile** '<' Back button, avatar with balance, betslip icon are present on header
        EXPECTED: - 'Set Odds to' option is present with radio buttons 'Fractional' and 'Decimal'
        """
        pass

    def test_004_verify_default_odds_formatsetting(self):
        """
        DESCRIPTION: Verify default Odds format setting
        EXPECTED: - By default 'Fractional' button is selected, all 'Price/Odds' buttons display prices in fractional format
        EXPECTED: Note: to verify default setting cookies should be cleared
        """
        pass

    def test_005_verify__back_button(self):
        """
        DESCRIPTION: Verify '<' Back button
        EXPECTED: User gets back to the Home page
        """
        pass

    def test_006_verify_decimal_button(self):
        """
        DESCRIPTION: Verify 'Decimal' button
        EXPECTED: Switching to Decimal format will result in Prices format change across all sports (e.g. 1.70)
        EXPECTED: - Landing pages
        EXPECTED: - Event details pages
        EXPECTED: - BetSlip
        EXPECTED: - Message about price changing in the BetSlip
        EXPECTED: - Horse Race -> BetFilter-> Bet Filter Results
        """
        pass

    def test_007_verify_fractional_button(self):
        """
        DESCRIPTION: Verify 'Fractional' button
        EXPECTED: Switching to Fractional format will result in Prices format change across all sports (e.g. 7/10)
        EXPECTED: - Landing pages
        EXPECTED: - Event details pages
        EXPECTED: - BetSlip
        EXPECTED: - Message about price changing in the BetSlip
        EXPECTED: - Horse Race -> BetFilter->Bet Filter Results
        """
        pass

    def test_008_change_odds_format_and_log_out_from_the_app(self):
        """
        DESCRIPTION: Change Odds format and log out from the app
        EXPECTED: Odds format is 'remembered' and is the same after logout
        """
        pass

    def test_009_change_odds_format_open_app_in_a_new_tab_and_verify_odds_format(self):
        """
        DESCRIPTION: Change Odds format, open app in a new tab and verify Odds Format
        EXPECTED: Odds format is 'remembered' and is the same in a new tab
        """
        pass

    def test_010_change_odds_format_and_clear_cookies(self):
        """
        DESCRIPTION: Change Odds format and clear cookies
        EXPECTED: Default Odds format is set
        """
        pass
