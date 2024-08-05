import pytest
from selenium.common.exceptions import StaleElementReferenceException
import voltron.environments.constants as vec

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.tennis
@pytest.mark.basketball
@pytest.mark.in_play
@pytest.mark.timeout(800)
@pytest.mark.slow
@pytest.mark.safari
@vtest
class Test_Verify_Created_Live_Events_Presence_On_Site(BaseSportTest):
    """
    VOL_ID: C9698707
    NAME: Verify Created Live Events Presence On Site
    DESCRIPTION: OCC: VOL 551 INC0601058 : Snooker - Matches after 14:30 Not displaying
    """
    keep_browser_open = True

    football_section_name = tests.settings.football_autotest_competition_league
    tennis_section_name = tests.settings.tennis_autotest_competition_trophy
    basketball_section_name = tests.settings.basketball_us_competition
    football_events, tennis_events, basketball_events = [], [], []

    def get_events_for_section(self, section_name, sport_name):
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one event section found in for sport: "%s"' % sport_name)
        section = sections[section_name] if section_name in sections.keys() else None
        self.assertTrue(section, msg='Section "%s" is not found in "%s"' % (section_name, ', '.join(sections.keys())))
        section.expand()
        try:
            events = section.items_as_ordered_dict
        except (StaleElementReferenceException, VoltronException):
            sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            section = sections[section_name] if section_name in sections.keys() else None
            events = section.items_as_ordered_dict if section else None
        self.assertTrue(events, msg='No events found in section "%s"' % section_name)
        return events

    def get_events_for_section_on_inplay_page(self, sport_name, section_name):
        self.site.inplay.inplay_sport_menu.click_item(sport_name)
        sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one event section found in for sport: "%s"' % sport_name)
        section = sections[section_name] if section_name in sections.keys() else None
        self.assertTrue(section, msg='Section "%s" is not found in "%s"' % (section_name, ', '.join(sections.keys())))
        section.expand()
        try:
            events = section.items_as_ordered_dict
        except (StaleElementReferenceException, VoltronException):
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            section = sections[section_name] if sections else None
            events = section.items_as_ordered_dict if section else None
        self.assertTrue(events, msg='No events found in section "%s"' % section_name)
        return events

    def get_events_for_section_on_home_page_inplay_tab(self, sport_name, section_name):
        modules = self.cms_config.get_initial_data().get('modularContent', [])
        modules_name = [module.get('id') for module in modules]
        self.softAssert(self.assertIn, self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play, modules_name,
                        msg=f'In-play tab isn\'t shown on Homepage')
        tab_content = self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play))

        sport_sections = tab_content.live_now.items_as_ordered_dict
        sport_section = sport_sections.get(sport_name)

        self.assertTrue(sport_section, msg=f'Sport "{sport_name}" is not found in {list(sport_sections.keys())}')
        sport_section.expand()
        league_sections = sport_section.items_as_ordered_dict
        self.assertTrue(league_sections, msg=f'No Leagues for "{sport_name}" found')
        league = league_sections.get(section_name)
        if not league and sport_section.has_show_more_leagues_button():
            sport_section.show_more_leagues_button.click()
            league_sections = sport_section.items_as_ordered_dict
            self.assertTrue(league_sections, msg=f'No Leagues for "{sport_name}" found')
            league = league_sections.get(section_name)

        self.assertTrue(league, msg=f'League "{section_name}" not found in {list(league_sections.keys())}')
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for "{section_name}"')
        return events

    def check_events_availability(self, expected, actual):
        self.assertTrue(set(expected).issubset(set(actual)),
                        msg='Missed %s events on page: "%s"'
                            % (len(set(expected).difference(actual)), ', '.join(set(expected).difference(actual))))

    def test_000_create_20_live_events_for_each_sport(self):
        """
        DESCRIPTION: Create 20 Live events for each of Football/Tennis/Basketball sports
        """
        for i in range(0, 20):
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, wait_for_event=False)
            event_name = '%s v %s' % (event.team1, event.team2)
            self.__class__.football_events.append(event_name)

        for i in range(0, 20):
            event = self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True, wait_for_event=False)
            event_name = '%s v %s' % (event.team1, event.team2)
            self.__class__.tennis_events.append(event_name)

        for i in range(0, 20):
            event = self.ob_config.add_basketball_event_to_us_league(is_live=True, wait_for_event=False)
            event_name = '%s v %s' % (event.team1, event.team2)
            self.__class__.basketball_events.append(event_name)

    def test_001_navigate_to_football_inplay_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to Football In-Play page
        DESCRIPTION: Check events presence on Football In-Play page
        EXPECTED: All previously created Football Live events are present
        """
        self.navigate_to_page(name='sport/football/live')
        self.site.wait_content_state('FOOTBALL')
        events = self.get_events_for_section(section_name=self.football_section_name, sport_name='FOOTBALL')
        self.check_events_availability(actual=events.keys(), expected=self.football_events)

    def test_002_navigate_to_tennis_inplay_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to Tennis In-Play page
        DESCRIPTION: Check events presence on Tennis In-Play page
        EXPECTED: All previously created Tennis Live events are present
        """
        self.navigate_to_page(name='sport/tennis/live')
        self.site.wait_content_state('TENNIS')
        events = self.get_events_for_section(section_name=self.tennis_section_name, sport_name='TENNIS')
        self.check_events_availability(actual=events.keys(), expected=self.tennis_events)

    def test_003_navigate_to_basketball_inplay_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to Basketball In-Play page
        DESCRIPTION: Check events presence on Basketball In-Play page
        EXPECTED: All previously created Basketball Live events are present
        """
        self.navigate_to_page(name='sport/basketball/live')
        self.site.wait_content_state('BASKETBALL')
        events = self.get_events_for_section(section_name=self.basketball_section_name, sport_name='BASKETBALL')
        self.check_events_availability(actual=events.keys(), expected=self.basketball_events)

    def test_004_navigate_to_inplay_football_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to In-Play -> Football page
        DESCRIPTION: Check events presence on In-Play -> Football page
        EXPECTED: All previously created Football Live events are present
        """
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state('IN-PLAY')

        events = self.get_events_for_section_on_inplay_page(section_name=self.football_section_name,
                                                            sport_name=vec.inplay.IN_PLAY_FOOTBALL)
        self.check_events_availability(actual=events.keys(), expected=self.football_events)

    def test_005_navigate_to_inplay_basketball_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to In-Play -> Basketball page
        DESCRIPTION: Check events presence on In-Play -> Basketball page
        EXPECTED: All previously created Basketball Live events are present
        """
        events = self.get_events_for_section_on_inplay_page(section_name=self.basketball_section_name,
                                                            sport_name=vec.inplay.IN_PLAY_BASKETBALL)
        self.check_events_availability(actual=events.keys(), expected=self.basketball_events)

    def test_006_navigate_to_inplay_tennis_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to In-Play -> Tennis page
        DESCRIPTION: Check events presence on In-Play -> Tennis page
        EXPECTED: All previously created Tennis Live events are present
        """
        events = self.get_events_for_section_on_inplay_page(section_name=self.tennis_section_name, sport_name=vec.inplay.IN_PLAY_TENNIS)
        self.check_events_availability(actual=events.keys(), expected=self.tennis_events)

    def test_007_navigate_to_homepage_inplay_tab_and_check_events(self):
        """
        DESCRIPTION: Navigate to Homepage -> In-Play tab
        DESCRIPTION: Check events presence on Homepage -> In-Play tab
        EXPECTED: All previously created Live events are present
        """
        self.navigate_to_page(name='home/in-play')
        self.site.wait_content_state('Homepage')
        section_name = self.football_section_name.title() if self.brand == 'bma' else self.football_section_name
        events = self.get_events_for_section_on_home_page_inplay_tab(section_name=section_name,
                                                                     sport_name='FOOTBALL')
        self.check_events_availability(actual=events.keys(), expected=self.football_events)

        section_name = self.tennis_section_name.title() if self.brand == 'bma' else self.tennis_section_name
        events = self.get_events_for_section_on_home_page_inplay_tab(section_name=section_name,
                                                                     sport_name='TENNIS')
        self.check_events_availability(actual=events.keys(), expected=self.tennis_events)

        events = self.get_events_for_section_on_home_page_inplay_tab(section_name=self.basketball_section_name,
                                                                     sport_name='BASKETBALL')
        self.check_events_availability(actual=events.keys(), expected=self.basketball_events)
