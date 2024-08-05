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
class Test_C24623576_Verify_data_filtering_on_In_Play_and_Live_Stream_section_on_Desktop(Common):
    """
    TR_ID: C24623576
    NAME: Verify data filtering on 'In-Play and Live Stream' section on Desktop
    DESCRIPTION: This test case verifies in-play and live streaming events filtering on 'In-Play and Live Stream' section on Desktop
    PRECONDITIONS: 1. Load Oxygen app on Desktop
    PRECONDITIONS: 2. On Homepage scroll down to 'In-Play and Live Stream' section
    PRECONDITIONS: 3. Make sure that in-play and live streaming events are configured
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX" for 'In-play' switcher and "IN_PLAY_SPORT_TYPE::XX::STREAM_EVENT::XXX" for 'Live stream' switcher
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40725)      ![](index.php?/attachments/get/40724)
    """
    keep_browser_open = True

    def test_001_verify_events_when_in_play_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events when 'In-play' switcher is selected
        EXPECTED: Events with the following attributes are present:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: "EVFLAG_BL"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        """
        pass

    def test_002_verify_events_when_live_stream_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events when 'Live Stream' switcher is selected
        EXPECTED: Events with the following attributes are present:
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
