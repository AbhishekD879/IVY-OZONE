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
class Test_C28662_Verify_Tennis_Live_Score_of_BIP_events(Common):
    """
    TR_ID: C28662
    NAME: Verify Tennis Live Score of BIP events
    DESCRIPTION: This test case verifies Live Score of BIP events.
    DESCRIPTION: NOTE: Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 1) In order to have a Scores Tennis event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **participant_id** -  to verify player name and corresponding player score
    PRECONDITIONS: *   **period_code**='GAME', **period_index**="X" with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**='SET', **periodIndex**="X" - to look at the scorers for the specific Set (where X-set number)
    PRECONDITIONS: *   **code**='SCORE' - to see Match facts
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: 3) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: CLOCK
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='GAME', **state**='R/S', **periodIndex**="X" with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletnavigate_to_tennis_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_tennis_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Tennis' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Tennis' Landing page from the 'Left Navigation' menu
        EXPECTED: 'Tennis' landing page is opened
        """
        pass

    def test_003_clicktap_in_play_tab(self):
        """
        DESCRIPTION: Click/Tap 'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_tennis_event_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Tennis event with Game Scores available
        EXPECTED: Event is shown
        """
        pass

    def test_005_verify_game_score_displaying(self):
        """
        DESCRIPTION: Verify Game Score displaying
        EXPECTED: Each score for particular player is shown at the same row as player's name near the Price/Odds button
        """
        pass

    def test_006_verify_game_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Game Score correctness for each player
        EXPECTED: Game Score corresponds to the** 'value'** attribute from WS:
        EXPECTED: period_code="SET" level with the highest value of **period_index**
        EXPECTED: **-->**
        EXPECTED: period_code="GAME" level with the highest value of **period_index**
        """
        pass

    def test_007_verify_game_score_ordering(self):
        """
        DESCRIPTION: Verify Game Score ordering
        EXPECTED: *   Score for the home player is shown opposite the home player name (role_code="PLAYER_1")
        EXPECTED: *   Score for the away player is shown opposite the away player name (role_code="PLAYER_2")
        EXPECTED: Note: use **participant_id **for matching Player and Score
        """
        pass

    def test_008_verify_set_score_displaying(self):
        """
        DESCRIPTION: Verify set score displaying
        EXPECTED: *   Number of columns corresponds to max value of **periodIndex**
        EXPECTED: *   Set score is shown before price/odds buttons
        EXPECTED: *   Set score is shown vertically
        """
        pass

    def test_009_verify_set_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify set score correctness for each player
        EXPECTED: *   Score corresponds to the** 'value'** attribute from the WS on period_code="SET" level
        EXPECTED: *   Scores are shown from lower set to higher based on **period_index **value
        """
        pass

    def test_010_verify_set_score_ordering(self):
        """
        DESCRIPTION: Verify set score ordering
        EXPECTED: *   Score for the home player is shown on the first row (role_code="PLAYER_1")
        EXPECTED: *   Score for the away player is shown on the second row (role_code="PLAYER_2")
        EXPECTED: Note: use **eventParticipantId **for matching Player and Score
        EXPECTED: e.g.
        EXPECTED: Player1 vs Player2
        EXPECTED: Set 1 (period_index="1")
        EXPECTED: Set 2 (period_index="2")
        EXPECTED: 'value'  Player1 (role_code="PLAYER_1")
        EXPECTED: 'value'  Player1 (roleCode="PLAYER_1")
        EXPECTED: 'value' of Player2 (role_code="PLAYER_2")
        EXPECTED: 'value' of Player2 (roleCode="PLAYER_2")
        """
        pass

    def test_011_verify_set_displaying(self):
        """
        DESCRIPTION: Verify Set displaying
        EXPECTED: Number of Set is shown in format:** '<set>st/nd/th Set'**
        EXPECTED: <set> corresponds to the highest **period_index** attribute on the period_code="SET"
        """
        pass

    def test_012_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown below player names instead of Game Score
        """
        pass

    def test_013_verify_game_and_set_scores_set_number_for_outright_events(self):
        """
        DESCRIPTION: Verify Game and Set Scores, set number for Outright events
        EXPECTED: Game and Set Scores, set number are not shown for Outright events
        EXPECTED: The 'LIVE' label is displayed instead score
        """
        pass

    def test_014_for_mobiletabletnavigate_to_in_play_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'In-Play' page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' tab is shown with 'All Sport' selected
        """
        pass

    def test_015_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_016_clicktap_tennis_icon_from_the_sports_menu_ribbon_on_in_play_page(self):
        """
        DESCRIPTION: Click/Tap 'Tennis' icon from the Sports Menu Ribbon on 'In-Play' page
        EXPECTED: 'Tennis' page is opened
        """
        pass

    def test_017_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_018_for_mobiletabletnavigate_to_live_stream_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_live_stream_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Live Stream' page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Live Stream' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_019_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_020_for_mobiletablettap_in_play_tab_from_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Tap 'In-Play' tab from the Module Selector Ribbon on the Homepage
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_021_for_mobiletabletrepeat_steps_4_13(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_022_for_mobiletablettap_live_stream_tab_on_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Tap 'Live Stream' tab on the Module Selector Ribbon on the Homepage
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'Live Stream' tab is opened
        """
        pass

    def test_023_for_mobiletabletrepeat_steps_4_13(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_024_for_desktopnavigate_to_in_play__live_stream_section_at_the_homepage_by_scrolling_the_page_down(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section at the Homepage by scrolling the page down
        EXPECTED: **For Desktop:**
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * The first 'Sport' tab is selected by default
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        """
        pass

    def test_025_for_desktoprepeat_steps_4_13(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_026_for_desktopchoose_live_stream_switcher(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Choose 'Live Stream' switcher
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Live Stream' Landing Page is opened
        EXPECTED: * 'Live Stream' is selected
        """
        pass

    def test_027_for_desktoprepeat_steps_4_13(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_028_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_in_play_widget_with_live_events_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'In-Play' widget with live events is available
        EXPECTED: 'In-Play' widget is present and contains live events
        """
        pass

    def test_029_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass

    def test_030_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_live_stream_widget_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'Live Stream 'widget is available
        EXPECTED: 'Live Stream' widget is present
        """
        pass

    def test_031_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps №4-13
        EXPECTED: 
        """
        pass
