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
class Test_C2552944_Banach_Correct_score_market_layout_and_scroll(Common):
    """
    TR_ID: C2552944
    NAME: Banach. Correct score market layout and scroll
    DESCRIPTION: Test case verifies display of Correct score market, drop downs value selection, Show All/Less button, selected value display in selections grid
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    DESCRIPTION: Related to [Format of Correct score selections][2]
    DESCRIPTION: [2]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490706
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **CORRECT SCORE market is present on Build Your Bet tab**
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True

    def test_001_tap_on_market_header_correct_score(self):
        """
        DESCRIPTION: Tap on market header 'CORRECT SCORE'
        EXPECTED: - Market accordion is expanded
        EXPECTED: - Three switcher tabs are displayed:
        EXPECTED: * '90 MIN' (selected by default)
        EXPECTED: * '1ST HALF'
        EXPECTED: * '2ND HALF'
        """
        pass

    def test_002_tap_on_each_tab_of_the_switchers_90_min__1st_half__2nd_half(self):
        """
        DESCRIPTION: Tap on each tab of the switchers '90 MIN' / '1ST HALF' / '2ND HALF'.
        EXPECTED: - Two drop down menus under the [Home/away] team names are displayed
        EXPECTED: - ADD TO BET button as per the GD.
        EXPECTED: - "Show All" button is displayed underneath the score drop-downs
        """
        pass

    def test_003_in_90_mins_switcher_tab_select_the_following_score_43_and_tap_add_to_bet_button(self):
        """
        DESCRIPTION: In "90 mins" switcher tab select the following score: 4:3 and tap ADD TO BET button
        EXPECTED: "4:3" selection is added to dashboard
        """
        pass

    def test_004_expand_grid_of_selections_by_tapping_show_all_buttonscroll_until_value_43(self):
        """
        DESCRIPTION: Expand grid of selections by tapping "Show All" button
        DESCRIPTION: Scroll until value "4:3"
        EXPECTED: - Selections grid is expanded and scrollable
        EXPECTED: - Selection "4:3" is highlighted in the first (Home) part of the grid
        """
        pass

    def test_005_switch_to_1st_half_tab(self):
        """
        DESCRIPTION: Switch to "1st half" tab
        EXPECTED: - Tab is switched
        EXPECTED: - Selections grid is expanded
        EXPECTED: - "Show less" button is displayed
        """
        pass

    def test_006_tap_on_show_less_button(self):
        """
        DESCRIPTION: Tap on "Show Less" button
        EXPECTED: - Selections grid is collapsed
        EXPECTED: - "Show All" button is shown
        """
        pass
