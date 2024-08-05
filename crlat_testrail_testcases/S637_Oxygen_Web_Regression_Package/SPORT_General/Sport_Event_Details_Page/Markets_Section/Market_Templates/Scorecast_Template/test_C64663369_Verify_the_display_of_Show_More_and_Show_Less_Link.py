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
class Test_C64663369_Verify_the_display_of_Show_More_and_Show_Less_Link(Common):
    """
    TR_ID: C64663369
    NAME: Verify the display of Show More and Show Less Link
    DESCRIPTION: Verify the Score cast template
    PRECONDITIONS: Scorecast template should be configured/mapped to the event
    PRECONDITIONS: This will be a 2-phase selection template, with the first phase leading on to the second phase based on selection:
    PRECONDITIONS: Phase 1: Player Selection
    PRECONDITIONS: Phase 2: Scoreline Selection
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_any_sports__edp_page(self):
        """
        DESCRIPTION: Navigate to any sports  EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_the_markets_which_should_display_the_score_cast_template(self):
        """
        DESCRIPTION: Expand the markets which should display the Score cast Template
        EXPECTED: 1.Market Header (including signposting if applied)
        EXPECTED: -------2.Market Blurb (if applied)--OutOfScope for Now
        EXPECTED: 3.List of Player Name Links
        EXPECTED: 4.Show More Link
        EXPECTED: 5.Show Less link
        """
        pass

    def test_004_after_expanding_verify_few_player_names_will_display(self):
        """
        DESCRIPTION: After Expanding, Verify few player names will display
        EXPECTED: Few Player names should be displayed along with Show More link
        """
        pass

    def test_005_click_on_show_more_link(self):
        """
        DESCRIPTION: Click on Show More Link
        EXPECTED: Hidden list of player names link should be displayed with &gt; Arrow symbol
        EXPECTED: and Show LESS link should be displayed
        """
        pass

    def test_006_click_on_one_player_from_hidden_player_listfrom_recently_expanded_list_of_players(self):
        """
        DESCRIPTION: Click on One player from hidden player list[from recently expanded list of players]
        EXPECTED: Score line pop up page should be displayed
        """
        pass

    def test_007_click_on_show_less_link_and_verify_recently_expanded_hidden_player_names_will_be_collapsed(self):
        """
        DESCRIPTION: Click on Show LESS link and verify recently expanded hidden player names will be collapsed
        EXPECTED: hidden Player list should be collapsed other than Existing player names
        EXPECTED: and Show More link should be displayed
        """
        pass
