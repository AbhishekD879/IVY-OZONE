import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C874381_Verify_Football_Scores_displaying_and_updating(Common):
    """
    TR_ID: C874381
    NAME: Verify Football Scores displaying and updating
    DESCRIPTION: This test case verifies the Football Scores displaying and updating for BIP events
    DESCRIPTION: AUTOTEST [C50107450] - mobile - (just on tst2 endpoints)
    DESCRIPTION: AUTOTEST [C50107451] - desktop
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: * In order to have Football Scores, the event should be BIP. In OB system/TI make the following settings:
    PRECONDITIONS: * Set 'Bet in Play List': True in 'Flag' section on event level
    PRECONDITIONS: * Set the valid 'Start Time' for event
    PRECONDITIONS: * Set 'Is Off':'Yes' on the event level
    PRECONDITIONS: * Set 'Bet In Running':'Yes' on market level
    PRECONDITIONS: Links to OB system:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+OpenBet+System
    PRECONDITIONS: * [How to generate Live Scores for Football using Amelco][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: * [How to generate Live Scores for Football using TI][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: * [How to configure Fallback Scoreboard in CMS][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To verify Football data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: *   **categoryCode** = "FOOTBALL"
    PRECONDITIONS: *   **score** : X,
    PRECONDITIONS: where X - score from main match time for particular team;
    PRECONDITIONS: *   **extraTimeScore** : X,
    PRECONDITIONS: where X - score from extra time period for particular team;
    PRECONDITIONS: *   **penaltyScore** : X,
    PRECONDITIONS: where X - score due to penalty for particular team;
    PRECONDITIONS: *   **role_code**='HOME'/'AWAY' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **period_code**='FIRST_HALF/HALF_TIME/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF''** - to look at the scorers for the specific time
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: ![](index.php?/attachments/get/6051048)
    PRECONDITIONS: 2) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='FIRST_HALF/HALF_TIME/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF''** - to look at the scorers for the specific time
    PRECONDITIONS: *   **role_code**='HOME'/'AWAY' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **value** - to see a score for particular team
    PRECONDITIONS: ![](index.php?/attachments/get/6051050)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to 'In-Play' page
    PRECONDITIONS: 3. Select the 'Football' tab
    """
    keep_browser_open = True

    def test_001_verify_scores_displaying_for_the_event_which_has_scores_available(self):
        """
        DESCRIPTION: Verify scores displaying for the event which has Scores available
        EXPECTED: * Match score is shown
        EXPECTED: * Each score for a particular team is shown near team name
        """
        pass

    def test_002__trigger_updating_of_scores_verify_reflection_of_updated_scores_on_the_page(self):
        """
        DESCRIPTION: * Trigger updating of Scores.
        DESCRIPTION: * Verify reflection of updated Scores on the page.
        EXPECTED: * New Score replace the old one
        EXPECTED: * New Score is received in 'SCBRD' response in WS
        """
        pass

    def test_003_verify_event_which_doesnt_have_scores_available(self):
        """
        DESCRIPTION: Verify event which doesn't have Scores available
        EXPECTED: * Only 'LIVE' label is shown below the team name
        EXPECTED: * Scores are NOT displayed
        """
        pass

    def test_004_repeat_steps_1_3_for__homepage___featured_tabsection_mobile__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section **Mobile**
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        EXPECTED: 
        """
        pass

    def test_005_desktopnavigate_to_football_landing_page__matches_tab_and_verify_scorestimer_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Football landing page > 'Matches' tab and verify scores/timer for 'In-play' widget
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        pass

    def test_006_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps: 2-3
        EXPECTED: 
        """
        pass

    def test_007_desktopnavigate_to_football_landing_page__matches_tab_and_verify_scorestimer_for_live_stream_widget_if_available(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Football landing page > 'Matches' tab and verify scores/timer for 'Live Stream' widget (if available)
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        """
        pass

    def test_008_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps: 2-3
        EXPECTED: 
        """
        pass
