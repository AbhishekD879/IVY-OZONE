import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C1931571_Verify_appearing_hiding_of_Sport_icon_on_Sport_Ribbon_at_In_Play_Live_Stream_section_on_Homepage_for_Desktop(Common):
    """
    TR_ID: C1931571
    NAME: Verify appearing/hiding of <Sport> icon on Sport Ribbon at 'In-Play & Live Stream' section on Homepage for Desktop
    DESCRIPTION: This test case verifies appearing/hiding of <Sport> icon on Sport Ribbon at 'In-Play & Live Stream' section on Homepage for Desktop
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Scroll the page down to view 'In-play and Live Stream' section ('In-Play' switcher and the first 'Sport' tab are selected by default)
    PRECONDITIONS: )
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose **?EIO=3&transport=websocket** record
    PRECONDITIONS: * Use "IN_PLAY_SPORTS_RIBBON_CHANGED" response to check updates
    """
    keep_browser_open = True

    def test_001_undisplayresult_all_events_from_non_selected_sport(self):
        """
        DESCRIPTION: Undisplay/result all events from non-selected sport
        EXPECTED: * "IN_PLAY_SPORTS_RIBBON_CHANGED" response is sent with update and <Sport> is NOT listed in its response
        EXPECTED: * <Sport> events disappear immediately
        EXPECTED: * <Sport> icon disappears from Sports Ribbon immediately
        """
        pass

    def test_002_select_any_sport_that_is_not_1st_in_ribbon_and_undisplayresult_all_its_events(self):
        """
        DESCRIPTION: Select any sport that is NOT 1st in ribbon and undisplay/result all its events
        EXPECTED: * "IN_PLAY_SPORTS_RIBBON_CHANGED" response is sent with update and <Sport> is NOT listed in its response
        EXPECTED: * <Sport> events disappear immediately
        EXPECTED: * <Sport> icon disappears from Sports Ribbon immediately
        EXPECTED: * 1st sport in ribbon becomes selected
        """
        pass

    def test_003_select_1st_sport_in_ribbon_and_undisplayresult_all_its_events(self):
        """
        DESCRIPTION: Select 1st sport in ribbon and undisplay/result all its events
        EXPECTED: * "IN_PLAY_SPORTS_RIBBON_CHANGED" response is sent with update and <Sport> is NOT listed in its response
        EXPECTED: * <Sport> events disappear immediately
        EXPECTED: * <Sport> icon disappears from Sports Ribbon immediately
        EXPECTED: * Next sport is ribbon becomes selected
        """
        pass

    def test_004_start_new_event_within_sport_that_is_not_present_in_sports_ribbon(self):
        """
        DESCRIPTION: Start new event within <Sport> that is not present in Sports Ribbon
        EXPECTED: * "IN_PLAY_SPORTS_RIBBON_CHANGED" response is sent with update and <Sport> is listed in its response
        EXPECTED: * <Sport> icon appears on Sports Ribbon immediately
        EXPECTED: * Its position is controlled by 'CategoryDisplayOrder' in ascending OR alphabetically in case of identical dispOrder
        EXPECTED: * Previously selected sport remains selected in ribbon
        """
        pass

    def test_005_repeat_steps_1_4_when_live_stream_switcher_is_selected(self):
        """
        DESCRIPTION: Repeat steps 1-4 when 'Live Stream' switcher is selected
        EXPECTED: 
        """
        pass
