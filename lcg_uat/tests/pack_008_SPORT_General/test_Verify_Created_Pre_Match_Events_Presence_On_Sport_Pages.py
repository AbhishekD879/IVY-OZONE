import pytest
from selenium.common.exceptions import StaleElementReferenceException

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
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_Verify_Created_Pre_Match_Events_Presence_On_Sports_Pages(BaseSportTest):
    """
    NAME: Verify Created Pre-Match Events Presence On Sports Pages
    DESCRIPTION: OCC: VOL 551 INC0601058 : Snooker - Matches after 14:30 Not displaying
    """
    keep_browser_open = True
    football_section_name = tests.settings.football_autotest_league
    tennis_section_name = tests.settings.tennis_autotest_trophy
    basketball_section_name = tests.settings.basketball_us_league
    football_events, tennis_events, basketball_events = [], [], []

    def get_events_for_section(self, section_name):
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one event section found')
        section = sections[section_name] if section_name in sections.keys() else None
        self.assertTrue(section, msg='Section "%s" is not found in "%s"' % (section_name, ', '.join(sections.keys())))
        section.expand()
        try:
            events = section.items_as_ordered_dict
        except (StaleElementReferenceException, VoltronException):
            sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            section = sections[section_name] if section_name in sections.keys() else None
            events = section.items_as_ordered_dict if section else None
        self.assertTrue(events, msg='No events found in section "%s"' % section_name)
        return events

    def check_events_availability(self, expected, actual):
        self.assertTrue(set(expected).issubset(set(actual)),
                        msg='Missed "%s" events on page: "%s"'
                            % (len(set(expected).difference(actual)), ', '.join(set(expected).difference(actual))))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create 20 events for each of Football/Tennis/Basketball sports
        """
        for _ in range(0, 20):
            event = self.ob_config.add_autotest_premier_league_football_event(wait_for_event=False)
            event_name = f'{event.team1} v {event.team2}'
            self.__class__.football_events.append(event_name)

            event = self.ob_config.add_tennis_event_to_autotest_trophy(wait_for_event=False)
            event_name = f'{event.team1} v {event.team2}'
            self.__class__.tennis_events.append(event_name)

            event = self.ob_config.add_basketball_event_to_us_league(wait_for_event=False)
            event_name = f'{event.team1} v {event.team2}'
            self.__class__.basketball_events.append(event_name)

    def test_001_navigate_to_football_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to Football page
        DESCRIPTION: Check events presence on Football page
        EXPECTED: All previously created Football events are present
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        events = self.get_events_for_section(section_name=self.football_section_name)

        self.check_events_availability(actual=events.keys(), expected=self.football_events)

    def test_002_navigate_to_tennis_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to Tennis page
        DESCRIPTION: Check events presence on Tennis page
        EXPECTED: All previously created Tennis events are present
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        events = self.get_events_for_section(section_name=self.tennis_section_name)

        self.check_events_availability(actual=events.keys(), expected=self.tennis_events)

    def test_003_navigate_to_basketball_page_and_check_events(self):
        """
        DESCRIPTION: Navigate to Basketball page
        DESCRIPTION: Check events presence on Basketball page
        EXPECTED: All previously created Basketball events are present
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        events = self.get_events_for_section(section_name=self.basketball_section_name)

        self.check_events_availability(actual=events.keys(), expected=self.basketball_events)
