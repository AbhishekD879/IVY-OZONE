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
class Test_C717034_Verify_Quick_Bet(Common):
    """
    TR_ID: C717034
    NAME: Verify Quick Bet
    DESCRIPTION: This test case verifies Quick Bet view
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: The layout of Quick Bet:
    PRECONDITIONS: ![](index.php?/attachments/get/115468133)                           ![](index.php?/attachments/get/115468132)
    PRECONDITIONS: Load Oxygen app
    """
    keep_browser_open = True

    def test_001_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any Selection
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * Betslip counter does NOT increase by one
        """
        pass

    def test_002_verify_quick_bet_opening(self):
        """
        DESCRIPTION: Verify Quick Bet opening
        EXPECTED: * Quick Bet is opened with slide-in animation that begins from the bottom of the page
        EXPECTED: * Greyed-out overlay is displayed under Quick Bet
        """
        pass

    def test_003_verify_quick_bet_displaying(self):
        """
        DESCRIPTION: Verify Quick Bet displaying
        EXPECTED: Quick Bet consists of:
        EXPECTED: * Selection name
        EXPECTED: * Market name / event name
        EXPECTED: * Promo icon (LADBROKES ONLY)
        EXPECTED: * Estimated Returns ( **CORAL**) / Potential Returns ( **LADBROKES** ) for that individual bet
        EXPECTED: * Total Stake for that individual bet
        """
        pass

    def test_004_verify_greyed_out_overlay_behind_quick_bet(self):
        """
        DESCRIPTION: Verify greyed-out overlay behind Quick Bet
        EXPECTED: * Any options behind Quick Bet can not be selected
        """
        pass

    def test_005_verify_add_to_betslip_button(self):
        """
        DESCRIPTION: Verify 'ADD TO BETSLIP' button
        EXPECTED: * Quick Bet is closed after tapping 'Add to Betslip' button
        """
        pass

    def test_006_verify_login__place_betplace_bet_button(self):
        """
        DESCRIPTION: Verify 'LOGIN & PLACE BET'/'PLACE BET' button
        EXPECTED: * 'LOGIN & PLACE BET'/'PLACE BET' button is disabled by default
        EXPECTED: * 'LOGIN & PLACE BET'/'PLACE BET' button becomes enabled after entering value in 'Stake' field or using Quick Stakes
        """
        pass

    def test_007_verify_x_icon(self):
        """
        DESCRIPTION: Verify 'X' icon
        EXPECTED: * Quick Bet section is closed after tapping 'X' icon
        EXPECTED: * Selection is NOT added to Betslip
        EXPECTED: After release of BMA-54870 Expected Result will be:
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        pass

    def test_008_enter_value_in_stake_field_and_check_ew_checkbox(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_009_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Quick Bet is opened
        EXPECTED: * 'Stake' field is pre-populated with the same value as on step 7
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass
