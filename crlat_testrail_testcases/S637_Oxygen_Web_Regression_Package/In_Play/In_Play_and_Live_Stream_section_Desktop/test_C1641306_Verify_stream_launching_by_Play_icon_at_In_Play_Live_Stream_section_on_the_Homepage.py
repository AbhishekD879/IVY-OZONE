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
class Test_C1641306_Verify_stream_launching_by_Play_icon_at_In_Play_Live_Stream_section_on_the_Homepage(Common):
    """
    TR_ID: C1641306
    NAME: Verify stream launching by 'Play' icon at 'In-Play & Live Stream ' section on the Homepage
    DESCRIPTION: This test case verifies stream launching by 'Play' icon at 'In-Play & Live Stream ' section on the Homepage
    PRECONDITIONS: 1) Use the following link for checking attributes of In-Play events:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Types of available streams:
    PRECONDITIONS: EVFLAG_IVM - IMG Video Mapped for this event
    PRECONDITIONS: EVFLAG_PVM - Perform Video Mapped for this event
    PRECONDITIONS: EVFLAG_AVA - At The Races stream available
    PRECONDITIONS: EVFLAG_RVA - RacingUK stream available
    PRECONDITIONS: EVFLAG_RPM - RPGTV Greyhound streaming Mapped
    PRECONDITIONS: EVFLAG_GVM - iGameMedia streaming Mapped
    """
    keep_browser_open = True

    def test_001_open_oxygen_application(self):
        """
        DESCRIPTION: Open Oxygen application
        EXPECTED: * User is logged out
        EXPECTED: * Homepage is opened
        """
        pass

    def test_002_navigate_to_in_play__live_stream_section_on_homepage_by_scrolling_the_page_down(self):
        """
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage by scrolling the page down
        EXPECTED: * 'In-play & Live stream' section is displayed below 'Enhanced multiples' carousel if EM events are available
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        EXPECTED: * 'In-Play' switcher is selected by default
        EXPECTED: * The first 'Sport' tab is selected by default
        """
        pass

    def test_003_choose_live_stream_switcher_and_verify_events_on_a_list(self):
        """
        DESCRIPTION: Choose 'Live Stream' switcher and verify events on a list
        EXPECTED: * 'Live Stream' page is opened
        EXPECTED: * All events on a list have:
        EXPECTED: - 'Play' icon and 'Watch' text displayed on the left side of event card
        EXPECTED: - 'Watch Live' text displayed on event card next to 'Live' icon/'Match Timer'/'Sets'
        EXPECTED: - Message at the top section above accordions: 'In order to watch this stream, you must be logged in and have a positive balance...'
        """
        pass

    def test_004_log_in_and_verify_1st_event_on_live_stream_switcher(self):
        """
        DESCRIPTION: Log in and verify 1st event on 'Live Stream' switcher
        EXPECTED: * Video launches automatically at the top section above accordions
        EXPECTED: * First event on a list has:
        EXPECTED: - 'Active' icon and text displayed on the left side of event card
        EXPECTED: - 'Watching now' text displayed on event card next to 'Live' icon/'Match Timer'/'Sets'
        """
        pass

    def test_005_verify_other_events_on_live_stream_page(self):
        """
        DESCRIPTION: Verify other events on 'Live Stream' page
        EXPECTED: Other events have:
        EXPECTED: * 'Play' icon and 'Watch' text on the left side of event card
        EXPECTED: * 'Watch Live' text displayed on event card next to 'Live' icon/'Match Timer'/'Sets'
        """
        pass

    def test_006_hover_the_mouse_over_play_icon(self):
        """
        DESCRIPTION: Hover the mouse over 'Play' icon
        EXPECTED: Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_007_click_on_play_icon(self):
        """
        DESCRIPTION: Click on 'Play' icon
        EXPECTED: * 'Play' icon is clikable
        EXPECTED: * 'Play' icon is replaced by 'Active' icon
        EXPECTED: * 'Watch Live' text is replaced by 'Watching now' on event card next to 'Live' icon/'Match Timer'/'Sets'
        EXPECTED: * Video is launched at the top section
        EXPECTED: * Previously selected event card contains 'Play' icon and 'Watch Live' text again
        """
        pass

    def test_008_hover_the_mouse_over_active_icon(self):
        """
        DESCRIPTION: Hover the mouse over 'Active' icon
        EXPECTED: * Pointer does NOT change view from 'Normal select' to 'Link select'
        EXPECTED: * 'Active' icon is NOT clickable
        """
        pass
