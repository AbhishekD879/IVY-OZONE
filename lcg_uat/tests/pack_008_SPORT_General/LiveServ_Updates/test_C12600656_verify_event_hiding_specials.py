import pytest
from crlat_cms_client.utils.exceptions import CMSException

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # cannot perform liveserv updates on prod endpoints
# @pytest.mark.prod
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55699')
@vtest
class Test_C12600656_Verify_hiding_of_Sports_events_that_have_finished_on_Specials_page(BaseSportTest):
    """
    TR_ID: C12600656
    NAME: Verify hiding of <Sports> events that have finished on Specials page
    DESCRIPTION: This test case verifies hiding of <Sports> events that have finished on Specials page
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
    expected_tab_name = None

    def wait_sport_tab_name(self, tab: str, timeout: int = 15):
        wait_for_result(lambda: self.get_sport_tab_name(tab, self.ob_config.football_config.category_id),
                        timeout=timeout,
                        name='Sport tab to appear',
                        bypass_exceptions=CMSException)
        self.__class__.expected_tab_name = self.get_sport_tab_name(tab, self.ob_config.football_config.category_id)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football specials events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(special=True)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.created_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.created_event_name}"')

        event_params2 = self.ob_config.add_autotest_premier_league_football_event(special=True)
        self.__class__.eventID2 = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.created_event_name2 = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.created_event_name}"')
        self.__class__.selection_id = event_params2.selection_ids

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_navigate_to_specials_page(self):
        """
        DESCRIPTION: Navigate to Specials page
        EXPECTED: Specials page is opened
        """
        self.wait_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials)
        self.navigate_to_page(name='sport/football')
        self.site.football.tabs_menu.click_button(self.expected_tab_name)
        self.assertEqual(self.site.football.tabs_menu.current, self.expected_tab_name,
                         msg='Specials tab is not active')
        specials = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(specials, msg='*** Specials events are not displayed')

        section = self.get_section(section_name=self.section_name)
        section.expand()
        self.assertTrue(section.is_expanded(timeout=10), msg=f'Section "{self.section_name}" is not expanded')

        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in section "{self.section_name}"')
        self.assertIn(self.created_event_name, events.keys(), msg=f'Added event "{self.created_event_name}" '
                                                                  f'was not found on page "{events.keys()}"')

    def test_002_undisplay_event_from_the_current_page(self):
        """
        DESCRIPTION: Undisplay event from the current page
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        if self.get_section(self.section_name) is not None:
            result = wait_for_result(lambda: self.get_event_from_league(event_id=self.eventID,
                                                                        section_name=self.section_name,
                                                                        raise_exceptions=False) is None,
                                     timeout=10,
                                     name='Event to hide')
            self.assertTrue(result, msg=f'Event "{self.created_event_name}" is not hidden')

    def test_003_set_results_for_another_event_from_the_current_page(self):
        """
        DESCRIPTION: Set results for another event from the current page
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[self.eventID2][market_short_name]
        for selection in (list(self.selection_id.values())):
            self.ob_config.update_selection_result(selection_id=selection, market_id=market_id,
                                                   event_id=self.eventID2)
        self.get_section(self.section_name, expected_result=False)
