import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.football
@pytest.mark.evergage
@pytest.mark.racing
@pytest.mark.other
@pytest.mark.low
@pytest.mark.next_races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.portal_dependant
@vtest
class Test_C119840_Verify_eventID_attribute_in_DOM_on_Sports_and_Racing(BaseSportTest, BaseRacing):
    """
    TR_ID: C119840
    NAME: Verify 'eventid' attribute in the DOM/HTML on Sports and Racing pages
    DESCRIPTION: This Test Case verified 'eventid' attribute in the DOM/HTML on Sports and Racing pages
    """
    keep_browser_open = True
    max_number_of_events = 5
    max_number_of_sections = 3
    expected_next_races_name = None

    def go_thru_sports_events(self):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in list(sections.items())[:self.max_number_of_sections]:
            section.expand()
            try:
                events = section.items_as_ordered_dict
            except StaleElementReferenceException:
                sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                events = sections[section_name].items_as_ordered_dict
            self.assertTrue(events, msg='No events found')
            for event_name, event in list(events.items())[:self.max_number_of_events]:
                self._logger.info('*** Event id of event %s is %s' % (event_name, event.event_id))
                self.assertTrue(event.event_id, msg='Eventid attribute is empty in DOM')

    def test_001_check_eventid_for_football_landing_page(self):
        """
        DESCRIPTION: Open Football and check eventid for each event on Football landing page
        EXPECTED: Event ids attributes are present for all events on page
        """
        self.site.open_sport(name='FOOTBALL', timeout=10)
        self.go_thru_sports_events()

    def test_002_check_eventid_on_outrights_tab(self):
        """
        DESCRIPTION: Open OUTRIGHTS tab and check eventid for each event on Outrights page
        EXPECTED: Event ids attributes are present for all events on page
        """
        if self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                               category_id=self.ob_config.football_config.category_id):
            expected_sport_tab = \
                self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.ob_config.football_config.category_id)
            self.site.football.tabs_menu.click_button(expected_sport_tab)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, expected_sport_tab,
                             msg=f'OUTRIGHTS tab is not active, active is "{active_tab}"')
            self.go_thru_sports_events()
        else:
            self._logger.warning(f'*** "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights}" tab is not supposed to be present. '
                                 f'Probably it is disabled in CMS. Skipping verification of presence.')

    def test_003_check_eventid_on_jackpot_tab(self):
        """
        DESCRIPTION: Open JACKPOT tab and check eventid for each event on Jackpot page
        EXPECTED: Event ids attributes are present for all events on page
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   category_id=self.ob_config.backend.ti.football.category_id,
                                   brand=self.brand)
        ss_pool = ss_req.ss_pool(query_builder=self.jackpot_query, raise_exceptions=False)
        if ss_pool:
            expected_sport_tab = \
                self.get_sport_tab_name(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.jackpot, self.ob_config.football_config.category_id)
            self.site.football.tabs_menu.click_button(expected_sport_tab)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, expected_sport_tab,
                             msg=f'JACKPOT tab is not active, active is "{active_tab}"')
            self.go_thru_sports_events()

    def test_004_check_eventid_on_inplay_tab(self):
        """
        DESCRIPTION: Open IN-PLAY tab and check eventid for each event on In-Play page
        EXPECTED: Event ids attributes are present for all events on page
        """
        expected_sport_tab = \
            self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, category_id=self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'IN-PLAY tab is not active, active is "{active_tab}"')
        self.go_thru_sports_events()

    def test_005_check_eventid_on_racing_landing_page(self):
        """
        DESCRIPTION: Open Racing page and check eventid for each event on Racing Landing page
        EXPECTED: Event ids attributes are present for all events on page
        """
        self.section_skip_list.extend([self.enhanced_races_name,
                                       vec.racing.ENHANCED_MULTIPLES_NAME,
                                       vec.racing.YOURCALL_SPECIALS.upper(),
                                       vec.virtuals.VIRTUAL_SPORTS])
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('horse-racing')
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on Horseracing page')
        for section_name, section in sections.items():
            section.expand()
            if section_name in self.section_skip_list or self.next_races_title in section_name:
                continue
            else:
                meetings = section.items_as_ordered_dict
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='No one event was found in row: "%s"' % meeting_name)
                    for event_name, event in events.items():
                        self._logger.info('*** Event id of event %s is %s' % (event_name, event.event_id))
                        self.assertTrue(event.event_id, msg='"event_id" attribute is empty in DOM')

    def test_006_check_eventid_for_next4_section(self):
        """
        DESCRIPTION: Check eventid for each event on NEXT 4 section
        EXPECTED: Event ids attributes are present for all events on section
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle')
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if next_races_toggle.get('nextRacesComponentEnabled'):
            next_races = self.get_next_races_section()
            next4_cards = next_races.items_as_ordered_dict
            for event_name, event in next4_cards.items():
                self._logger.info('*** Event id of event %s is %s' % (event_name, event.event_id))
                self.assertTrue(event.event_id, msg='Eventid attribute is empty in DOM')
        else:
            self._logger.warning('*** Next Races component disabled in CMS')
