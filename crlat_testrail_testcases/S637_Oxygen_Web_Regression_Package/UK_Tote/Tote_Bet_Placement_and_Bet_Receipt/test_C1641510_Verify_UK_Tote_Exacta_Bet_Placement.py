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
class Test_C1641510_Verify_UK_Tote_Exacta_Bet_Placement(Common):
    """
    TR_ID: C1641510
    NAME: Verify UK Tote Exacta Bet Placement
    DESCRIPTION: This test case verifies bet placement on Exacta UK tote
    DESCRIPTION: AUTOTEST [C2099837]
    DESCRIPTION: AUTOTEST [C2108789]
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Exacta/Trifecta pool types are available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_select_exacta_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Exacta" sub-tab under "Tote" tab
        EXPECTED: * Exacta tab is selected
        EXPECTED: * Exacta racecard is opened
        """
        pass

    def test_002_select_1st_and_2nd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st" and "2nd" check boxes for any runners
        EXPECTED: * Selections are added to the Exacta tote bet builder
        EXPECTED: * "ADD TO BETSLIP" button becomes enabled in the bet builder
        EXPECTED: * Corresponding bet type name is shown in the bet builder
        """
        pass

    def test_003_tap_on_clear_selections_in_bet_builder(self):
        """
        DESCRIPTION: Tap on 'Clear Selections' in bet builder
        EXPECTED: * All selected checkboxes become unselected
        EXPECTED: * Bet builder disappear
        EXPECTED: * Footer menu is shown
        """
        pass

    def test_004_select_both_1st_and_2nd_check_boxed_once_again_and_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Select both 1st and 2nd check boxed once again and tap "ADD TO BETSLIP" button
        EXPECTED: * Tote Exacta bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 number indicator
        """
        pass

    def test_005_open_betslip_and_verify_the_exacta_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Exacta tote bet
        EXPECTED: * The bet is present
        EXPECTED: * There is a "remove" button to remove the exacta tote bet from the betslip
        """
        pass

    def test_006_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: * "Your selections: 1" label in the section header
        EXPECTED: * "Exacta Totepool"
        EXPECTED: * "Exacta" bet type name
        EXPECTED: * All selections with correct order according to the selected check boxes
        EXPECTED: * Time of the race is shown is the following format:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        """
        pass

    def test_007_clicktap_the_remove_button(self):
        """
        DESCRIPTION: Click/Tap the "remove" button
        EXPECTED: Bet is removed from the betslip
        """
        pass

    def test_008_select_a_couple_of_any_check_boxes_and_tap_add_to_betslip_button_in_the_exacta_tote_bet_builder(self):
        """
        DESCRIPTION: Select a couple of "Any" check boxes and tap "ADD TO BETSLIP" button in the Exacta tote bet builder
        EXPECTED: * Tote Exacta bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 number indicator
        """
        pass

    def test_009_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: * "Your selections: 1" label in the section header
        EXPECTED: * "Exacta Totepool"
        EXPECTED: * 'Reverse exacta bet' (if 2 selection are added) or "X Combination Exacta Bets" bet type name (due to # of checkboxes selected)
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: WHERE
        EXPECTED: '#' of lines inCombination Exacta is calculated by the formula:
        EXPECTED: No. of selections x next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        EXPECTED: * Time of the race is shown is the following format:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        """
        pass

    def test_010_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        pass

    def test_011_verify_estimated_returnspot_returns_coralladbrokes(self):
        """
        DESCRIPTION: Verify "Estimated Returns"/"Pot. Returns:" (Coral/Ladbrokes)
        EXPECTED: Estimated Returns values are "N/A" for Tote bets
        """
        pass

    def test_012_verify_total_stake_and_total_est_returnstotal_potential_returns__coralladbrokes(self):
        """
        DESCRIPTION: Verify "Total Stake" and "Total Est. Returns"/"Total Potential Returns"  (Coral/Ladbrokes)
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        pass

    def test_013_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: * Exacta Tote bet is successfully placed
        EXPECTED: * Exacta Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'GO BETTING' buttons are displayed at the bottom
        """
        pass
