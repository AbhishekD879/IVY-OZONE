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
class Test_C28425_Verify_live_events_filtering_on_In_Play_pages(Common):
    """
    TR_ID: C28425
    NAME: Verify live events filtering on 'In-Play' pages
    DESCRIPTION: This test case verifies live events filtering on 'In-Play' page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40725)
    """
    keep_browser_open = True

    def test_001_verify_live_events_within_the_page(self):
        """
        DESCRIPTION: Verify live events within the page
        EXPECTED: All events with attributes:
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

    def test_002_repeat_step_1_on_home_page__in_play_tab_mobiletablet_sports_landing_page__in_play_tab_sports_landing_page__in_play_widget_desktop(self):
        """
        DESCRIPTION: Repeat step 1 on:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * Sports Landing page > 'In-play' widget **Desktop**
        EXPECTED: 
        """
        pass
