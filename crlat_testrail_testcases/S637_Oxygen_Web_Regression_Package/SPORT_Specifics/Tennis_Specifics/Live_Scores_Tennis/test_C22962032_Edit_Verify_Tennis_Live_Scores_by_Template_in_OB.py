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
class Test_C22962032_Edit_Verify_Tennis_Live_Scores_by_Template_in_OB(Common):
    """
    TR_ID: C22962032
    NAME: Edit Verify Tennis Live Scores by Template in OB
    DESCRIPTION: This test case verifies that Live Scores for Tennis are shown and updated through OB name template
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile [C34181740]
    DESCRIPTION: Desktop [C42446909]
    PRECONDITIONS: 1) In order to have a Scores Tennis event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attribute 'scoreboard':
    PRECONDITIONS: Verify score value for **'ALL'** (value for sets), **'CURRENT'** (value for games) and **'SUBPERIOD'** (value for points)
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: Create event in OB:
    PRECONDITIONS: Event name template:
    PRECONDITIONS: **|Player A*| (x1) x2 x3-y3 y2 (y1) |Player B|** , where x1,y1 - set scores, x2,y2 - game scores and x3,y3 - points scores
    PRECONDITIONS: e.g. |Player1 Test*| (1) 1 15-30 2 (1) |Playeyer2 Test|
    PRECONDITIONS: - '*' near player name is responsible for serving (identifies who passes the ball)
    PRECONDITIONS: - To check that scores are updated just edit the value of the score in event name
    PRECONDITIONS: - to check that serving is changed just set '*' near another player name. '*' can be set before or after player name
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    """
    keep_browser_open = True

    def test_001_load_oxygen_applicationverify_that_scores_and_serving_are_showing_and_updating_on_pages_where_scores_are_available(self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Verify that scores and serving are SHOWING and UPDATING on pages where scores are available:
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletin_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_tennis_pagesfor_desktopin_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_tennis_pages(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Tennis** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Tennis** pages
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        EXPECTED: ![](index.php?/attachments/get/36770)
        """
        pass

    def test_003_for_mobiletablethome_page__featured_tab_verify_that_scores_for_the_event_on_in_play_modulehighlight_carouselfeatured_module_created_by_type_idevent_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'Featured' tab** :
        DESCRIPTION: Verify that scores for the event on :
        DESCRIPTION: In-play module
        DESCRIPTION: Highlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        pass

    def test_004_for_mobiletablethome_page__in_play_tabhome_page__live_stream_tabfor_desktophome_page__in_play_and_live_stream_modulecheck_in_play_tab_and_live_stream_tabs(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'In Play'** tab
        DESCRIPTION: Home page > **'Live stream'** tab
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Home page > **'In play and live stream'** module
        DESCRIPTION: Check 'In-play' tab and 'Live Stream' tabs
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        EXPECTED: NOTE: on **'Life stream'** tab updates come through the push in the event name
        """
        pass

    def test_005_go_to_tennis_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Go to **Tennis Landing page > 'In Play'** tab
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        pass

    def test_006_navigate_to_tennis_landing_page__competitions_tabselect_appropriate_competition_to__event_where_scores_should_be_checked(self):
        """
        DESCRIPTION: Navigate to **Tennis Landing page > Competitions** tab
        DESCRIPTION: Select appropriate Competition to  event where scores should be checked
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        pass

    def test_007_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        EXPECTED: ![](index.php?/attachments/get/36772)
        """
        pass

    def test_008_for_desktopsports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        pass
