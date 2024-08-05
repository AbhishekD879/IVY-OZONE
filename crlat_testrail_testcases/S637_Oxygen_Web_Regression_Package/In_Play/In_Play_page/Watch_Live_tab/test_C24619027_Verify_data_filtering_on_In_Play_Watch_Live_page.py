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
class Test_C24619027_Verify_data_filtering_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C24619027
    NAME: Verify data filtering on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies live and upcoming events with mapped stream filtering on 'In-Play Watch Live' page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Live and Upcoming events with the mapped stream are present in 'Live Now' and 'Upcoming' sections (for mobile/tablet) or when 'Live Now'/'Upcoming' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * Be aware that 'drilldownTagNames' to determine WHICH stream provider has been mapped to the event
    PRECONDITIONS: **'drilldownTagNames'**** ***Streaming flags are:*
    PRECONDITIONS: * EVFLAG_IVM -  IMG Video Mapped for this event
    PRECONDITIONS: * EVFLAG_PVM - Perform Video Mapped for this event
    PRECONDITIONS: * EVFLAG_GVM' - iGameMedia Video Mapped for this event
    PRECONDITIONS: * To verify attributes received for recognazing if events have mapped stream use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::STREAM_EVENT::XXX" for live now events and "IN_PLAY_SPORT_TYPE::XX::UPCOMING_STREAM_EVENT::XXX" for upcoming events
    PRECONDITIONS: where
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40724)
    """
    keep_browser_open = True

    def test_001_verify_events_within_live_now_section_when_live_now_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within 'Live now' section/ when 'Live Now' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: {"EVFLAG_BL" AND "EVFLAG_IVM"} OR {"EVFLAG_BL" AND "EVFLAG_PVM"} OR {"EVFLAG_BL" AND "EVFLAG_GVM"}
        EXPECTED: * Type's attribute contains 'typeFlagCodes' contains "IVA" OR "PVA" OR "GVA"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        """
        pass

    def test_002_verify_events_within_upcoming_events_section_when_upcoming_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within 'Upcoming Events' section/ when 'Upcoming' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Event is NOT started
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: {"EVFLAG_BL" AND "EVFLAG_IVM"} OR {"EVFLAG_BL" AND "EVFLAG_PVM"} OR {"EVFLAG_BL" AND "EVFLAG_GVM"}
        EXPECTED: * Type's attribute contains 'typeFlagCodes' contains "IVA" OR "PVA" OR "GVA"
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        EXPECTED: are shown
        EXPECTED: Events with 'isStarted="true"' attribute are NOT present within 'Upcoming' section
        """
        pass
