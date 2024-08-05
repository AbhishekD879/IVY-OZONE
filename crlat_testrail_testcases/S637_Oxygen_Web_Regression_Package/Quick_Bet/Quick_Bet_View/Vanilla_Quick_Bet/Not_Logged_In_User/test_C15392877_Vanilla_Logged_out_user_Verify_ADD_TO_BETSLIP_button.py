import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15392877_Vanilla_Logged_out_user_Verify_ADD_TO_BETSLIP_button(Common):
    """
    TR_ID: C15392877
    NAME: [Vanilla] [Logged out user] Verify 'ADD TO BETSLIP' button
    DESCRIPTION: This test case verifies 'ADD TO BETSLIP' button within Quick Bet
    DESCRIPTION: AUTOTEST: [C1143957]
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_003_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'ADD TO BETSLIP' button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        pass

    def test_004_tap_second_sportrace_selection(self):
        """
        DESCRIPTION: Tap second <Sport>/<Race> selection
        EXPECTED: * Quick Bet is NOT opened
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        pass

    def test_005_remove_all_selections_from_betslip(self):
        """
        DESCRIPTION: Remove all selections from Betslip
        EXPECTED: Betslip is closed automatically and shows 0 label
        """
        pass

    def test_006_tap_one_race_selection_with_each_way_option_available(self):
        """
        DESCRIPTION: Tap one <Race> selection with Each Way option available
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * 'E/W' checkbox is displayed within Quick Bet
        """
        pass

    def test_007_enter_value_in_stake_field_and_check_ew_checkbox(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_008_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'ADD TO BETSLIP' button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * 'Stake' field is pre-populated with the same value as on step #7
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_009_tap_second_sportrace_selection(self):
        """
        DESCRIPTION: Tap second <Sport>/<Race> selection
        EXPECTED: * Quick Bet is NOT opened
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        pass
