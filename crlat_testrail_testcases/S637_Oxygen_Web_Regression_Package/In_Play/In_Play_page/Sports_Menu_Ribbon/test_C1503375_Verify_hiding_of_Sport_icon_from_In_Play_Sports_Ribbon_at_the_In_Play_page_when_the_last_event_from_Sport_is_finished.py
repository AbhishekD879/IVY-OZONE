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
class Test_C1503375_Verify_hiding_of_Sport_icon_from_In_Play_Sports_Ribbon_at_the_In_Play_page_when_the_last_event_from_Sport_is_finished(Common):
    """
    TR_ID: C1503375
    NAME: Verify hiding of <Sport> icon from In-Play Sports Ribbon at the In-Play page when the last event from Sport is finished
    DESCRIPTION: This test case verifies hiding of <Sport> icon from In-Play Sports Ribbon at the In-Play page when the last event from Sport is finished.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose **?EIO=3&transport=websocket** record
    PRECONDITIONS: 2. Make sure that within <Sport> section only one event is available
    """
    keep_browser_open = True

    def test_001_set_result_or_undisplay_event_from_preconditions_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Set result or undisplay event from preconditions in Openbet TI tool
        EXPECTED: "IN_PLAY_SPORTS_RIBBON_CHANGED" response is sent with update and <Sport> is NOT listed in its response
        """
        pass

    def test_002_verify_sport_icon_displaying_in_in_play_sports_ribbon(self):
        """
        DESCRIPTION: Verify <Sport> icon displaying in In-Play Sports Ribbon
        EXPECTED: <Sport> section is disappeared from In-Play Sports Ribbon immediately
        """
        pass

    def test_003_for_desktopnavigate_to_in_play__live_stream_section_choose_in_play_switcher_on_homepage_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section, choose 'In-Play' switcher on Homepage and repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_004_for_desktopchoose_live_stream_switcher_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Choose 'Live Stream' switcher and repeat steps 1-2
        EXPECTED: 
        """
        pass
