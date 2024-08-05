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
class Test_C59112600_Verify_events_sorting_in_Live_Stream_Widget(Common):
    """
    TR_ID: C59112600
    NAME: Verify events sorting in "Live Stream" Widget
    DESCRIPTION: This test case verifies Events sorting scenarios in "Live Stream" Widget on desktop
    PRECONDITIONS: 1. Live Stream widget is enabled in CMS > System Configurations > DesktopWidgetsToggle > liveStream = 'enabled'
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. Only 4 Events with following names and mapped Streams are created within same Sport:
    PRECONDITIONS: - Events from the same Type:
    PRECONDITIONS: 1) |AEvent| |vs| |AEvent2|
    PRECONDITIONS: 2) |BEvent| |vs| |BEvent2|
    PRECONDITIONS: 3) |CEvent| |vs| |CEvent2|
    PRECONDITIONS: - Events from different Type that has typeDisplayOrder smaller than one for which 3 previous events are created:
    PRECONDITIONS: 4) |DEvent| |vs| |DEvent2|
    PRECONDITIONS: NOTE: all events should have same startTime attribute except |DEvent| |vs| |DEvent2|. It should have startime which is later than 3 other Events.
    PRECONDITIONS: 4. Navigate to Sport landing page for which Events were created and scroll page to "Live Stream" Widget
    PRECONDITIONS: General sorting approach:
    PRECONDITIONS: - Events are sorted firstly by typeDisplayOrder(in case if there are Events from different Types)
    PRECONDITIONS: - Events are sorted by startTime attribute within same Type
    PRECONDITIONS: - In case of same startTime for multiple Events, they are sorted by displayOrder of the events.
    PRECONDITIONS: - If startTime and displayOrder are the same for multiple events, they are sorted Alphabetically.
    """
    keep_browser_open = True

    def test_001_verify_event_inside_live_stream_widget_and_subscription_to_event_in_inplay_ws(self):
        """
        DESCRIPTION: Verify Event inside "Live Stream" Widget and subscription to Event in Inplay WS.
        EXPECTED: - |DEvent| |vs| |DEvent2| Event is displayed in "Live Stream" Widget
        EXPECTED: - Subscription to EventId only for the Event from "Live Stream" Widget is present in Inplay WS
        """
        pass

    def test_002_undisplay_devent_vs_devent2_event_in_backoffice(self):
        """
        DESCRIPTION: Undisplay |DEvent| |vs| |DEvent2| event in backoffice
        EXPECTED: 
        """
        pass

    def test_003_go_back_to_live_stream_widget_verify_event_inside_widget_and_subscription_to_event_in_inplay_ws(self):
        """
        DESCRIPTION: Go back to "Live Stream" Widget. Verify Event inside Widget and subscription to Event in Inplay WS.
        EXPECTED: - |AEvent| |vs| |AEvent2| Event is displayed in "Live Stream" Widget
        EXPECTED: - Subscription to EventId only for the Event from "Live Stream" Widget is present in Inplay WS
        """
        pass

    def test_004_undisplay_aevent_vs_aevent2_event_in_backoffice(self):
        """
        DESCRIPTION: Undisplay |AEvent| |vs| |AEvent2| event in backoffice
        EXPECTED: 
        """
        pass

    def test_005_go_back_to_live_stream_widget_and_verify_event_inside__widget(self):
        """
        DESCRIPTION: Go back to "Live Stream" Widget, and verify Event inside  Widget
        EXPECTED: - |AEvent| |vs| |AEvent2| is removed from "Live Stream" Widget by live update
        EXPECTED: - unsubscribe for |AEvent| |vs| |AEvent2| Event is present in Inplay WS
        EXPECTED: - |BEvent| |vs| |BEvent2| Event is displayed in "Live Stream" Widget
        EXPECTED: - Subscription to EventId |BEvent| |vs| |BEvent2| Event is present in Inplay WS
        """
        pass

    def test_006_display_back_aevent_vs_aevent2_event_in_backoffice(self):
        """
        DESCRIPTION: Display back |AEvent| |vs| |AEvent2| event in backoffice
        EXPECTED: 
        """
        pass

    def test_007_go_back_to_live_stream_widget_refresh_the_page_and_verify_event_inside__widget(self):
        """
        DESCRIPTION: Go back to "Live Stream" Widget, refresh the page and verify Event inside  Widget
        EXPECTED: - |AEvent| |vs| |AEvent2| Event is displayed in "Live Stream" Widget
        EXPECTED: - Subscription to EventId only for the Event from "Live Stream" Widget is present in Inplay WS
        """
        pass

    def test_008_change_displayorder_of_cevent_vs_cevent2_event_displayorder_should_be_smaller_than_displayorder_for_two_other_events(self):
        """
        DESCRIPTION: Change displayOrder of |CEvent| |vs| |CEvent2| event (displayOrder should be smaller than displayOrder for two other events)
        EXPECTED: 
        """
        pass

    def test_009_go_back_to_live_stream_widget_refresh_the_page_and_verify_event_inside__widget(self):
        """
        DESCRIPTION: Go back to "Live Stream" Widget, refresh the page and verify Event inside  Widget
        EXPECTED: - |CEvent| |vs| |CEvent2| Event is displayed in "Live Stream" Widget
        EXPECTED: - Subscription to EventId only for the Event from "Live Stream" Widget is present in Inplay WS
        """
        pass

    def test_010_change_the_starttime_for_bevent_vs_bevent2_event_to_start_prior_to_aevent_vs_aevent2_cevent_vs_cevent2_in_backoffice(self):
        """
        DESCRIPTION: Change the startTime for |BEvent| |vs| |BEvent2| event to start prior to |AEvent| |vs| |AEvent2|, |CEvent| |vs| |CEvent2| in backoffice
        EXPECTED: 
        """
        pass

    def test_011_go_back_to_live_stream_widget_refresh_the_page_and_verify_event_inside__widget(self):
        """
        DESCRIPTION: Go back to "Live Stream" Widget, refresh the page and verify Event inside  Widget
        EXPECTED: - |BEvent| |vs| |B Event2| Event is displayed in "Live Stream" Widget
        EXPECTED: - Subscription to EventId only for the Event from "Live Stream" Widget is present in Inplay WS
        """
        pass
