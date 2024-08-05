import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C59208808_Verify_stream_displaying_after_attempt_to_launch_another_unavailable_stream_at_In_Play_Live_Stream_section(Common):
    """
    TR_ID: C59208808
    NAME: Verify stream displaying after attempt to launch another unavailable stream at 'In-Play & Live Stream ' section
    DESCRIPTION: Test case verifies correct displaying of the stream launched after another unavailable stream at 'In-Play & Live Stream ' section of Homepage
    PRECONDITIONS: Use the following link for checking attributes of In-Play events:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: Types of available streams:
    PRECONDITIONS: EVFLAG_IVM - IMG Video Mapped for this event
    PRECONDITIONS: EVFLAG_PVM - Perform Video Mapped for this event
    PRECONDITIONS: EVFLAG_AVA - At The Races stream available
    PRECONDITIONS: EVFLAG_RVA - RacingUK stream available
    PRECONDITIONS: EVFLAG_RPM - RPGTV Greyhound streaming Mapped
    PRECONDITIONS: EVFLAG_GVM - iGameMedia streaming Mapped
    PRECONDITIONS: Necessary precondition:
    PRECONDITIONS: 1) At least one available and one mapped, but not available stream is present in 'In-Play & Live Stream ' section of Homepage
    PRECONDITIONS: 2) User is logged in
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: * Homepage is displayed
        EXPECTED: * 'In-Play & Live Stream ' section is displayed with 'In-Play' tab selected by default
        """
        pass

    def test_002_navigate_to_live_stream_tab(self):
        """
        DESCRIPTION: Navigate to **Live stream** tab
        EXPECTED: * Tab is opened
        EXPECTED: * First event stream is started automatically
        """
        pass

    def test_003_press_play_icon_for_the_event_with_mapped_but_unavailable_stream(self):
        """
        DESCRIPTION: Press Play icon for the event with mapped, but unavailable stream
        EXPECTED: * "The Stream for this event is currently not available." message is displayed
        """
        pass

    def test_004_press_play_icon_for_any_other_present_event_with_available_stream(self):
        """
        DESCRIPTION: Press Play icon for any other present event with available stream
        EXPECTED: * Stream is launched for selected event
        EXPECTED: * Error messages disappear and are not displayed within the widget
        """
        pass
