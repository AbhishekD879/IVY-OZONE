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
class Test_C28663_Verify_Live_Scores_Displaying_when_Score_was_Changed_for_HOME_Player(Common):
    """
    TR_ID: C28663
    NAME: Verify Live Scores Displaying when Score was Changed for HOME Player
    DESCRIPTION: Thos test case verifies live scores displaying when score was changed for HOME player.
    DESCRIPTION: NOTE: UAT assistance is needed for LIVE Scores changing. ([or use instruction][1])
    DESCRIPTION: [1]: https://confluence.egalacoral.com/display/MOB/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: 1) In order to have a Scores Tennis event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify player name and corresponding player score
    PRECONDITIONS: *   **periodCode**='GAME', **description**="Game in Tennis match', **state**='R/S', periodIndex="X" with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**="SET", **description**="Set in Tennis match", periodIndex="X" - to look at the scorers for the specific Set (where X-set number)
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_tennis_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Tennis' icon from the Sports Menu Ribbon
        EXPECTED: 'Tennis' landing page is opened
        """
        pass

    def test_003_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: 'In Play' tab is opened
        """
        pass

    def test_004_verify_tennis_event_with_score_available(self):
        """
        DESCRIPTION: Verify Tennis event with score available
        EXPECTED: Score is shown between player names
        """
        pass

    def test_005_trigger_the_following_situationfact_is_changed_for_home_player_rolecodeplayer_1_on_the_higestperiodindex_levelandfactis_changed_for_home_player_on_periodcodegame_level_of_the_highestperiodindex(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **'fact'** is changed for HOME player (roleCode="PLAYER_1")  on the higest **periodIndex **level
        DESCRIPTION: AND
        DESCRIPTION: **'fact'** is changed for HOME player on periodCode="GAME" level of the highest **periodIndex**
        EXPECTED: Score is immediately start displaying new value for Home player on Game Score and on highest Set Score
        """
        pass

    def test_006_find_event_from_step_4_on_today_tabfor_desktopmatches_tab_for_mobile_and_repeat_step_5(self):
        """
        DESCRIPTION: Find event from step №4 on Today tab(for desktop)/'Matches' tab (for mobile) and repeat step №5
        EXPECTED: 
        """
        pass

    def test_007_tap_live_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Live' icon from the Sports Menu Ribbon
        EXPECTED: 'In-Play' tab is shown with 'All Sport' selected
        """
        pass

    def test_008_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_009_tap_tennis_icon_from_the_sports_menu_ribbon_on_in_play_page(self):
        """
        DESCRIPTION: Tap 'Tennis' icon from the Sports Menu Ribbon on 'In-Play' page
        EXPECTED: 'Tennis' page is opened
        """
        pass

    def test_010_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_011_tap_live_stream_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Live Stream' icon from the Sports Menu Ribbon
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_012_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_013_tap_in_play_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'In-Play' tab from the Module Selector Ribbon
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_014_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_015_tap_live_stream_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Live Stream' tab from the Module Selector Ribbon
        EXPECTED: 'Live Stream' tab is opened
        """
        pass

    def test_016_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_017_verify_gameset_score_change_for_home_player_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Game/Set Score change for HOME player for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Game/Set Score will be shown there
        """
        pass

    def test_018_verify_gameset_score_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Game/Set Score change before application is opened
        EXPECTED: If application was not started/opened and Score was changed for HOME player, after opening application and verified event - updated Game/Set Score will be shown there
        """
        pass

    def test_019_verify_gameset_score_change_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify Game/Set Score change when Details Page of verified event is opened
        EXPECTED: After tapping Back button updated Score will be shown on Landing page
        """
        pass
