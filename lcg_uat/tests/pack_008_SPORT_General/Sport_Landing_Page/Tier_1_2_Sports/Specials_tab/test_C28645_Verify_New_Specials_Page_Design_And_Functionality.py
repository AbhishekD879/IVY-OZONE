import re
import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.specials
@pytest.mark.ob_smoke
@pytest.mark.sports
@vtest
class Test_C28645_Verify_New_Specials_Page_Design_And_Functionality(BaseSportTest):
    """
    TR_ID: C28645
    VOL_ID: C9697868
    NAME: Verify New Specials Page Design & Functionality
    """
    keep_browser_open = True
    sport_name = 'Football'

    def check_selection_name_on_event_details_page(self):
        """
        DESCRIPTION: Tap on the selection name and verify event details page of that Special is opened
        """
        event_name_details_page = self.site.sport_event_details.event_title_bar.event_name
        self._logger.debug(f'*** Event name on event details page: "{event_name_details_page}"')
        result = re.match(tests.settings.football_event_name_pattern, event_name_details_page, re.U)
        self.assertTrue(result, msg=f'Item text "{event_name_details_page}" not matching pattern '
                                    f'"{tests.settings.football_event_name_pattern}"')

    def go_back_to_specials_page(self):
        """
        DESCRIPTION: Tap on back button and verify specials page is opened
        """
        self.site.back_button_click()
        self.assertEqual(self.site.football.tabs_menu.current, self.expected_sport_tabs.specials,
                         msg='Specials tab is not active')

    def get_section_by_name(self, section_name: str):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No sections found')
        section = sections.get(section_name)
        self.assertTrue(section, msg=f'Section "{section_name}" is not found in "{sections.keys()}"')
        return section

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Specials event
        """
        self.ob_config.add_autotest_premier_league_football_event(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True)

    def test_001_tap_sport(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports menu:
        EXPECTED: Football landing page is opened
        """
        self.site.open_sport(self.sport_name)

    def test_002_tap_specials(self):
        """
        DESCRIPTION: Tap on 'SPECIALS' Module header:
        EXPECTED: Specials page is opened
        EXPECTED: Specials page is displayed all available Football Specials
        EXPECTED: 'SPECIALS' events is displayed within Competition type
        EXPECTED: Each Event within a Competition type is ordered by Start date and time
        EXPECTED: The first Competition is expanded by default
        EXPECTED: The remaining Competition is collapsed by default
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.specials)
        self.assertEqual(self.site.football.tabs_menu.current, self.expected_sport_tabs.specials,
                         msg='Specials tab is not active')
        specials = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(specials, msg='*** Specials events are not displayed')

        specials_name, special = list(specials.items())[0]
        is_section_expanded = special.is_expanded()
        self.assertTrue(is_section_expanded, msg=f'The section "{specials_name}" is not expanded by default')
        if len(specials) > 1:
            for specials_name, special in list(specials.items())[1:]:
                self.assertFalse(special.is_expanded(), msg='The section "{specials_name}" is not collapsed by default')

    def test_003_verify_specials_event(self):
        """
        DESCRIPTION: Football Special Event contains only one selection - selection name is displayed with odds
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No sections found')
        section_names = sections.keys()

        for section_name in section_names:
            section = self.get_section_by_name(section_name=section_name)
            section.expand()
            events = section.items_as_ordered_dict

            self.assertTrue(events, msg=f'*** No events found in section: {section_name}')
            self.__class__.event_name, event = list(events.items())[0]
            if 'ENHANCED MULTIPLES' in section_name:
                self._logger.warning(f'*** Skipping click on event {self.event_name} since it is Special event')
            else:
                event.click()
                self.check_selection_name_on_event_details_page()
                self.go_back_to_specials_page()
