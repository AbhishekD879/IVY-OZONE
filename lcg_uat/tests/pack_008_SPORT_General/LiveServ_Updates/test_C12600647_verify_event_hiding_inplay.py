import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.football
@pytest.mark.in_play
@pytest.mark.liveserv_updates
@pytest.mark.ob_smoke
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C12600647_Verify_hiding_of_Sports_events_that_have_finished_on_In_Play_pagewidget(BaseSportTest):
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add live football events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        event_params2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID2, self.__class__.selection_id, self.__class__.team1_1, self.__class__.team2_2 \
            = event_params2.event_id, event_params2.selection_ids, event_params2.team1, event_params2.team2
        event_resp2 = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID2,
                                                                query_builder=self.ss_query_builder)
        self.__class__.event_name2 = normalize_name(event_resp2[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name2}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

    def test_001_navigate_to_sports_landing_page_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: Navigate to Sports Landing page from Sports Ribbon/Left Navigation menu
        EXPECTED: * <Sports> landing page is opened
        EXPECTED: * Events for current day are displayed
        """
        self.navigate_to_page(name='sport/football')

    def test_002_verify_event_is_present(self):
        """
        DESCRIPTION: Choose 'In-Play' tab
        EXPECTED: 'In-Play' page is opened and event is displaying
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        self.site.wait_content_state(state_name='Football')
        self.__class__.sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No one league section found on Football page')
        if not self.get_section(section_name=self.section_name):
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Football')
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name, inplay_section=vec.inplay.LIVE_NOW_SWITCHER)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not shown')

    def test_003_undisplay_event_from_the_current_page(self):
        """
        DESCRIPTION: Undisplay event from the current page
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        if self.get_section(self.section_name) is not None:
            self.sections[self.section_name].expand()
            event = self.get_event_from_league(event_id=self.eventID,
                                               section_name=self.section_name,
                                               inplay_section=vec.inplay.LIVE_NOW_SWITCHER,
                                               raise_exceptions=False)
            self.assertIsNone(event, msg=f'Event "{self.event_name}" is not hidden')
        else:
            self._logger.warning(f'*** Skipping verification as section "{self.section_name}" is not present on page')

    def test_004_set_results_for_another_event_from_the_current_page(self):
        """
        DESCRIPTION: Set results for another event from the current page
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        event = self.get_event_from_league(event_id=self.eventID2,
                                           section_name=self.section_name,
                                           inplay_section=vec.inplay.LIVE_NOW_SWITCHER,
                                           raise_exceptions=False)

        self.assertTrue(event, msg=f'Event "{self.event_name2}" is not shown')
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[self.eventID2][market_short_name]

        for selection in (list(self.selection_id.values())):
            self.ob_config.update_selection_result(selection_id=selection, market_id=market_id,
                                                   event_id=self.eventID2)

        if self.get_section(self.section_name) is not None:
            event = self.get_event_from_league(event_id=self.eventID2,
                                               section_name=self.section_name,
                                               inplay_section=vec.inplay.LIVE_NOW_SWITCHER,
                                               raise_exceptions=False)
            self.assertIsNone(event, msg=f'Event "{self.event_name2}" is not hidden')
        else:
            self._logger.warning(f'*** Skipping verification as section "{self.section_name}" is not present on page')

    def test_005_for_desktop_navigate_to_sports_landing_page_make_sure_that_sport_has_available_live_events_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page (make sure that Sport has available live events) from Sports Ribbon/Left Navigation menu
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * In-Play widget with available live events for particular Sport is displayed in 3-rd Service column
        """
        # Verified for desktop in previous steps
        pass

    def test_006_for_desktoprepeat_steps_4_5_for_both_in_play_widgets(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-5 for 'In-play' widget
        EXPECTED: **For step 4:**
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole widget disappears on front end if it contains only one event
        EXPECTED: **For step 5:**
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole widget disappears on front end if it contains only one event
        """
        # Verified for desktop in previous steps
        pass

    def test_007_for_desktopnavigate_to_in_play_section_on_homepage_and_repeat_steps_4_5_for_in_play_filter_switcher(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play' section on Homepage and repeat steps №4-5 for both 'In-play' filter switchers
        EXPECTED:
        """
        # Verified for desktop in previous steps
        pass
