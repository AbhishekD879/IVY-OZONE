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
class Test_C2552945_Banach_Correct_score_market_selection_rule(Common):
    """
    TR_ID: C2552945
    NAME: Banach. Correct score market selection rule
    DESCRIPTION: Test case verifies rules of adding selections to dashboard in Correct score market
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    DESCRIPTION: Related to [Format of Correct score selections][2]
    DESCRIPTION: [2]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490706
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: To check error when selections cannot be combined check **price** request > "responseMessage" parameter
    PRECONDITIONS: **CORRECT SCORE is present on 'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab**
    PRECONDITIONS: **Correct score market is expanded and no selections are added to dashboard**
    """
    keep_browser_open = True

    def test_001_in_90_mins_switcher_tab_inside_market_select_the_following_score_in_the_drop_downs_43_and_tap_add_to_bet_button(self):
        """
        DESCRIPTION: In "90 mins" switcher tab inside market select the following score in the drop-downs: 4:3 and tap ADD TO BET button
        EXPECTED: "4:3" selection is added to dashboard
        """
        pass

    def test_002_in_the_same_switcher_tab_select_the_following_score_in_the_drop_downs_42(self):
        """
        DESCRIPTION: In the same switcher tab select the following score in the drop-downs: "4:2"
        EXPECTED: Selection "4:3" is substituted with selection "4:2" in dashboard
        """
        pass

    def test_003_tap_on_show_all_button_scroll_and_check_selected_values_in_the_grid(self):
        """
        DESCRIPTION: Tap on "Show All" button, scroll and check selected values in the Grid
        EXPECTED: - Selection "4:2" is highlighted
        EXPECTED: - Selection "4:3" is not highlighted
        """
        pass

    def test_004_switch_to_1st_half_tab_and_select_the_following_value_from_the_selections_grid_34(self):
        """
        DESCRIPTION: Switch to "1st half" tab and select the following value from the selections Grid: "3:4"
        EXPECTED: Combination error message taken from the **price** request is displayed above dashboard
        """
        pass

    def test_005_select_the_following_value_from_the_1st_half_grid_32(self):
        """
        DESCRIPTION: Select the following value from the "1st half" Grid: "3:2"
        EXPECTED: - Selection "3:4" is substituted with selection ""3:2"
        EXPECTED: - Error message disappears
        """
        pass
