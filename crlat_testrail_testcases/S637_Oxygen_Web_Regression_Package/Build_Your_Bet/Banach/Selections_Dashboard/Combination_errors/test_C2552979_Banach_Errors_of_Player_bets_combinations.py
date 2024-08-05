import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2552979_Banach_Errors_of_Player_bets_combinations(Common):
    """
    TR_ID: C2552979
    NAME: Banach. Errors of Player bets combinations
    DESCRIPTION: This test case verifies error when user adds Player bets selections which cannot be combined to dashboard
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: * BYB **Coral**/Bet Builder **Ladbrokes** tab on event details page is loaded
    PRECONDITIONS: * Player Bet selection is added to the dashboard, e.g. Player 1 to have 2+Shots on Goals
    """
    keep_browser_open = True

    def test_001_add_one_more_player_bet_selection_to_dashboard_with_the_same_player_statistic_type_and_statistic_valueeg_player_1_to_have_2plusshots_on_goals(self):
        """
        DESCRIPTION: Add one more Player Bet selection to dashboard with the same player, statistic type and statistic value
        DESCRIPTION: (e.g. Player 1 to have 2+Shots on Goals)
        EXPECTED: * Selection is added to Dashboard
        EXPECTED: * Error message 'There are selections that cannot be combined in the dashboard' appears above Dashboard
        EXPECTED: * 'Place bet' button with price is hidden from Dashboard
        EXPECTED: * Both selections have error icon on the left
        """
        pass

    def test_002_edit_statistic_value_for_one_of_the_selectionseg_player_1_to_have_3plusshots_on_goals(self):
        """
        DESCRIPTION: Edit statistic value for one of the selections
        DESCRIPTION: (e.g. Player 1 to have 3+Shots on Goals)
        EXPECTED: * Error message 'There are selections that cannot be combined in the dashboard' appears above Dashboard
        EXPECTED: * 'Place bet' button with price is hidden from Dashboard
        """
        pass

    def test_003_edit_statistic_type_for_one_of_the_selectionseg_player_1_to_have_3plusgoals(self):
        """
        DESCRIPTION: Edit statistic type for one of the selections
        DESCRIPTION: (e.g. Player 1 to have 3+Goals)
        EXPECTED: * Error message disappears
        EXPECTED: * 'Place bet' button with price appears again
        EXPECTED: * Two selections are in normal view without any error icon
        """
        pass

    def test_004_revert_changes_for_statistic_type_to_be_like_in_step_3eg_player_1_to_have_3plusshots_on_goals(self):
        """
        DESCRIPTION: Revert changes for statistic type to be like in step 3
        DESCRIPTION: (e.g. Player 1 to have 3+Shots on Goals)
        EXPECTED: * Error message 'There are selections that cannot be combined in the dashboard' appears above Dashboard
        EXPECTED: * 'Place bet' button with price is hidden from Dashboard
        """
        pass

    def test_005_change_player_for_one_of_the_selectionseg_player_2_to_have_3plusgoals(self):
        """
        DESCRIPTION: Change Player for one of the selections
        DESCRIPTION: (e.g. Player 2 to have 3+Goals)
        EXPECTED: * Error message disappears
        EXPECTED: * 'Place bet' button with price appears again
        EXPECTED: * Two selections are in normal view without any error icon
        """
        pass

    def test_006_add_2_more_selections_which_are_conflictingeg_player_3_to_have_45pluspassesplayer_3_to_have_have_47pluspasses(self):
        """
        DESCRIPTION: Add 2 more selections which are conflicting
        DESCRIPTION: (e.g. Player 3 to have 45+Passes
        DESCRIPTION: Player 3 to have have 47+Passes)
        EXPECTED: * Selections are added to the dashboard
        EXPECTED: * Error message 'There are selections that cannot be combined in the dashboard' appears above Dashboard
        EXPECTED: * 'Place bet' button with price is hidden from Dashboard
        """
        pass

    def test_007_remove_one_of_the_conflicting_selectionseg_player_3_to_have_have_47pluspasses(self):
        """
        DESCRIPTION: Remove one of the conflicting selections
        DESCRIPTION: (e.g Player 3 to have have 47+Passes)
        EXPECTED: * Error message disappears
        EXPECTED: * 'Place bet' button with price appears again
        EXPECTED: * 3 selections are in normal view without any error icon
        """
        pass
