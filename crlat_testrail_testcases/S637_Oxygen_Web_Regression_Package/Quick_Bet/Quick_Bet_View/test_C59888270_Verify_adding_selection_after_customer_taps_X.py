import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C59888270_Verify_adding_selection_after_customer_taps_X(Common):
    """
    TR_ID: C59888270
    NAME: Verify adding selection after customer taps X
    DESCRIPTION: BMA-54870 Quickbet - Add selection if customer taps X
    DESCRIPTION: This Test case verifies that, after customer taps 'X' Button on Quick bet, Quick bet is closed and Selection is added to Betslip
    DESCRIPTION: Before the release of this feature, tapping on 'X' will close Quick bet, without adding selection to Betslip
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in/logged out
    PRECONDITIONS: (Test for logged in and logged out user)
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_002_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        pass

    def test_003_go_to_betslip_verify_added_selection(self):
        """
        DESCRIPTION: Go to Betslip. Verify added Selection
        EXPECTED: Selection is the same as was added by Quick bet
        """
        pass

    def test_004_remove_all_selections_from_betslip(self):
        """
        DESCRIPTION: Remove all selections from Betslip
        EXPECTED: Betslip is empty
        """
        pass

    def test_005_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_006_add_any_stake(self):
        """
        DESCRIPTION: Add any Stake
        EXPECTED: 'Stake' field contains added value
        """
        pass

    def test_007_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is the same as was added by Quick bet
        EXPECTED: * 'Stake' field contains added value from Quick bet
        """
        pass

    def test_008_tap_one_on_race_selection_with_each_way_option_available(self):
        """
        DESCRIPTION: Tap one on 'Race' selection with Each Way option available
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_009_add_any_stake_and_check_ew_checkbox(self):
        """
        DESCRIPTION: Add any Stake and check 'E/W' checkbox
        EXPECTED: * 'Stake' field contains added value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_010_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is the same as was added by Quick bet
        EXPECTED: * 'Stake' field contains added value from Quick bet
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass
