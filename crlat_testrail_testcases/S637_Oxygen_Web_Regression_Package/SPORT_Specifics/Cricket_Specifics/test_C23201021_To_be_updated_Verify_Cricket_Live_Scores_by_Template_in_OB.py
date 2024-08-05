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
class Test_C23201021_To_be_updated_Verify_Cricket_Live_Scores_by_Template_in_OB(Common):
    """
    TR_ID: C23201021
    NAME: [To be updated] Verify Cricket Live Scores by Template in OB
    DESCRIPTION: To be updated - should be added new screenshots for each page
    DESCRIPTION: This test case verifies that Live Score for Cricket are shown and updated through OB name template
    DESCRIPTION: AUTO TEST MOBILE: [C42668746]
    DESCRIPTION: DESKTOP: [C43885005]
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attribute scoreboard:
    PRECONDITIONS: Look at the attribute 'scoreboard':
    PRECONDITIONS: Verify score value for **'ALL'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: Create event in OB:
    PRECONDITIONS: Event name template can be different (integer and fractional):
    PRECONDITIONS: **|Team A| x1-y2 |Team B|**
    PRECONDITIONS: **|Team A| x1 v |Team B| y1/y2**
    PRECONDITIONS: **|Team A| x1/x2 v |Team B| y1**
    PRECONDITIONS: **|Team A| x1/x2 v |Team B| y1/y2**
    PRECONDITIONS: **|Team A| x1 v |Team B| y1 y2/y3**
    PRECONDITIONS: **|Team A| x1 x2/x3 v |Team B| y1**
    PRECONDITIONS: **|Team A| x1 x2/x3 v |Team B| y1 y2/y3**
    PRECONDITIONS: e.g.
    PRECONDITIONS: **|Team A| 1-0 |Team B|**
    PRECONDITIONS: **|Team A| 0 v |Team B| 1/3**
    PRECONDITIONS: **|Team A| 1/2 v |Team B| 2**
    PRECONDITIONS: **|Team A| 2/3 v |Team B| 3/1**
    PRECONDITIONS: **|Team A| 1 v |Team B| 1 3/1**
    PRECONDITIONS: **|Team A| 4 2/1 v |Team B| 1**
    PRECONDITIONS: **|Team A| 1 1/3 v |Team B| 1 3/1**
    PRECONDITIONS: **|Team A| 1 1/3 v |Team B 3rd T20| 1 3/1** (following event name is added after PROD incident https://jira.egalacoral.com/browse/BMA-48652)
    PRECONDITIONS: **|Team A 3rd T20| 1 1/3 v |Team B 3rd T20| 1 3/1** (following event name is added after PROD incident https://jira.egalacoral.com/browse/BMA-48652)
    PRECONDITIONS: To check scores are updated just edit the scores in event name
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    """
    keep_browser_open = True

    def test_001_load_oxygen_applicationverify_that_scores_are_shown_and_updated_on_pages_where_scores_are_availablecheck_that_different_templates_are_shown_and_updating_appropriately(self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Verify that scores are shown and updated on pages where scores are available:
        DESCRIPTION: Check that different templates are shown and updating appropriately
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletin_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_football_pagesfor_desktopin_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_football_pages(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Football** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Football** pages
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: ![](index.php?/attachments/get/36813)
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
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
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
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: NOTE: on **'Life stream'** tab updates come through the push in the event name
        """
        pass

    def test_005_go_to_cricket_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Go to **Cricket Landing page > 'In Play'** tab
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        pass

    def test_006_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: ![](index.php?/attachments/get/36814)
        """
        pass

    def test_007_for_desktopsports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        pass
