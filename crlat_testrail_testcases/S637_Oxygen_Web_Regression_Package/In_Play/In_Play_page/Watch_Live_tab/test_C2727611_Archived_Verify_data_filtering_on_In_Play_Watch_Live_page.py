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
class Test_C2727611_Archived_Verify_data_filtering_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727611
    NAME: [Archived] Verify data filtering on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies data filtering on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load Oxygen application
    PRECONDITIONS: 3. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_events_within_the_page_when_live_now_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within the page, when 'Live Now' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        EXPECTED: are shown, when 'Live Now' sorting type is selected
        """
        pass

    def test_002_verify_events_within_the_page_when_upcoming_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within the page, when 'Upcoming' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Event is NOT started
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * Attribute 'isNext24HourEvent="true"' is present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        EXPECTED: are shown, when 'Upcoming' sorting type is selected
        EXPECTED: Events with 'isStarted="true"' attribute are NOT present within 'Upcoming' section
        """
        pass
