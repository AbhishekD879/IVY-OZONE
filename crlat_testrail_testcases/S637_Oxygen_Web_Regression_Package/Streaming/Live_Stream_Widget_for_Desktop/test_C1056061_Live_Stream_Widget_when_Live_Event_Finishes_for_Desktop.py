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
class Test_C1056061_Live_Stream_Widget_when_Live_Event_Finishes_for_Desktop(Common):
    """
    TR_ID: C1056061
    NAME: 'Live Stream' Widget when Live Event Finishes for Desktop
    DESCRIPTION: This test case verifies 'Live Stream' Widget when live event finishes for Desktop
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Video streaming is mapped for particular <Sport>
    PRECONDITIONS: To get information about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * x.xx latest supported SiteServer version
    PRECONDITIONS: * xxxx event id
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: **startTime** attribute - to see start time of event
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sport_landing_page_where_live_streaming_is_mapped(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page where live streaming is mapped
        EXPECTED: * <Sport> Landing page is opened
        EXPECTED: * 'Matches' tab is opened by default
        EXPECTED: * Live Stream widget is present in the Main view column 2
        EXPECTED: * Live Stream widget is expanded
        EXPECTED: * First available event from current <Sport>, that has live streaming mapped, is displayed (see **startTime** attribute);
        EXPECTED: * Events with identical start time are sorted in the following way:
        EXPECTED: 1) competition 'displayOrder' in ascending
        EXPECTED: 2) Alphabetical order
        EXPECTED: * in WS:
        EXPECTED: "GET_SPORT" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORTS::16::STREAM_EVENT",…] response received
        EXPECTED: "GET_TYPE" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORT_TYPE::16::STREAM_EVENT::",…] response received
        EXPECTED: "subscribe" message sent only for 1 event with livestream available (by start time and display order)
        """
        pass

    def test_003_finish_current_live_stream_event_by_resulting_or_undisplaying_in_ti_or_wait_for_it_to_finish(self):
        """
        DESCRIPTION: Finish current Live Stream event (by resulting or undisplaying in TI or wait for it to finish)
        EXPECTED: * In WS:
        EXPECTED: "unsubscribe" message sent for finished event
        EXPECTED: * New event doesn't appear in widget
        """
        pass

    def test_004_refresh_the_page_and_verify_event_displaying_in_live_stream_widget(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying in Live Stream widget
        EXPECTED: * The next available event from current <Sport>, that has live streaming mapped, is displayed (see **startTime** attribute)
        EXPECTED: * Events with identical start time are sorted in the following way:
        EXPECTED: 1) competition 'displayOrder' in ascending
        EXPECTED: 2) Alphabetical order
        EXPECTED: * in WS:
        EXPECTED: "GET_SPORT" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORTS::16::STREAM_EVENT",…] response received
        EXPECTED: "GET_TYPE" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORT_TYPE::16::STREAM_EVENT::",…] response received
        EXPECTED: "subscribe" message sent only for 1 event with livestream available (by start time and display order)
        """
        pass

    def test_005_verify_live_stream_widget_when_live_event_finishes_and_there_are_no_more_live_streaming_events(self):
        """
        DESCRIPTION: Verify Live Stream widget when live event finishes and there are no more live streaming events
        EXPECTED: Live Stream widget disappear
        """
        pass
