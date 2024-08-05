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
class Test_C1501893_Verify_layout_content_of_In_Play_and_Live_Stream_section_on_Home_page_for_Desktop(Common):
    """
    TR_ID: C1501893
    NAME: Verify layout/content of 'In-Play and Live Stream' section on Home page for Desktop
    DESCRIPTION: This test case verifies layout/content of 'In-Play and Live Stream' section on Home page for Desktop
    PRECONDITIONS: 1) Use the following link for checking attributes of In-Play events:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    PRECONDITIONS: 2) Types of available streams:
    PRECONDITIONS: EVFLAG_IVM - IMG Video Mapped for this event
    PRECONDITIONS: EVFLAG_PVM - Perform Video Mapped for this event
    PRECONDITIONS: EVFLAG_AVA - At The Races stream available
    PRECONDITIONS: EVFLAG_RVA - RacingUK stream available
    PRECONDITIONS: EVFLAG_RPM - RPGTV Greyhound streaming Mapped
    PRECONDITIONS: EVFLAG_GVM - iGameMedia streaming Mapped
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_scroll_the_page_down_to_view_in_play_and_live_stream_section(self):
        """
        DESCRIPTION: Scroll the page down to view 'In-play and Live Stream' section
        EXPECTED: * 'In-play and Live Stream' section is displayed below 'Enhances Multiples' carousel
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        EXPECTED: * 'In-Play' switcher is selected by default
        EXPECTED: * First 'Sport' tab is selected by default
        """
        pass

    def test_003_verify_header(self):
        """
        DESCRIPTION: Verify header
        EXPECTED: Header consist of:
        EXPECTED: * 'In-Play and Live Stream' section name
        EXPECTED: * In-play Sports Ribbon
        """
        pass

    def test_004_verify_in_play_view(self):
        """
        DESCRIPTION: Verify 'In-play' view
        EXPECTED: * Max 4 events are shown
        EXPECTED: * Events are grouped by 'typeId'
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * 'Cash out' icon is displayed if available
        """
        pass

    def test_005_verify_events_that_are_shown_when_in_play_is_selected(self):
        """
        DESCRIPTION: Verify events that are shown when 'In-play' is selected
        EXPECTED: All events with attributes:
        EXPECTED: *   Event's/market's/outcome's attribute 'siteCannels' contains 'M'
        EXPECTED: *   Attribute 'isStarted="true"' is present
        EXPECTED: *   Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: *   Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: *   Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: *   At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: *   At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: *   At least one market is displayed (available in the response)
        """
        pass

    def test_006_verify_in_play_view_footer(self):
        """
        DESCRIPTION: Verify 'In-play' view footer
        EXPECTED: Footer link redirects to In-play page with 'All sports' or specific &lt;sport&gt; tab selected, depending on number of events
        """
        pass

    def test_007_verify_live_stream_view(self):
        """
        DESCRIPTION: Verify 'Live Stream' view
        EXPECTED: * Max 4 events are shown
        EXPECTED: * Events are grouped by 'typeId'
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * 'Cash out' icon is displayed if available
        """
        pass

    def test_008_verify_events_that_are_shown_when_live_stream_is_selected(self):
        """
        DESCRIPTION: Verify events that are shown when 'Live Stream' is selected
        EXPECTED: * Event's/market's/outcome's attribute 'siteCannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * drilldownTagNames **should include the following attributes: {EVFLAG_BL and EVFLAG_IVM} OR {EVFLAG_BL, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAGIVM, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAG_GVM}(on the Event level) **
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * event startTime **is today**
        """
        pass

    def test_009_verify_live_stream_view_footer(self):
        """
        DESCRIPTION: Verify 'Live Stream' view footer
        EXPECTED: Footer link is always shown and redirects to 'Live Stream' page
        """
        pass

    def test_010_click_on_any_selection_from_the_widget(self):
        """
        DESCRIPTION: Click on any selection from the widget
        EXPECTED: * Selection is successfully added to Betslip
        EXPECTED: * Selection is marked as added in 'In-Play & Live Stream' section
        """
        pass

    def test_011_place_a_bet_for_added_selection(self):
        """
        DESCRIPTION: Place a bet for added selection
        EXPECTED: Bet is placed successfully
        EXPECTED: Selection is unmarked in 'In-Play & Live Stream' section
        """
        pass

    def test_012_click_on_event_card_section(self):
        """
        DESCRIPTION: Click on Event card section
        EXPECTED: User is redirected to Event Details page
        """
        pass

    def test_013_repeat_steps_10_12_when_live_stream_view_is_selected(self):
        """
        DESCRIPTION: Repeat steps 10-12 when 'Live Stream' view is selected
        EXPECTED: 
        """
        pass
