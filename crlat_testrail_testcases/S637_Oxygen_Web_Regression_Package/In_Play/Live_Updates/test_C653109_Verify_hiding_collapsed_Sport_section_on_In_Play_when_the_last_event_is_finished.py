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
class Test_C653109_Verify_hiding_collapsed_Sport_section_on_In_Play_when_the_last_event_is_finished(Common):
    """
    TR_ID: C653109
    NAME: Verify hiding collapsed <Sport> section on In-Play when the last event is finished
    DESCRIPTION: This test case verifies hiding collapsed <Sport> section on In-Play when the last event is finished
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab > 'Live Now' section/switcher
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose ?EIO=3&transport=websocket record
    PRECONDITIONS: * Make sure that within <Sport> section only one event is available
    """
    keep_browser_open = True

    def test_001_collapse_sport_section_which_has_one_event_within(self):
        """
        DESCRIPTION: Collapse <Sport> section which has one event within
        EXPECTED: * <Sport> section is collapsed
        EXPECTED: * Event within <Sport> section becomes unsubscribed from Live Serv updates
        EXPECTED: * <Sport> is subscribed to 'IN_PLAY_SPORT_COMPETITION_CHANGED' updates (record is sent in WS)
        """
        pass

    def test_002_set_result_or_undisplay_event_from_step_1_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Set result or undisplay event from step 1 in Openbet TI tool
        EXPECTED: * Push notification is NOT received for updated event
        EXPECTED: * 'IN_PLAY_STRUCTURE_CHANGED' record is sent with update and <Sport> is no more listed in its response
        EXPECTED: * <Sport> section is disappeared from In Play page immediately
        """
        pass

    def test_003_repeat_steps_1_2_for_upcoming_section(self):
        """
        DESCRIPTION: Repeat steps 1-2 for 'Upcoming' section
        EXPECTED: 
        """
        pass

    def test_004_for_mobiletabletnavigate_to_homepage__in_play_tab_and_repeat_steps_1_3(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage > 'In-Play' tab and repeat steps 1-3
        EXPECTED: 
        """
        pass
