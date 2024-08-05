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
class Test_C58212493_Verify_Football_Match_Time_displaying_and_updating(Common):
    """
    TR_ID: C58212493
    NAME: Verify Football Match Time displaying and updating
    DESCRIPTION: This test case verifies the Football Match Time displaying and updating for BIP events
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
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: CLOCK
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='FIRST_HALF/HALF_TIME/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF''** - to look at the scorers for the specific time
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: ![](index.php?/attachments/get/6051049)
    """
    keep_browser_open = True

    def test_001_verify_match_time_displaying(self):
        """
        DESCRIPTION: Verify Match Time displaying
        EXPECTED: * Match time is shown instead of Start Time in the format:
        EXPECTED: MM:SS  (minutes and seconds)
        EXPECTED: * The timer is counting in real-time
        EXPECTED: * 'HT' label is shown in case of half time
        EXPECTED: * 'LIVE' label is shown in case event doesn't have scores and Timer for displaying
        """
        pass

    def test_002_verify_the_reflection_of_updated_match_time_on_the_page(self):
        """
        DESCRIPTION: Verify the reflection of updated 'Match Time' on the page
        EXPECTED: * New 'Match Time' replace the old one
        EXPECTED: * New 'Match Time' is received in 'CLOCK' response in WS
        """
        pass

    def test_003_verify_match_time_displaying_for_the_following_pages__homepage___featured_tabsection_mobile__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Verify Match Time displaying for the following pages:
        DESCRIPTION: - Homepage -> 'Featured' tab/section **Mobile**
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        EXPECTED: * 'LIVE'/'Timer' is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        pass

    def test_004_repeat_step_2_for_he_following_pages__homepage___featured_tabsection_mobile__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat step 2 for he following pages:
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
        EXPECTED: * 'LIVE'/'Timer' badge is displayed next to event class/type
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        """
        pass

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass
