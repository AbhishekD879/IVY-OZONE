import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C12600647_Verify_hiding_of_Sports_events_that_have_finished_on_In_Play_page_widget(Common):
    """
    TR_ID: C12600647
    NAME: Verify hiding of <Sports> events that have finished on In-Play page/widget
    DESCRIPTION: This test case verifies hiding of <Sports> events that have finished on In-Play page/widget
    PRECONDITIONS: 1. LiveServer is available for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 3. To verify 'Displayed' and 'Result_conf' attributes values check Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 4. Use http://backoffice-tst2.coral.co.uk/ti/ for triggering events undisplaying or setting results
    PRECONDITIONS: *NOTE:* *LiveServe pushes with updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: Navigate to Sports Landing page from Sports Ribbon/Left Navigation menu
        EXPECTED: * <Sports> landing page is opened
        EXPECTED: * Events for current day are displayed
        """
        pass

    def test_002_choose_in_play_tab(self):
        """
        DESCRIPTION: Choose 'In-Play' tab
        EXPECTED: 'In-Play' page is opened and event is displaying
        """
        pass

    def test_003_undisplay_event_from_the_current_page(self):
        """
        DESCRIPTION: Undisplay event from the current page
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        pass

    def test_004_set_results_for_another_event_from_the_current_page(self):
        """
        DESCRIPTION: Set results for another event from the current page
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        pass

    def test_005_for_desktopnavigate_to_sports_landing_page_make_sure_that_sport_has_available_live_events_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page (make sure that Sport has available live events) from Sports Ribbon/Left Navigation menu
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * In-Play widget with available live events for particular Sport is displayed in 3-rd Service column
        """
        pass

    def test_006_for_desktoprepeat_steps_4_5_for_both_in_play_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-5 for both 'In-play' widget
        EXPECTED: **For step 4:**
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole widget disappears on front end if it contains only one event
        EXPECTED: **For step 5:**
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole widget disappears on front end if it contains only one event
        """
        pass

    def test_007_for_desktopnavigate_to_in_play_section_on_homepage_and_repeat_steps_4_5_for__in_play_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play ' section on Homepage and repeat steps №4-5 for  'In-play' filter switchers
        EXPECTED: 
        """
        pass
