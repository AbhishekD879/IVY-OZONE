import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C822274_Verify_Correct_Score_market_with_incomplete_data(Common):
    """
    TR_ID: C822274
    NAME: Verify Correct Score market with incomplete data
    DESCRIPTION: This test case verifies Correct Score market on Football event details page in the following cases:
    DESCRIPTION: * if all selections for Team 1 have been disabled (undisplayed or deleted)
    DESCRIPTION: * if all selections for Team 2 have been disabled (undisplayed or deleted)
    DESCRIPTION: * if all selections for both teams have been disabled (undisplayed or deleted)
    DESCRIPTION: * if all "Draw" selections have been disabled (undisplayed or deleted)
    PRECONDITIONS: There has to be a Football event with Correct Score market.
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_the_event_from_preconditions(self):
        """
        DESCRIPTION: Open event details page of the event from Preconditions
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_select_all_markets_tab(self):
        """
        DESCRIPTION: Select "All Markets" tab
        EXPECTED: "MAIN MARKETS" ( **Mobile** ) / "MAIN" ( **Desktop** ) tab is opened
        EXPECTED: First 2 sections ( **Mobile** ) / 4 sections ( **Desktop** ) are expanded by default
        """
        pass

    def test_003_verify_correct_score_section(self):
        """
        DESCRIPTION: Verify "Correct Score" section
        EXPECTED: * Pickers for Home Team and Away Team are present, active and contain data in them;
        EXPECTED: * Price/odds button next to the pickers shows valid odds;
        EXPECTED: * After expanding the section, there are 3 columns with corresponding results for "Home", "Draw" and "Away" selections
        """
        pass

    def test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(self):
        """
        DESCRIPTION: Undisplay **all** available selections related to Home Team in TI and save
        EXPECTED: Selections are undisplayed in TI
        """
        pass

    def test_005_reload_the_event_details_page_and_verify_correct_score_section(self):
        """
        DESCRIPTION: Reload the event details page and verify "Correct Score" section
        EXPECTED: * Pickers for both teams are still present and populated with data
        EXPECTED: * After expanding the section, there are only 2 columns with price/odds buttons ("Draw" and "Away Team" correspondingly)
        """
        pass

    def test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(self):
        """
        DESCRIPTION: Select in the drop-down picker any value for Home Team and a value for Away Team which satisfies the following conditions:
        DESCRIPTION: * It should **not** be a draw (e.g., NOT 1-1 or 2-2 etc.)
        DESCRIPTION: * Value selected for Away Team should be **smaller** than value selected for the Home Team (e.g., NOT 1-5 BUT 5-1)
        EXPECTED: Values are selected
        """
        pass

    def test_007_check_the_priceodds_button_next_to_the_pickers(self):
        """
        DESCRIPTION: Check the price/odds button next to the pickers
        EXPECTED: * Price/odds button is disabled
        EXPECTED: * Price/odds button shows 'N/A' text
        """
        pass

    def test_008_change_the_value_for_home_team_or_away_team_to_make_a_draw(self):
        """
        DESCRIPTION: Change the value for Home Team or Away Team to make a draw
        EXPECTED: Values are changed
        """
        pass

    def test_009_check_the_priceodds_button_next_to_the_pickers(self):
        """
        DESCRIPTION: Check the price/odds button next to the pickers
        EXPECTED: * Price/odds button is enabled
        EXPECTED: * Price/odds button shows correct price (the same as for the corresponding draw in the table below the picker when all selections are shown)
        EXPECTED: * Price/odds button can be selected and corresponding selection is added to the betslip
        """
        pass

    def test_010_change_the_value_for_away_team_to_be_greater_than_value_for_home_team(self):
        """
        DESCRIPTION: Change the value for Away Team to be **greater** than value for Home Team
        EXPECTED: Values are changed
        """
        pass

    def test_011_check_the_priceodds_button_next_to_the_pickers(self):
        """
        DESCRIPTION: Check the price/odds button next to the pickers
        EXPECTED: * Price/odds button is enabled
        EXPECTED: * Price/odds button shows correct price (the same as for the corresponding selection in the table below the picker when all selections are shown)
        EXPECTED: * Price/odds button can be selected and corresponding selection is added to the betslip
        """
        pass

    def test_012_display_back_the_selections_for_the_home_team_in_ti_and_reload_the_event_details_pageverify_correct_score_section(self):
        """
        DESCRIPTION: Display back the selections for the Home Team in TI and reload the event details page
        DESCRIPTION: Verify "Correct Score" section
        EXPECTED: * 3 columns are shown again in the table with all selections
        EXPECTED: * "N/A" text on the price/odds button next to the pickers is shown only in that case when selection is not present in the table
        EXPECTED: * Everything works in the same way as it used to work before selections were undisplayed
        """
        pass

    def test_013_repeat_steps_4_12_for_away_team(self):
        """
        DESCRIPTION: Repeat steps 4-12 for Away Team
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_4_12_for_both_teams_at_the_same_time(self):
        """
        DESCRIPTION: Repeat steps 4-12 for both teams at the same time
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_4_12_for_draw_selections(self):
        """
        DESCRIPTION: Repeat steps 4-12 for Draw selections
        EXPECTED: 
        """
        pass

    def test_016_repeat_this_test_case_all_over_again_but_this_time_delete_selections_in_ti_instead_of_undisplaying_them(self):
        """
        DESCRIPTION: Repeat this test case all over again, but this time **delete** selections in TI instead of undisplaying them
        EXPECTED: 
        """
        pass
