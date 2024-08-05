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
class Test_C1904848_Banach_Markets_with_Player_Lists_and_switcher_multiple_choice(Common):
    """
    TR_ID: C1904848
    NAME: Banach. Markets with Player Lists and switcher (multiple choice)
    DESCRIPTION: This test case verifies the display and selection rule of markets with player lists and switcher where multiple selections can added to dashboard .
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    DESCRIPTION: Related to [Format of Player Markets selections in dashboard][2]
    DESCRIPTION: [2]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2553331
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Scope of markets with Player lists with switcher where multiple selections can added to dashboard. Select available for testing:**
    PRECONDITIONS: Anytime Goalscorer, Player to score 2+ goals, To be shown a card
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True

    def test_001_expand__collapse_market_accordion_of_market_with_switcher_provided_in_the_pre_conditions(self):
        """
        DESCRIPTION: Expand / collapse market accordion of market with switcher provided in the pre-conditions
        EXPECTED: - Switcher is displayed having 2 tabs (team names)
        EXPECTED: - [Home team] tab is selected by default
        """
        pass

    def test_002_switch_between_team_tabs(self):
        """
        DESCRIPTION: Switch between team tabs
        EXPECTED: - Player selections are displayed in 2 columns, as per **selections** request
        EXPECTED: - A maximum of 6 players are displayed with the 'Show More' link in the footer when selections >6
        """
        pass

    def test_003_tap_on_show_more_link_in_the_footer_when_selections6(self):
        """
        DESCRIPTION: Tap on 'Show More' link in the footer when selections>6
        EXPECTED: The full list of all available players is displayed
        """
        pass

    def test_004_tap_on_selection_inside_home_team_tab(self):
        """
        DESCRIPTION: Tap on selection inside [Home team] tab
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection is added to the dashboard
        """
        pass

    def test_005_tap_on_the_selection_from_the_same_tab(self):
        """
        DESCRIPTION: Tap on the selection from the same tab
        EXPECTED: 2 selections in dashboard
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection is added to the dashboard
        """
        pass

    def test_006_switch_to_away_team_tab_and_tap_on_the_selection(self):
        """
        DESCRIPTION: Switch to [Away team tab] and tap on the selection
        EXPECTED: 3 selections in dashboard
        EXPECTED: - Selection from [Away team] tab is highlighted inside accordion
        EXPECTED: - Selection from [Away team] tab is added to the dashboard
        """
        pass
