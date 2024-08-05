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
class Test_C1501894_Verify_counter_displaying_updating_for_Sport_Tabs_within_In_Play_and_Live_Stream_section_on_Home_page_for_Desktop(Common):
    """
    TR_ID: C1501894
    NAME: Verify counter displaying/updating for Sport Tabs within 'In-Play and Live Stream' section on Home page for Desktop
    DESCRIPTION: This test case verifies counter displaying/updating for Sport Tabs within 'In-Play and Live Stream' section on Home page for Desktop
    PRECONDITIONS: To check value that is displayed in Counter use the following instruction:
    PRECONDITIONS: 1. Dev Tools->Network->WS
    PRECONDITIONS: 2. Open 'INPLAY_LS_SPORTS_RIBBON' response
    PRECONDITIONS: 3. Look at **liveEventCount / liveStreamEventCount** attributes for in-play/live stream events
    PRECONDITIONS: Use the following link for checking attributes of In-Play events:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_scroll_down_the_page_to_view_in_play_and_live_stream_section(self):
        """
        DESCRIPTION: Scroll down the page to view 'In-play and Live stream' section
        EXPECTED: * 'In-play and Live stream' section is displayed below 'Enhanced multiples' carousel if EM events are available
        EXPECTED: * Section contains 2 filter switchers: 'In-play' and 'Live Stream'
        EXPECTED: * 'In-play' is opened by default
        EXPECTED: * Sport tabs are displayed with counters
        """
        pass

    def test_003_verify_counter_on_in_play_events_per_sport(self):
        """
        DESCRIPTION: Verify counter on in-play events Per Sport
        EXPECTED: * Counter is displayed for every Sports icon on In-Play section
        EXPECTED: * Number of In-Play events for certain Sport corresponds to value in Counter
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute in WS
        """
        pass

    def test_004_choose_live_stream_tab(self):
        """
        DESCRIPTION: Choose 'Live Stream' tab
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_005_verify_counter_displaying_of_live_stream_in_play_events_per_sport(self):
        """
        DESCRIPTION: Verify Counter displaying of Live Stream in-play events Per Sport
        EXPECTED: * Counter is displayed for every Sports icon where Live Stream events are
        EXPECTED: * Number of Live Stream in-play events for certain Sport corresponds to value in Counter
        EXPECTED: * Value in Counter corresponds to **liveStreamEventCount**
        """
        pass

    def test_006_verify_counter_displaying_of_live_stream_in_play_events_per_sport_if_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify counter displaying of Live Stream in-play events per Sport if there are no available events
        EXPECTED: * Counters are NOT displayed for Sports that don't contain Live Stream events
        EXPECTED: * Sports icon is still displayed on Sports Ribbon
        EXPECTED: * liveStreamEventCount attribute in WS equal to '0'
        """
        pass

    def test_007_verify_counter_with_total_number_of_live_streamin_play_events_for_in_playlive_stream_tabs(self):
        """
        DESCRIPTION: Verify counter with total number of Live Stream/In-play events for 'In-play'/'Live Stream' tabs
        EXPECTED: Counter with total number of Live Stream/In-play events is NOT displayed next to 'In-play'/'Live Stream' inscription
        """
        pass

    def test_008_trigger_completionexpiration_of_event_from_any_sport_on_in_play_sectionnote_event_completionexpiration_means_that_event_is_not_present_on_siteserver_anymore_attribute_displayedn_is_set_for_event_(self):
        """
        DESCRIPTION: Trigger completion/expiration of event from any Sport on 'In-play' section
        DESCRIPTION: NOTE: Event completion/expiration means that event is not present on SiteServer anymore (attribute 'displayed="N"' is set for event )
        EXPECTED: * Completed/expired event is removed from the front-end automatically
        EXPECTED: * Counter is updated for respective Sport
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** attribute in WS
        """
        pass

    def test_009_trigger_starting_of_event_for_any_sport(self):
        """
        DESCRIPTION: Trigger starting of event for any Sport
        EXPECTED: * Started event appears on the front-end (after refresh)
        EXPECTED: * Counter is updated for respective Sport
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** attribute in WS
        """
        pass

    def test_010_repeat_steps_8_9_for_live_stream_section(self):
        """
        DESCRIPTION: Repeat steps 8-9 for 'Live Stream' section
        EXPECTED: 
        """
        pass
