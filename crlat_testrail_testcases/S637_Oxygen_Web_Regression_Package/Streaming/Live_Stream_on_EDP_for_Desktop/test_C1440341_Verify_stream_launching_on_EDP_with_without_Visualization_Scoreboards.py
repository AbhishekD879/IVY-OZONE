import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C1440341_Verify_stream_launching_on_EDP_with_without_Visualization_Scoreboards(Common):
    """
    TR_ID: C1440341
    NAME: Verify stream launching on EDP with/without Visualization/Scoreboards
    DESCRIPTION: This test case verifies stream launching on EDP.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) SiteServer event should be configured to support the following streaming:
    PRECONDITIONS: * IMG streaming ( **typeFlagCodes** ='IVA , ... ' AND **drilldownTagNames** ='EVFLAG_IVM' flags should be set) and should be mapped to IMG stream event
    PRECONDITIONS: * Perform streaming ( **typeFlagCodes** ='PVA , ... ' AND **drilldownTagNames** ='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2) Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: *   isMarketBetInRun = "true"
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_with_credentials_where_you_have_the_positive_balance(self):
        """
        DESCRIPTION: Login with credentials where you have the positive balance
        EXPECTED: The user is logged in
        """
        pass

    def test_003_open_event_details_page_of_any_sport_for_the_event_which_has_mapped_visualizationscoreboards_without_an_available_stream(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which has mapped Visualization/Scoreboards without an available stream
        EXPECTED: *<Sport> Event Details Page is opened
        EXPECTED: * Visualization/Scoreboard is displayed
        EXPECTED: * 'Match Live' and 'Watch Live' buttons are NOT displayed
        """
        pass

    def test_004_open_event_details_page_of_any_sport_for_the_event_which_has_available_streaming_but_without_mapped_visualizationscoreboards(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which has available streaming but without mapped Visualization/Scoreboards
        EXPECTED: *<Sport> Event Details Page is opened
        EXPECTED: * Stream is launched automatically
        EXPECTED: * 'Match Live' and 'Watch Live' buttons are NOT displayed
        """
        pass

    def test_005_click_on_pause_and_play_icon_again_at_the_video_player(self):
        """
        DESCRIPTION: Click on 'Pause' and 'Play' icon again at the video player
        EXPECTED: The stream is stopped and started playing again
        """
        pass

    def test_006_adjust_volume_at_the_video_player(self):
        """
        DESCRIPTION: Adjust volume at the video player
        EXPECTED: Volume can be adjusted
        """
        pass

    def test_007_click_on_expand_and_minimize_icon_at_the_video_player(self):
        """
        DESCRIPTION: Click on 'Expand' and 'Minimize' icon at the video player
        EXPECTED: * The stream is resized to the full screen, playing correctly
        EXPECTED: * It is possible to minimize it back
        """
        pass

    def test_008_open_event_details_page_of_any_sport_for_the_event_which_has_available_streaming_and_mapped_visualizationscoreboards(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which has available streaming and mapped Visualization/Scoreboards
        EXPECTED: *<Sport> Event Details Page is opened
        EXPECTED: * 'Match Live' and 'Watch Live' buttons are displayed
        EXPECTED: * 'Match Live' button is selected by default and Visualization/Scoreboard is displayed
        """
        pass

    def test_009_hover_the_mouse_over_match_live_and_watch_live_buttons(self):
        """
        DESCRIPTION: Hover the mouse over 'Match Live' and 'Watch Live' buttons
        EXPECTED: Hover state is activated on buttons
        """
        pass

    def test_010_click_on_watch_live_button(self):
        """
        DESCRIPTION: Click on 'Watch Live' button
        EXPECTED: * 'Watch Live' button is clickable
        EXPECTED: * Stream is launched automatically
        """
        pass

    def test_011_click_on_match_live_button(self):
        """
        DESCRIPTION: Click on 'Match Live' button
        EXPECTED: * 'Match Live' button is clickable
        EXPECTED: * Visualization/Scoreboard is displayed
        """
        pass
