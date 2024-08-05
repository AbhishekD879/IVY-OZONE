import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C60090033_Verify_stream_player_during_navigation_to_another_type_from_Meetings_switcher(Common):
    """
    TR_ID: C60090033
    NAME: Verify stream player during navigation to another type from Meetings switcher
    DESCRIPTION: This test case verifies stream player during navigation to another type from Meetings switcher on meetings page
    PRECONDITIONS: **TO BE FINISHED AFTER IMPLEMENTATION OF BMA-56794**
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: Static block for Always On Stream Channel is created in CMS
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5ba3a1f77d3b30391d93e665/dashboard?sid=5f748efe059ce64d59a70620
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5d24ab732fabd699077b9b8c/dashboard?sid=5f748e0c0bf7df38a687f767
    PRECONDITIONS: In CMS: System Configuration > Structure > %future streaming tv config name% -> set to enabled
    PRECONDITIONS: 1) Load app
    PRECONDITIONS: 2) User is logged in with balance >0 or placed bet during last 24 hours
    PRECONDITIONS: 3) Navigate to Greyhounds Landing page
    """
    keep_browser_open = True

    def test_001_press_on_watch_ladbrokescoral_tv_button(self):
        """
        DESCRIPTION: Press on 'Watch Ladbrokes/Coral TV' button
        EXPECTED: * Ladbrokes/Coral TV meeting page is opened for next available event
        EXPECTED: * Streaming video player is ready for user (play button is available)
        """
        pass

    def test_002_press_play_button(self):
        """
        DESCRIPTION: Press play button
        EXPECTED: * Stream is started and content is visible on Greyhound Landing page
        EXPECTED: * Stream is muted by default
        EXPECTED: * Player controls and features are same as on regular event stream and depends on platform under test (web or native)
        """
        pass

    def test_003_in_meetings_switcher_choose_event_type_with_available_always_on_streaming_feature_but_different_from_ladbrokes_tvcoral_tvindexphpattachmentsget122259040(self):
        """
        DESCRIPTION: In Meetings switcher, choose event type with available Always On Streaming feature (but different from 'Ladbrokes TV'/'Coral TV')
        DESCRIPTION: ![](index.php?/attachments/get/122259040)
        EXPECTED: * Page for closest meeting of chosen type is loaded
        EXPECTED: * SS response in devTools for Event has **GAO** flag, and its parent Type has **GVA** flag
        """
        pass

    def test_004_observe_stream_player_content_of_meeting_page(self):
        """
        DESCRIPTION: Observe stream player content of meeting page
        EXPECTED: Streaming window displayed ready for user to press play to watch stream
        """
        pass

    def test_005_press_play_button(self):
        """
        DESCRIPTION: Press Play button
        EXPECTED: * Stream is started and content is visible on Greyhound Landing page
        EXPECTED: * Stream is muted by default
        """
        pass

    def test_006_navigate_to_ladbrokes_tvcoral_tv_type_from_meetings_switcher(self):
        """
        DESCRIPTION: Navigate to 'Ladbrokes TV'/'Coral TV' type from Meetings switcher
        EXPECTED: * Ladbrokes/Coral TV meeting page is opened for next available event
        EXPECTED: * Streaming video player is ready for user (play button is available)
        """
        pass

    def test_007_press_play_button(self):
        """
        DESCRIPTION: Press play button
        EXPECTED: * Stream is started and content is visible on Greyhound Landing page
        EXPECTED: * Stream is muted by default
        """
        pass

    def test_008_in_meetings_switcher_choose_event_type_without_available_always_on_streaming_feature(self):
        """
        DESCRIPTION: In Meetings switcher, choose event type **without** available Always On Streaming feature
        EXPECTED: * Page for closest meeting of chosen type is loaded
        EXPECTED: * Regular meeting page view is displayed without streaming window opened
        EXPECTED: * 'Watch' button is available for the event
        EXPECTED: * SS response in devTools for Event has **no** **GAO** flag, and its parent Type has **no** **GVA** flag
        EXPECTED: ![](index.php?/attachments/get/122259044)
        """
        pass
