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
class Test_C58612445_Verify_eSoccer_Live_Scores_by_Template_in_OB(Common):
    """
    TR_ID: C58612445
    NAME: Verify eSoccer Live Scores by Template in OB
    DESCRIPTION: This test case verifies that Live Scores for eSoccer are shown and updated through OB name template
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Create events using OB for Football category in eSoccer class.
    PRECONDITIONS: Use the following event name templates:
    PRECONDITIONS: **|Team A| x-y |Team B|**
    PRECONDITIONS: **|Team A (Nickname1@!)| x-y |Team B (Nickname2@!) (Bo1)||(BG)|**
    PRECONDITIONS: **Team A (Nickname1@!) x-y Team B (Nickname2@!) (Bo1)(BG)**
    PRECONDITIONS: e.g. |Test Team 1| 0-0 |Test Team 2|
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    PRECONDITIONS: **RULES:**
    PRECONDITIONS: Added possibility to use brackets in team name to specify secondary name (SN) for Football and eSports: Liverpool (FEARGGWP), where FEARGGWP is secondary name.
    PRECONDITIONS: * There can be used as much SN as you want: Liverpool (lv-pl)(FEARGGWP) (second attempt).
    PRECONDITIONS: * SN can contain same characters as base team name: `' "&!@#$^|_;:.,?~/ and alphanumeric: Liverpool (lvpl777@com)
    PRECONDITIONS: * SN should NOT start from digit! Liverpool (123lvp)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check scores are updated just edit the scores in event name: e.g. from 0-0 to 1-0
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: - Look at the attribute 'scoreboard':
    PRECONDITIONS: - Verify score value for **'ALL'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: - Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: ![](index.php?/attachments/get/104229685)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Verify that scores are shown and updated on pages where scores are available:
    """
    keep_browser_open = True

    def test_001_for_mobiletablet_in_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_esoccer_pages_home_page_gt_featured_tab__in_play_module_highlight_carousel_featured_module_created_by_type_idevent_id_home_page_gt_in_play_tab_home_page_gt_live_stream_tab_esoccer_landing_page_gt_in_play_module(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: * **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **eSoccer** pages
        DESCRIPTION: * Home page &gt; **'Featured' tab** :
        DESCRIPTION: * In-play module
        DESCRIPTION: * Highlight carousel
        DESCRIPTION: * Featured module (created by Type_id/Event_id)
        DESCRIPTION: * Home page &gt; **'In Play'** tab
        DESCRIPTION: * Home page &gt; **'Live stream'** tab
        DESCRIPTION: * **eSoccer Landing page &gt; 'In Play'** module
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: ![](index.php?/attachments/get/104231911)
        """
        pass

    def test_002_for_desktop_in_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_esoccer_pages_home_page_gt_in_play_and_live_stream_module_check_in_play_tab_and_live_stream_tabs_sports_landing_page_gt_in_play_widget_and_live_stream_widget_esoccer_landing_page_gt_in_play_tab(self):
        """
        DESCRIPTION: **For Desktop**
        DESCRIPTION: * **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **eSoccer** pages
        DESCRIPTION: * Home page &gt; **'In play and live stream'** module
        DESCRIPTION: * Check 'In-play' tab and 'Live Stream' tabs
        DESCRIPTION: * Sports Landing page &gt; 'In-Play' widget and 'Live Stream 'widget
        DESCRIPTION: * **eSoccer Landing page &gt; 'In Play'** tab
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: ![](index.php?/attachments/get/104231911)
        """
        pass

    def test_003_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Team name and scores are shown in one line
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: ![](index.php?/attachments/get/104231912)
        """
        pass
