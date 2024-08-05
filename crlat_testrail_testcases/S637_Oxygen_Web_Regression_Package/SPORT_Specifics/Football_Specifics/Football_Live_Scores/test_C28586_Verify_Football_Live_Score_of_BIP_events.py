import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28586_Verify_Football_Live_Score_of_BIP_events(Common):
    """
    TR_ID: C28586
    NAME: Verify Football Live Score of BIP events
    DESCRIPTION: This test case verifies Live Score of BIP events.
    DESCRIPTION: NOTE: Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 1) In order to have a Scores Football event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **participant_id** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **period_code**='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: *   **period_code**='FIRST_HALF/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF'** - to look at the scorers for the specific time
    PRECONDITIONS: *   **code**='SCORE'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletnavigate_to_football_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_football_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Football' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Football' Landing page from the 'Left Navigation' menu
        EXPECTED: 'Football' landing page is opened
        """
        pass

    def test_003_tap_on_in_play_tab(self):
        """
        DESCRIPTION: Tap on **'In-Play'** tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_football_event_with_scores_available(self):
        """
        DESCRIPTION: Verify Football event with scores available
        EXPECTED: Event is shown
        """
        pass

    def test_005_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Each score for particular team is shown in the same row as team's name near the Price/Odds button
        """
        pass

    def test_006_verify_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify score correctness for each team
        EXPECTED: Score corresponds to the** 'value'** attribute from WS
        """
        pass

    def test_007_verify_score_ordering(self):
        """
        DESCRIPTION: Verify score ordering
        EXPECTED: *   Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: *   Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: Note: use **participant_id ** for matching Team and Score
        """
        pass

    def test_008_verify_live_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify live event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown
        EXPECTED: Scores are not shown
        """
        pass

    def test_009_verify_game_score_for_outright_events(self):
        """
        DESCRIPTION: Verify Game Score for Outright events
        EXPECTED: Game Score is not shown for Outright events
        EXPECTED: The 'LIVE' label is displayed instead
        """
        pass

    def test_010_repeat_steps_4_9_on_next_pages(self):
        """
        DESCRIPTION: Repeat steps №4-9 on next pages:
        EXPECTED: 
        """
        pass

    def test_011_for_mobiletabletin_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_football_pagesfor_desktopin_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_football_pages(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Football** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Football** pages
        EXPECTED: 
        """
        pass

    def test_012_for_mobiletablethome_page__featured_tab_in_play_modulehightlight_carouselfeatured_module_created_by_type_idevent_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > 'Featured' tab :
        DESCRIPTION: In-play module
        DESCRIPTION: Hightlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        EXPECTED: 
        """
        pass

    def test_013_for_mobiletablethome_page__in_play_tabhome_page__live_stream_tabfor_desktophome_page__in_play_and_live_stream_modulecheck_in_play_tab_and_live_stream_tabs(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > In Play tab
        DESCRIPTION: Home page > Live stream tab
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Home page > In play and live stream module
        DESCRIPTION: Check 'In-play' tab and 'Live Stream' tabs
        EXPECTED: 
        """
        pass

    def test_014_for_desktopsports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: 
        """
        pass

    def test_015_navigate_to_edp_of_appropriate_event(self):
        """
        DESCRIPTION: Navigate to EDP of appropriate event
        EXPECTED: 
        """
        pass

    def test_016_place_bet_on_appropriate_events_as_in_steps_4_9navigate_to_my_betsopen_betscashout_and_settled_bets_tabsrepeat_steps_4_9(self):
        """
        DESCRIPTION: Place bet on appropriate events as in steps #4-9
        DESCRIPTION: Navigate to **My bets>Open bets/Cashout and Settled bets** tabs
        DESCRIPTION: Repeat steps №4-9
        EXPECTED: 
        """
        pass
