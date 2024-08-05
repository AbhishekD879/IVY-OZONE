import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2323016_Verify_UK_Tote_Scoop_6_Bet_Placement(Common):
    """
    TR_ID: C2323016
    NAME: Verify UK Tote Scoop 6 Bet Placement
    DESCRIPTION: This test case verifies bet placement on Scoop 6 tote bets (UK tote).
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Scoop 6 pool types are available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_select_scoop_6_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Scoop 6" sub-tab under "Tote" tab
        EXPECTED: * Scoop 6 tab is selected with the Leg1 sub tab opened by default
        EXPECTED: * Scoop 6 racecard is opened
        """
        pass

    def test_002_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: * All corresponding selections are selected for each Leg
        EXPECTED: * 'No. Lines' value is updated accordingly
        EXPECTED: * User can see all added selections by clicking on 'Open' link in Selection Overview widget with the option to delete each of them
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
        EXPECTED: * Tote Scoop 6 bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Footer menu is shown
        EXPECTED: * Betslip in increased by 1 number indicator
        """
        pass

    def test_005_open_betslip_and_verify_the_scoop_6_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Scoop 6 tote bet
        EXPECTED: * The bet section is collapsed by default
        EXPECTED: * It is possible to expand the tote bet by clicking on the **+** button
        EXPECTED: * There is a "remove" button to remove the Scoop 6 tote bet from the betslip
        EXPECTED: * Stake field is filled in with the value entered on bet builder
        """
        pass

    def test_006_verify_bet_details_for_scoop_6_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Scoop 6 tote bet
        EXPECTED: There are the following details on Scoop 6 tote bet:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Scoop 6 Totepool"
        EXPECTED: * Number of lines
        EXPECTED: Example:
        EXPECTED: + **Scoop 6 Totepool**
        EXPECTED: **448 Lines**
        """
        pass

    def test_007_expand_the_bet_and_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Expand the bet and verify the start date and time of the race
        EXPECTED: * Name of the each Leg is shown when the bet is expanded
        EXPECTED: * Name of selection for each Leg is shown when the bet is expanded
        EXPECTED: Example:
        EXPECTED: + **Scoop 6 Totepool**
        EXPECTED: **448 Lines**
        EXPECTED: **Leg1: 1mHCap**
        EXPECTED: 1. Dr Julius No
        EXPECTED: **Leg2: 6f HCap**
        EXPECTED: 1. Rivas Rob Roy
        EXPECTED: 2. Queen of Kalahari
        EXPECTED: etc.
        """
        pass

    def test_008_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        pass

    def test_009_verify_estimated_returns(self):
        """
        DESCRIPTION: Verify "Estimated Returns"
        EXPECTED: Estimated Returns values are "N/A" for Tote bets
        """
        pass

    def test_010_verify_total_stake_and_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Stake" and "Total Est. Returns"
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        pass

    def test_011_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: * Scoop 6 Tote bet is successfully placed
        EXPECTED: * Scoop 6 Tote Bet receipt is shown
        EXPECTED: * 'Reuse election' and 'Done' buttons are displayed at the bottom of the page
        """
        pass

    def test_012_add_to_betslip_at_least_1_selection_and_tap_on_remove_button(self):
        """
        DESCRIPTION: Add to betslip at least 1 selection and tap on remove button
        EXPECTED: * Betslip is cleared
        EXPECTED: * Check boxes become unselected on race card
        """
        pass

    def test_013_select_check_boxes_for_only_some_of_the_legs_not_all_of_them_and_enter_valid_stake_into_the_stake_input_field(self):
        """
        DESCRIPTION: Select check boxes for only some of the Legs (not all of them) and enter valid stake into the stake input field
        EXPECTED: User is unable to place bet as the 'Add to slip' button is inactive
        """
        pass

    def test_014_select_some_checkboxes_for_the_rest_of_legs_and_click_add_to_slip_button(self):
        """
        DESCRIPTION: Select some checkboxes for the rest of Legs and click 'Add to slip' button
        EXPECTED: * 'Add to slip' button is active
        EXPECTED: * Tote Scoop 6 bets are added to betslip
        EXPECTED: * Selected checkboxes become unselected
        """
        pass
