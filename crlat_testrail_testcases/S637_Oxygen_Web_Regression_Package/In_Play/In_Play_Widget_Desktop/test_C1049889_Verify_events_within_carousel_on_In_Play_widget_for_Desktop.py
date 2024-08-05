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
class Test_C1049889_Verify_events_within_carousel_on_In_Play_widget_for_Desktop(Common):
    """
    TR_ID: C1049889
    NAME: Verify events within carousel on In-Play widget for Desktop
    DESCRIPTION: This test case verifies events within carousel on In-play widget for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: * For checking data get from In-Play MS use the following instruction:
    PRECONDITIONS: 1) Dev Tools->Network->WS
    PRECONDITIONS: 2) Open "IN_PLAY_SPORTS::XX::LIVE_EVENT::XX" response;  XX - category ID;
    PRECONDITIONS: 3) Look at 'eventCount' attribute for every type available in WS for appropriate category
    PRECONDITIONS: * Use the following link for checking attributes of In-Play events: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page_that_contains_live_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Events are displayed in carousel
        """
        pass

    def test_003_verify_events_displaying_within_carousel_on_in_play_widget(self):
        """
        DESCRIPTION: Verify Events displaying within carousel on In-Play widget
        EXPECTED: * Maximum 10 events are displayed (It can be events from different classes/types)
        EXPECTED: * Events are displayed as cards in carousel and are scrollable to the right/left side by clicking on navigation arrows
        """
        pass

    def test_004_verify_events_ordering_within_carousel(self):
        """
        DESCRIPTION: Verify events ordering within carousel
        EXPECTED: * Classes (e.g. Football England, Football Brazil) are ordered by OpenBet 'displayOrder' in ascending where minus ordinals are displayed first
        EXPECTED: * The leagues (Types) are ordered by OpenBet 'displayOrder' in ascending
        EXPECTED: * The events from the same Competition are ordered in the following way:
        EXPECTED: 1. 'startTime' - chronological order in the first instance
        EXPECTED: 2. Event 'displayOrder' in ascending
        EXPECTED: 3. Alphabetical order
        """
        pass

    def test_005_verify_events_that_are_present(self):
        """
        DESCRIPTION: Verify events that are present
        EXPECTED: Events with the following attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        """
        pass

    def test_006_repeat_steps_3_5_when_live_outright_events_are_present_in_the_widget(self):
        """
        DESCRIPTION: Repeat steps 3-5 when Live Outright events are present in the widget
        EXPECTED: 
        """
        pass
