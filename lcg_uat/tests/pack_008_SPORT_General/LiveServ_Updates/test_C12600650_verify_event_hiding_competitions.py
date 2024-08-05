import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.football
@pytest.mark.competitions
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C12600650_Verify_Event_Hiding_Competitions(BaseSportTest):
    """
    TR_ID: C12600650
    NAME: Verify hiding of <Sports> events that have finished on Competitions page
    DESCRIPTION: This test case verifies hiding of <Sports> events that have finished on Competitions page
    PRECONDITIONS: 1. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 2. To verify 'Displayed' and 'Result_conf' attributes values check Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 3. Use http://backoffice-tst2.coral.co.uk/ti/ for triggering events undisplaying or setting results
    PRECONDITIONS: *NOTE:* *LiveServe pushes with updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True

    def verify_event_present_on_competitions_page(self, event_name, state=True):
        sections = wait_for_result(lambda: self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
                                   timeout=5,
                                   name='Events to appear')

        self.assertTrue(sections, msg='No sections are present on page')

        tab_name = vec.sb.TABS_NAME_TODAY.title() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else vec.sb.TABS_NAME_TODAY
        time_segment_name, time_segment = \
            next(((segment_name, segment) for (segment_name, segment) in sections.items() if tab_name in segment_name),
                 ('', None))
        if state:
            self.assertTrue(time_segment, msg='No "Today" date tab was not found')
            self.assertIn(event_name, time_segment.items_as_ordered_dict,
                          msg=f'Event "{event_name}" is not present on Competitions page')
        else:
            if time_segment:
                self.assertNotIn(event_name, time_segment.items_as_ordered_dict,
                                 msg=f'Event "{event_name}" is still present on Competitions page')

    def get_sports(self, sport: str):
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            return sport.title()
        return sport

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football events
        """
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
        if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                'A-ZClassIDs').split(','):
            raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                     f'is not configured on Competitions tab')

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, team1, team2 = event_params.event_id, event_params.team1, event_params.team2
        self.__class__.created_event_name = f'{team1} v {team2}'

        event_params2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID2, self.__class__.selection_id, team1_1, team2_2 = \
            event_params2.event_id, event_params2.selection_ids, event_params2.team1, event_params2.team2
        self.__class__.created_event_name2 = f'{team1_1} v {team2_2}'

    def test_001_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Navigate to 'Competitions' page
        EXPECTED: 'Competitions' page is opened
        """
        self.navigate_to_page(name='sport/football')
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competitions tab is not active, active is "{active_tab}"')

    def test_002_verify_event_is_present(self):
        """
        DESCRIPTION: Verify event is present on Competitions page
        """
        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')
        expected_league = self.get_sports(tests.settings.football_autotest_competition)
        self.assertIn(expected_league, competitions,
                      msg=f'"{expected_league}" is not present in "{competitions.keys()}" list')
        competition = competitions[expected_league]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        competition_league = tests.settings.football_autotest_competition_league
        competition_league = competition_league.title()
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(competition_league, leagues,
                      msg=f'League "{competition_league}" '
                          f'is not present in list of league in competition "{competition}"')
        league = leagues[competition_league]
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        self.verify_event_present_on_competitions_page(event_name=self.created_event_name)

    def test_003_undisplay_event_from_the_current_page(self):
        """
        DESCRIPTION: Undisplay event from the current page
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        self.verify_event_present_on_competitions_page(event_name=self.created_event_name, state=False)

    def test_004_set_results_for_another_event_from_the_current_page(self):
        """
        DESCRIPTION: Set results for another event from the current page
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        self.verify_event_present_on_competitions_page(event_name=self.created_event_name2, state=True)
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[self.eventID2][market_short_name]

        for selection in (list(self.selection_id.values())):
            self.ob_config.update_selection_result(selection_id=selection, market_id=market_id, event_id=self.eventID2)

        self.verify_event_present_on_competitions_page(event_name=self.created_event_name2, state=False)
