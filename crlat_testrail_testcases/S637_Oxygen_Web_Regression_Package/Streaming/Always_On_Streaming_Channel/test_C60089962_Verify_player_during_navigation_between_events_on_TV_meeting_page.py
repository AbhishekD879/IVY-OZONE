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
class Test_C60089962_Verify_player_during_navigation_between_events_on_TV_meeting_page(Common):
    """
    TR_ID: C60089962
    NAME: Verify player during navigation between events on TV meeting page
    DESCRIPTION: This case verifies video streaming player during navigation between events on Ladbrokes/Coral TV meeting page
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

    def test_001_press_play_button_on_tv_area_on_landing_page(self):
        """
        DESCRIPTION: Press Play button on TV area on Landing page
        EXPECTED: * Stream is started and content is visible on Greyhound Landing page
        EXPECTED: * Stream is muted by default
        EXPECTED: * Player controls and features are same as on regular event stream and depends on platform under test (web or native)
        """
        pass

    def test_002_press_on_watch_ladbrokescoral_tv_button(self):
        """
        DESCRIPTION: Press on 'Watch Ladbrokes/Coral TV' button
        EXPECTED: * Ladbrokes/Coral TV meeting page is opened for next available event
        EXPECTED: * Streaming video continues to play without need to start it again
        """
        pass

    def test_003_navigate_to_another_ladbrokescoral_tv_event_from_timeline_barindexphpattachmentsget122256520(self):
        """
        DESCRIPTION: Navigate to another Ladbrokes/Coral TV event from Timeline bar
        DESCRIPTION: ![](index.php?/attachments/get/122256520)
        EXPECTED: * Ladbrokes/Coral TV meeting page is opened for picked event
        EXPECTED: * Streaming video continues to play without need to start it again
        """
        pass

    def test_004_press_back_button(self):
        """
        DESCRIPTION: Press 'Back' button
        EXPECTED: * Ladbrokes/Coral TV meeting page of previous event is opened
        EXPECTED: * Streaming video continues to play without need to start it again
        """
        pass

    def test_005_press_back_button_again(self):
        """
        DESCRIPTION: Press 'Back' button again
        EXPECTED: * Greyhounds Landing page is loaded
        EXPECTED: * Streaming video continues to play in banner area of landing page without need to start it again
        """
        pass
