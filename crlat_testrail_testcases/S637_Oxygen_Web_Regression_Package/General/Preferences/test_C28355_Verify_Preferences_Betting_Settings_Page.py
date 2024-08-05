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
class Test_C28355_Verify_Preferences_Betting_Settings_Page(Common):
    """
    TR_ID: C28355
    NAME: Verify Preferences/Betting Settings Page
    DESCRIPTION: This test case verifies Preferences Page
    DESCRIPTION: *Note:*
    DESCRIPTION: It's not applicable for Desktop. Should be switched off in CMS for displaying on Desktop.
    PRECONDITIONS: 1. User must be logged in
    PRECONDITIONS: 2. To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    """
    keep_browser_open = True

    def test_001_coraltap_on_avatar_iconladbrokestap_on_avatar_icon_or_balance_button(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on avatar icon
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap on avatar icon or balance button
        EXPECTED: **Coral:** / **Ladbrokes:**
        EXPECTED: 'Menu' page is opened
        """
        pass

    def test_002_tap_settings_menu_item(self):
        """
        DESCRIPTION: Tap 'Settings' menu item
        EXPECTED: **Coral:** / **Ladbrokes:**
        EXPECTED: - 'Settings' page is opened
        EXPECTED: - Header contains
        EXPECTED: - 'Settings' title
        EXPECTED: - '<' Back button
        EXPECTED: - 'X' Close button
        EXPECTED: - Menu consists of the following items:
        EXPECTED: - My Account Details
        EXPECTED: - Change Password
        EXPECTED: - Marketing Preferences ( **CORAL** ) / Communication Preferences ( **LADBROKES** )
        EXPECTED: - Betting Settings
        """
        pass

    def test_003_tap_on_the_betting_settings(self):
        """
        DESCRIPTION: Tap on the Betting Settings
        EXPECTED: Page consists of the following options:
        EXPECTED: **CORAL:**
        EXPECTED: - 'Preferences' title
        EXPECTED: - '<' Back button
        EXPECTED: - 'Select Odds Format' option is present with options 'Fractional' and 'Decimal'
        EXPECTED: - 'Allow Quick Bet' option is present with a switcher
        EXPECTED: **Native (IOS) app:**
        EXPECTED: - Touch/Face ID Login with buttons 'Enabled', 'Disabled'
        EXPECTED: - 'Diagnostics' with 'Send report' button
        EXPECTED: **LADBROKES:**
        EXPECTED: - '<' Back button, avatar with balance, betslip icon are present on header
        EXPECTED: - 'Quick Bet' option is present with a switcher
        EXPECTED: - Text 'If your betslip is empty, Quick Bet helps you place quick singles by presenting a betslip as soon as you select a price.'
        EXPECTED: - 'Set Odds to' option is present with radio buttons 'Fractional' and 'Decimal'
        EXPECTED: **Native (IOS) app:**
        EXPECTED: - Touch/Face ID or FP is present with a switcher
        EXPECTED: - Text 'Use your Touch/Face ID for quick, simple and secure login.'
        EXPECTED: - 'Diagnostics' with 'Send report' button
        """
        pass

    def test_004_coralverify_alow_quick_bet_optionladbrokesverify_quick_bet_option(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Verify 'Alow Quick Bet' option
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Verify 'Quick Bet' option
        EXPECTED: - **Coral** 'Allow Quick Bet'/ **Ladbrokes** Quick Bet' option is present if it's enabled in CMS -> 'System Configuration' section -> 'QUICKBET' item ->'Notifications' option
        EXPECTED: - **Coral** 'Allow Quick Bet'/ **Ladbrokes** Quick Bet' option is not displayed if 'Notifications' option is disabled in CMS
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: 'Back' button navigates user to the previous visited page
        """
        pass
