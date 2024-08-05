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
class Test_C2291613_Verify_UK_Tote_Trifecta_Bet_Placement(Common):
    """
    TR_ID: C2291613
    NAME: Verify UK Tote Trifecta Bet Placement
    DESCRIPTION: This test case verifies bet placement on Trifecta UK tote bets
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    DESCRIPTION: AUTOTEST: [C2298055]
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Trifecta pool types are available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_select_trifecta_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Trifecta" sub-tab under "Tote" tab
        EXPECTED: * Trifecta tab is selected
        EXPECTED: * Trifecta racecard is opened
        """
        pass

    def test_002_select_1st_2nd_and_3rd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st", "2nd" and "3rd" check boxes for any runners
        EXPECTED: * Selections are added to the Trifecta tote bet builder
        EXPECTED: * "ADD TO BETSLIP" button becomes enabled in the bet builder
        EXPECTED: * 'Clear Selections' link is displayed right before 'Add to betslip' button
        EXPECTED: * Corresponding bet type name is shown in the bet builder
        """
        pass

    def test_003_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap "ADD TO BETSLIP" button
        EXPECTED: * Tote Trifecta bets are added to betslip
        EXPECTED: * Check boxes become unselected
        EXPECTED: * Bet builder disappears
        EXPECTED: * Footer menu appears
        EXPECTED: * Betslip counter shows 1
        """
        pass

    def test_004_open_betslip_and_verify_the_trifecta_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Trifecta tote bet
        EXPECTED: * There is a "X" remove and "Remove all" button to remove the Trifecta tote bet from the betslip
        EXPECTED: * 'Bet now' button is disabled
        """
        pass

    def test_005_verify_bet_details_for_trifecta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Trifecta tote bet
        EXPECTED: There are the following details on Trifecta tote bet:
        EXPECTED: * "Your Selections: 1" label in the section header
        EXPECTED: * "Trifecta Totepool"
        EXPECTED: * "Trifecta" bet type name
        EXPECTED: * All selections with correct order according to the selected check boxes
        """
        pass

    def test_006_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Verify the start date and time of the race
        EXPECTED: * Time of the race is shown when the bet is expanded
        EXPECTED: * Format is the following:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        """
        pass

    def test_007_enter_valid_stake_into_the_stake_field_and_press_bet_now_button(self):
        """
        DESCRIPTION: Enter valid stake into the stake field and press 'Bet now' button
        EXPECTED: * 'Bet now' button is active and clickable
        EXPECTED: * Stake is successfully placed
        EXPECTED: * Trifecta Tote Bet receipt is shown
        """
        pass

    def test_008_add_some_selections_to_betslip_and_tap_the_remove_button_in_the_betslip(self):
        """
        DESCRIPTION: Add some selections to betslip and tap the "remove" button in the betslip
        EXPECTED: Bet is removed from the betslip
        """
        pass

    def test_009_select_1st_and_2ndcheck_boxes_for_any_runner(self):
        """
        DESCRIPTION: Select "1st" and "2nd"check boxes for any runner
        EXPECTED: * Bet builder is shown but 'Add to betslip' button is inactive
        EXPECTED: * 3d option check boxes are active except for those runners who have 1st and 2nd already selected
        """
        pass

    def test_010_clear_selections_and_select_2_or_less_checkboxes_from_any_option(self):
        """
        DESCRIPTION: Clear selections and select 2 or less checkboxes from 'Any' option
        EXPECTED: * Bet builder is shown but 'Add to betslip' button is inactive
        EXPECTED: * All other check boxes from 'Any' option are active
        EXPECTED: * All 1st and 2nd check boxes are disabled
        """
        pass

    def test_011_select_any_3_runners_from_any_option_and_tap_add_to_betslip_button_in_the_trifecta_tote_bet_builder(self):
        """
        DESCRIPTION: Select any 3 runners from "Any" option and tap "ADD TO BETSLIP" button in the Trifecta tote bet builder
        EXPECTED: * Tote Trifecta bets are added to betslip
        EXPECTED: * Check boxes become unselected
        EXPECTED: * Bet builder disappears
        EXPECTED: * Footer menu is shown
        EXPECTED: * Betslip counter shows 1
        """
        pass

    def test_012_verify_bet_details_for_trifecta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Trifecta tote bet
        EXPECTED: There are the following details on Trifecta tote bet:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Trifecta Totepool"
        EXPECTED: * ""x Combination Trifecta Bets" bet type name
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: WHERE
        EXPECTED: '#' of lines inCombination Trifecta is calculated by the formula:
        EXPECTED: No. of selections x next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        """
        pass

    def test_013_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        pass

    def test_014_verify_estimated_returns(self):
        """
        DESCRIPTION: Verify "Estimated Returns"
        EXPECTED: Estimated Returns values are "N/A" for Tote bets
        """
        pass

    def test_015_verify_total_stake_and_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Stake" and "Total Est. Returns"
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        pass

    def test_016_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: * Trifecta Tote bet is successfully placed
        EXPECTED: * Trifecta Tote Bet receipt is shown
        """
        pass
