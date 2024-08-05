import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.races
@vtest
class Test_C1743725_Verify_UK_Tote_Placepot_Bet_Placement(Common):
    """
    TR_ID: C1743725
    NAME: Verify UK Tote Placepot Bet Placement
    DESCRIPTION: This test case verifies bet placement on Placepot (UK tote).
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    DESCRIPTION: AUTOTEST: [C2298197]
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Placepot pool types are available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_select_placepot_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Placepot" sub-tab under "Tote" tab
        EXPECTED: * Placepot tab is selected with Leg 1 sub tab opened by default
        EXPECTED: * Placepot racecard is opened
        """
        pass

    def test_002_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: * Corresponding selections are selected for each Leg
        EXPECTED: * 'No. Lines' value is updated accordingly
        """
        pass

    def test_003_enter_valid_stake_amount_into_stake_per_line_input_field(self):
        """
        DESCRIPTION: Enter valid stake amount into 'Stake per line' input field
        EXPECTED: * Stake amount is shown in the 'Stake per line' input field
        EXPECTED: * Stake amount is shown in format <currency symbol> <stake amount value>
        EXPECTED: * 'Add to slip <currency symbol> <stake amount> TOTAL STAKE' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: * 'TOTAL STAKE' value is updated accordingly
        """
        pass

    def test_004_tap_add_to_slip_button(self):
        """
        DESCRIPTION: Tap "ADD TO SLIP" button
        EXPECTED: * Tote Placepot bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 in number
        """
        pass

    def test_005_open_betslip_and_verify_the_placepot_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Placepot tote bet
        EXPECTED: * There is a "remove" button to remove the Placepot tote bet from the betslip
        EXPECTED: * Stake field is inserted with the value user entered on bet builder
        """
        pass

    def test_006_verify_bet_details_for_placepot_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Placepot tote bet
        EXPECTED: There are the following details on Quadpot tote bet:
        EXPECTED: * "Your Selections: X" title in the section header
        EXPECTED: * "Quadpot Totepool"
        EXPECTED: * Number of lines
        EXPECTED: * Name of the each Leg
        EXPECTED: * Name of selection for each Leg
        EXPECTED: Example:
        EXPECTED: x **Placepot Totepool**
        EXPECTED: **448 Lines**
        EXPECTED: **Leg1: 1mHCap**
        EXPECTED: 1. Dr Julius No
        EXPECTED: **Leg2: 6f HCap**
        EXPECTED: 1. Rivas Rob Roy
        EXPECTED: 2. Queen of Kalahari
        """
        pass

    def test_007_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        pass

    def test_008_verify_estimated_returns(self):
        """
        DESCRIPTION: Verify "Estimated Returns"
        EXPECTED: Estimated Returns values is "N/A" for Tote bets
        """
        pass

    def test_009_verify_total_stake_and_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Stake" and "Total Est. Returns"
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        pass

    def test_010_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: * Placepot Tote bet is successfully placed
        EXPECTED: * Placepot Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'Done' buttons appear at the bottom of the page
        """
        pass

    def test_011_add_to_betslip_at_least_1_selection_and_tap_on_remove_button(self):
        """
        DESCRIPTION: Add to betslip at least 1 selection and tap on remove button
        EXPECTED: Betslip is cleared.
        """
        pass

    def test_012_select_check_boxes_from_some_of_the_legs_not_from_all_legs_and_enter_stake_into_the_stake_field(self):
        """
        DESCRIPTION: Select check boxes from some of the Legs (not from all Legs) and enter stake into the stake field
        EXPECTED: *'Add to slip' button is still inactive
        EXPECTED: * User cannot place bet
        """
        pass
