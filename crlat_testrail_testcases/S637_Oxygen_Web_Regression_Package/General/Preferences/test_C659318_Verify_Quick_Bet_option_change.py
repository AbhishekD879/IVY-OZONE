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
class Test_C659318_Verify_Quick_Bet_option_change(Common):
    """
    TR_ID: C659318
    NAME: Verify 'Quick Bet' option change
    DESCRIPTION: This test case verifies 'Quick Bet' option change within 'Preferences' page (Coral)/ Settings (Ladbrokes)
    DESCRIPTION: AUTOTEST [C2592714]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. 'Quick Bet' functionality is enabled in CMS
    PRECONDITIONS: 3. 'Quick Bet' functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_coraltap_on_avatar_icon___settings___betting_settingsladbrokestap_on_avatar_icon_or_balance_button___settings___betting_settings(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on avatar icon -> Settings -> Betting Settings
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap on avatar icon or balance button -> Settings -> Betting Settings
        EXPECTED: **Coral:**
        EXPECTED: * 'Preferences' page is opened
        EXPECTED: * 'Allow Quick Bet' option is present
        EXPECTED: **Ladbrokes:**
        EXPECTED: * Settings page is opened
        EXPECTED: * 'Quick Bet' option is present
        EXPECTED: * Text 'If your betslip is empty, Quick Bet helps you place quick singles by presenting a betslip as soon as you select a price.' is present
        """
        pass

    def test_002_coralverify_default_value_set_for_allow_quick_bet_optionladbrokesverify_default_value_set_for_quick_bet_option(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Verify default value set for 'Allow Quick Bet' option
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Verify default value set for 'Quick Bet' option
        EXPECTED: Default value is 'ON'
        """
        pass

    def test_003_go_to_any_sportrace_page_and_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any <Sport>/<Race> page and add one selection to Betslip
        EXPECTED: 'Quick Bet' section is displayed at the bottom of the page immediately
        """
        pass

    def test_004_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip
        EXPECTED: 'Quick Bet' section is NOT displayed anymore
        """
        pass

    def test_005_coraltap_on_avatar_icon___settings___betting_settingsladbrokestap_on_avatar_icon_or_balance_button___settings___betting_settings(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on avatar icon -> Settings -> Betting Settings
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap on avatar icon or balance button -> Settings -> Betting Settings
        EXPECTED: 
        """
        pass

    def test_006_coralset_allow_quick_bet_option_to_offladbrokesset_quick_bet_option_to_off(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Set 'Allow Quick Bet' option to 'OFF'
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Set 'Quick Bet' option to 'OFF'
        EXPECTED: Value set to 'OFF'
        """
        pass

    def test_007_go_to_any_sportrace_page_and_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any <Sport>/<Race> page and add one selection to Betslip
        EXPECTED: - 'Quick Bet' section is NOT displayed at the bottom of the page immediately
        EXPECTED: - Selection is added to Betslip
        """
        pass
