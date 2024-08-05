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
class Test_C60092367_Verify_that_team_is_pre_populated_on_clicking_the_deep_link_URL(Common):
    """
    TR_ID: C60092367
    NAME: Verify that team is pre-populated on clicking the deep link URL
    DESCRIPTION: Verify that team is pre-populated on clicking the deep link URL
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Deep Link URL should be generated as promotion for the Users
    """
    keep_browser_open = True

    def test_001_load_the_app_or_url(self):
        """
        DESCRIPTION: Load the app or URL
        EXPECTED: User should be able to launch the URL
        EXPECTED: Mobile App: User should be able to launch the app
        """
        pass

    def test_002_navigate_to_promotions_and_click_on_the_promotion_for_5_a_side_with_advertised_teamvalidate_the_url(self):
        """
        DESCRIPTION: Navigate to Promotions and click on the promotion for 5-A side with advertised team.
        DESCRIPTION: Validate the URL
        EXPECTED: 1: User should be navigated to the Pitch View pre-populated with the 5-A Side team
        EXPECTED: 2: URL should contain the formation and places for all 5 players
        EXPECTED: 3: The exact team advertised with player positions ,Stats and formations should be displayed as per the generated deep link
        EXPECTED: 4: Odds should be displayed with Place bet enabled
        """
        pass

    def test_003_verify_the_user_is_able_to_place_bet(self):
        """
        DESCRIPTION: Verify the User is able to place bet
        EXPECTED: User should be able to place bet successfully
        """
        pass
