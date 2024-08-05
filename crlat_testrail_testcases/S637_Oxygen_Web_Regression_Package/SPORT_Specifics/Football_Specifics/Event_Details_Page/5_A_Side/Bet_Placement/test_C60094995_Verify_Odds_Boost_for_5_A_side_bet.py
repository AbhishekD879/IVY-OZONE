import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C60094995_Verify_Odds_Boost_for_5_A_side_bet(Common):
    """
    TR_ID: C60094995
    NAME: Verify Odds Boost for 5 A side bet
    DESCRIPTION: Verify the display of Odds Boost on 5-A Side pitch view
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: User should have Odds Boost available
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_app(self):
        """
        DESCRIPTION: Launch Ladbrokes app
        EXPECTED: User should be able launch the application successfully
        """
        pass

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: User should be navigated to Football landing page
        """
        pass

    def test_003_navigate_to_any_football_event_that_has_5_a_side_available(self):
        """
        DESCRIPTION: Navigate to any football event that has 5-A side available
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_004_navigate_to_5_a_side_tab(self):
        """
        DESCRIPTION: Navigate to 5-A Side tab
        EXPECTED: User should be navigated to 5-A Side tab
        """
        pass

    def test_005_click_on_build_a_team(self):
        """
        DESCRIPTION: Click on Build a Team
        EXPECTED: 1: Pitch View should be displayed
        EXPECTED: 2: Balanced formation should be selected by default
        EXPECTED: 3: User should be able to select any formation displayed in the pitch view
        """
        pass

    def test_006_1_pick_formations2_select_players3_choose_stats_and_build_the_team(self):
        """
        DESCRIPTION: 1: Pick Formations
        DESCRIPTION: 2: Select Players
        DESCRIPTION: 3: Choose Stats and build the team
        EXPECTED: 1: User should be navigated to pitch view with selected formation,players,stats.
        EXPECTED: 2: Place Bet should be displayed and enabled
        EXPECTED: 3: Odds should be displayed
        EXPECTED: 4: Before Odds display Odds boost should be displayed (If available for the user)
        """
        pass

    def test_007_click_on_boostindexphpattachmentsget122312635(self):
        """
        DESCRIPTION: Click on Boost
        DESCRIPTION: ![](index.php?/attachments/get/122312635)
        EXPECTED: 1: Boosted should be displayed
        EXPECTED: 2: Odds should be updated with previous odds striked
        """
        pass

    def test_008_click_on_boostedindexphpattachmentsget122312634(self):
        """
        DESCRIPTION: Click on Boosted
        DESCRIPTION: ![](index.php?/attachments/get/122312634)
        EXPECTED: 1: Boost should  be displayed
        EXPECTED: 2: Odds should be displayed
        """
        pass

    def test_009_boost_the_odds_and_place_bet(self):
        """
        DESCRIPTION: Boost the odds and Place bet
        EXPECTED: User should be able to place the 5-A side bet successfully
        """
        pass

    def test_010_validate_the_above_in_mobile_app_and_web(self):
        """
        DESCRIPTION: Validate the above in mobile app and web
        EXPECTED: User should be able to place the 5-A side bet successfully
        """
        pass
