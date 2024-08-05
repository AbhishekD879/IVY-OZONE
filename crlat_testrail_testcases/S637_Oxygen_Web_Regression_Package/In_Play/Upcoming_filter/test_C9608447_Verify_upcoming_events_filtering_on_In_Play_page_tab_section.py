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
class Test_C9608447_Verify_upcoming_events_filtering_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C9608447
    NAME: Verify upcoming events filtering on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies upcoming events filtering on 'In-Play' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Upcoming events are present in 'Upcoming' section (for mobile/tablet) or when 'Upcoming' switcher is selected (for Desktop)
    PRECONDITIONS: 4. For reaching Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::UPCOMING_EVENT::XXX"
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40808)
    """
    keep_browser_open = True

    def test_001_verify_upcoming_events_within_the_page(self):
        """
        DESCRIPTION: Verify upcoming events within the page
        EXPECTED: All events with next attributes are shown:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Event is NOT started
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        EXPECTED: Events with 'isStarted="true"' and 'is_off'="Y" attributes are NOT present within 'Upcoming' section
        """
        pass

    def test_002_repeat_step_1_on_home_page_gt_in_play_tab_for_mobiletablet_sports_landing_page_gt_in_play_tab(self):
        """
        DESCRIPTION: Repeat step 1 on:
        DESCRIPTION: * Home page &gt; 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page &gt; 'In-Play' tab
        EXPECTED: 
        """
        pass
