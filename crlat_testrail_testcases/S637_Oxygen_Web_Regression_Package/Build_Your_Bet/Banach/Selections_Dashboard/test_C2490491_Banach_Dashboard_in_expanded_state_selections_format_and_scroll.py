import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@vtest
class Test_C2490491_Banach_Dashboard_in_expanded_state_selections_format_and_scroll(Common):
    """
    TR_ID: C2490491
    NAME: Banach. Dashboard in expanded state, selections format and scroll
    DESCRIPTION: Test case verifies dashboard header and selections list, close and open button
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Examples of combinable Banach markets with selections:**
    PRECONDITIONS: -  without switcher Both teams to score, Total Corners, Corners Match bet, Win Either half HOME
    PRECONDITIONS: -  with switcher Match Betting [HOME or DRAW], Double Chance [HOME OR DRAW or AWAY OR DRAW]
    PRECONDITIONS: **2 Banach selections are added to the dashboard**
    PRECONDITIONS: **Dashboard is expanded**
    """
    keep_browser_open = True

    def test_001_verify_dashboard_in_expanded_state(self):
        """
        DESCRIPTION: Verify dashboard in expanded state
        EXPECTED: 1.Dashboard header:
        EXPECTED: - icon with number of selections
        EXPECTED: - BUILD YOUR BET **Coral**/BET BUILDER **Ladbrokes** text
        EXPECTED: - name of selections (in the same order they were added, separated by comma)
        EXPECTED: - "Close" label with the upside-down arrow
        EXPECTED: 2.Odds area
        EXPECTED: 3.Dashboard selections:
        EXPECTED: - Selection lines are displayed in the same order they were added
        EXPECTED: - Delete button next to each selection
        """
        pass

    def test_002_add_1_more_combinable_selection_from_marketswhere_select_1st_half_for_markets_with_switcherverify_selections_format(self):
        """
        DESCRIPTION: Add 1 more combinable selection from markets,
        DESCRIPTION: where select 1st Half for markets with switcher
        DESCRIPTION: Verify selections format
        EXPECTED: - For markets with 1st Half selection name consists of
        EXPECTED: [Market name 1st Half SELECTION NAME]
        """
        pass

    def test_003_add_1_more_combinable_selection_from_marketswhere_select_2nd_half_for_markets_with_switcher(self):
        """
        DESCRIPTION: Add 1 more combinable selection from markets,
        DESCRIPTION: where select 2nd Half for markets with switcher
        EXPECTED: - For markets with 2nd Half switcher selection name consists of
        EXPECTED: [Market name 2nd Half  SELECTION NAME]
        """
        pass

    def test_004_add_1_2_more_combinable_selection_from_markets_without_switcher(self):
        """
        DESCRIPTION: Add 1-2 more combinable selection from markets without switcher
        EXPECTED: - For markets without switcher selection name consists of
        EXPECTED: [Market name SELECTION NAME]
        """
        pass

    def test_005_add_selection_from_player_bets_market_and_verify_format(self):
        """
        DESCRIPTION: Add selection from 'Player bets' market and verify format
        EXPECTED: Selection from 'Player bets' market consists of:
        EXPECTED: - selection in the format:
        EXPECTED: [Player name]to have[statistic value range][player statistic]
        EXPECTED: - edit and delete icons next to each selection
        """
        pass

    def test_006_verify_scroll(self):
        """
        DESCRIPTION: Verify scroll
        EXPECTED: - Selections list is scrollable (scroll appears for 5 and more selections in dashboard)
        EXPECTED: - Page content with markets is not scrollable (when focus is on dashboard)
        """
        pass
