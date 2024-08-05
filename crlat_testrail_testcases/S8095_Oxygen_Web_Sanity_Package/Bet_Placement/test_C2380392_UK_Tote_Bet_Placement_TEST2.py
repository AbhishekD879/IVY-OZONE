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
class Test_C2380392_UK_Tote_Bet_Placement_TEST2(Common):
    """
    TR_ID: C2380392
    NAME: UK Tote Bet Placement [TEST2]
    DESCRIPTION: This test case verifies bet placement on UK tote pools
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * At least one pool type is available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_select_win_sub_tab_under_totepool_tab(self):
        """
        DESCRIPTION: Select 'Win' sub-tab under 'Totepool' tab
        EXPECTED: * Win tab is selected
        EXPECTED: * Win racecard is opened
        """
        pass

    def test_002_select_few_selections_win_buttons_from_the_race_card(self):
        """
        DESCRIPTION: Select few selections (win buttons) from the race card
        EXPECTED: * Selections becomes selected (green)
        EXPECTED: * Bet Builder appears at the bottom of the page
        EXPECTED: * 'N Win Selections' text appears on bet builder
        EXPECTED: Where 'N' is the number of selections user has selected
        """
        pass

    def test_003_tappress_add_to_betslip_button_on_bet_builder(self):
        """
        DESCRIPTION: Tap/press 'Add to betslip' button on bet builder
        EXPECTED: * Tote Win bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 number indicator
        """
        pass

    def test_004_open_betslip_and_check_bet_details(self):
        """
        DESCRIPTION: Open Betslip and check bet details
        EXPECTED: There are the following details on Win tote bet:
        EXPECTED: * 'Your selections: 1' text in the section header
        EXPECTED: * 'Win Totepool' with 'X' button
        EXPECTED: * 'N Win Selections' text below
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: * Time of event (eg. 15:27 Southwell Today)
        EXPECTED: * 'Total stake' value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * 'Total Potential Returns' value is 'N/A'
        """
        pass

    def test_005_presstap_place_bet_button(self):
        """
        DESCRIPTION: Press/Tap 'Place Bet' button
        EXPECTED: * Win Tote bet is successfully placed
        EXPECTED: * Win Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'Go Betting' buttons are displayed
        """
        pass

    def test_006_select_exacta_sub_tab_under_totepool_tab(self):
        """
        DESCRIPTION: Select 'Exacta' sub-tab under 'Totepool' tab
        EXPECTED: * Exacta tab is selected
        EXPECTED: * Exacta racecard is opened
        """
        pass

    def test_007_select_1st_and_2nd_check_boxes_for_any_runners_and_tap_add_to_betslip_button_at_the_bottom_of_the_page_on_bet_builder(self):
        """
        DESCRIPTION: Select '1st' and '2nd' check boxes for any runners and tap 'add to betslip' button at the bottom of the page on bet builder
        EXPECTED: * Tote Exacta bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 number indicator
        """
        pass

    def test_008_open_betslip_and_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Open 'Betslip' and verify bet details for exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: * 'Your selections: 1' text in the section header
        EXPECTED: * 'Exacta Totepool' with 'X' button
        EXPECTED: * '1 Exacta Bet'text below
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: * Time of event (eg. 15:27 Southwell Today)
        EXPECTED: * 'Total stake' value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * 'Total Potential Returns' value is 'N/A'
        """
        pass

    def test_009_insert_value_into_stake_input_field_and_presstap_place_bet_button(self):
        """
        DESCRIPTION: Insert value into stake input field and press/tap 'Place Bet' button
        EXPECTED: * Exacta Tote bet is successfully placed
        EXPECTED: * Exacta Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'Go Betting' buttons are displayed
        """
        pass

    def test_010_tappress_go_betting(self):
        """
        DESCRIPTION: Tap/Press 'Go Betting'
        EXPECTED: * 'Bet Receipt' is closed
        EXPECTED: * User is on 'Totepool' tab again
        """
        pass

    def test_011_select_3_any_check_boxes_for_some_runners_on_the_same_exacta_racecard(self):
        """
        DESCRIPTION: Select 3 'Any' check boxes for some runners on the same 'Exacta' racecard
        EXPECTED: * 3 check boxes are selected
        EXPECTED: * Bet builder appears at the bottom of the page
        EXPECTED: * '6 combination exacta bets' text appears on Bet Builder
        """
        pass

    def test_012_presstap_add_to_betslip_button_and_open_betslip(self):
        """
        DESCRIPTION: Press/Tap 'Add to betslip' button and open 'Betslip'
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: * 'Your selections: 1' text in the section header
        EXPECTED: * 'Exacta Totepool' with 'X' button
        EXPECTED: * '6 Combinations Exacta Bets' text below
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: * Time of event (eg. 15:27 Southwell Today)
        EXPECTED: * 'Total stake' value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * 'Total Potential Returns' value is 'N/A'
        EXPECTED: WHERE
        EXPECTED: '#' of lines in Combination Exacta is calculated by the formula:
        EXPECTED: No. of selections x next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        """
        pass

    def test_013_presstap_place_bet_button(self):
        """
        DESCRIPTION: Press/Tap 'Place Bet' button
        EXPECTED: * Exacta Tote bet is successfully placed
        EXPECTED: * Exacta Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'Go Betting' buttons are displayed
        """
        pass

    def test_014_select_trifecta_sub_tab_under_totepool_tab(self):
        """
        DESCRIPTION: Select "Trifecta" sub-tab under 'Totepool' tab
        EXPECTED: * Trifecta tab is selected
        EXPECTED: * Trifecta racecard is opened
        """
        pass

    def test_015_select_1st_2nd_and_3rd_check_boxes_for_any_runners_and_tap_add_to_betslip_button_in_the_trifecta_tote_bet_builder(self):
        """
        DESCRIPTION: Select '1st', '2nd' and '3rd' check boxes for any runners and tap 'Add to betslip' button in the Trifecta tote bet builder
        EXPECTED: * Tote Trifecta bets are added to betslip
        EXPECTED: * Check boxes become unselected
        EXPECTED: * Bet builder disappears
        EXPECTED: * Footer menu is shown
        EXPECTED: * Betslip counter shows 1
        """
        pass

    def test_016_verify_total_stake_and_total_potential_returns_in_betslip(self):
        """
        DESCRIPTION: Verify 'Total Stake' and 'Total Potential Returns' in Betslip
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Potential Returns value is 'N/A'
        """
        pass

    def test_017_presstap_place_bet_button(self):
        """
        DESCRIPTION: Press/Tap 'Place Bet' button
        EXPECTED: * Trifecta Tote bet is successfully placed
        EXPECTED: * Trifecta Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'Go Betting' buttons are displayed
        """
        pass

    def test_018_select_placepot_sub_tab_under_totepool_tab(self):
        """
        DESCRIPTION: Select 'Placepot' sub-tab under 'Totepool' tab
        EXPECTED: * Placepot tab is selected with 'Leg 1' sub tab opened by default
        EXPECTED: * Placepot racecard is opened
        """
        pass

    def test_019_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: * Corresponding selections are selected for each Leg
        EXPECTED: * Bet Builder appears at the bottom of the page
        EXPECTED: * 'No. Lines' value in Bet builder is updated accordingly
        EXPECTED: NOTE: Bet builder remains inactive until at least 1 check box is selected for each  Leg and stake is inserted
        """
        pass

    def test_020_enter_valid_stake_amount_into_stake_per_line_input_field_and_presstap_green_add_to_slip_button(self):
        """
        DESCRIPTION: Enter valid stake amount into 'Stake per line' input field and press/tap green 'add to slip' button
        EXPECTED: * Tote Placepot bets are added to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Footer menu is shown
        EXPECTED: * Betslip is increased by 1 in number
        """
        pass

    def test_021_open_betslip_and_verify_the_placepot_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Placepot tote bet
        EXPECTED: * The bet section is collapsed by default
        EXPECTED: * There is a 'remove' button to remove the Placepot tote bet from the betslip
        EXPECTED: * Stake field is inserted with the value user entered on bet builder
        EXPECTED: * 'Total Potential Returns' is 'N/A'
        """
        pass

    def test_022_tap_the_place_bet_button(self):
        """
        DESCRIPTION: Tap the 'Place Bet' button
        EXPECTED: * Placepot Tote bet is successfully placed
        EXPECTED: * Placepot Tote Bet receipt is shown
        EXPECTED: * 'Reuse selection' and 'Go Betting' buttons are displayed under bet info
        """
        pass
