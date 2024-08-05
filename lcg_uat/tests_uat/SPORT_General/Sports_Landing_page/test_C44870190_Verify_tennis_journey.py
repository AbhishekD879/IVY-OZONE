import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.pages.shared.contents.competitions_league_page import CompetitionsOutrightsTabContent


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.tennis
@pytest.mark.p1
@vtest
class Test_C44870190_Verify_tennis_journey(BaseSportTest):
    """
    TR_ID: C44870190
    NAME: Verify tennis journey
    """
    keep_browser_open = True
    sport_name = vec.bma.TENNIS
    widget_section_name = 'In-Play LIVE Tennis'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load application
        PRECONDITIONS: Site is loaded
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_001_tapclick_on_tennis_button_from_the_main_menu(self):
        """
        DESCRIPTION: Tap/Click on Tennis button from the Main Menu
        EXPECTED: Tennis Page is loaded
        EXPECTED: The 'Matches' tab is selected by default
        EXPECTED: The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: All events which are available are displayed for the League
        EXPECTED: Enhanced Multiple events (if available) are displayed on the top of the list and is expanded (**For Mobile/Tablet**) Enhanced Multiple events (if available) are displayed as carousel above tabs (**For Desktop**)
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel (**For Desktop**)
        """
        self.site.open_sport(self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)

        self.device.driver.implicitly_wait(0.5)
        current_tab = self.site.tennis.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Default tab: "{current_tab}" opened'
                             f'Expected tab: "{self.expected_sport_tabs.matches}" opened')

        # Enhanced Multiple events needs to be configured in OB, hence cannot customise and test it on prod.

        events = self.site.tennis.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events, msg='No leagues are display on Tennis page')

        if vec.racing.ENHANCED_MULTIPLES_NAME in list(events.keys()):
            expected_expanded_section = len(events.items()) if len(events.items()) < 4 else 4
        else:
            expected_expanded_section = len(events.items()) if len(events.items()) < 3 else 3
        for section_name, section in list(events.items())[:expected_expanded_section]:
            self.assertTrue(section.is_expanded(), msg=f'"{section_name}" is not expanded')
        for section_name, section in list(events.items())[expected_expanded_section:]:
            self.assertFalse(section.is_expanded(expected_result=False),
                             msg=f'"{section_name}" is not collapsed')

        if self.device_type == 'desktop':
            widget = self.site.tennis.in_play_widget.items_as_ordered_dict
            self.assertTrue(widget, msg=f'{vec.siteserve.IN_PLAY_TAB} widget is not found on Tennis page')
            self.assertIn(self.widget_section_name, widget.keys(),
                          msg=f'{self.widget_section_name} not found in {widget.keys()}')

    def test_002_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: The 'In-Play' tab is loaded with the 'Live Now'/'Upcoming' sections
        EXPECTED: The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content (**For Desktop**)
        """
        if self.device_type == 'mobile':
            self.site.tennis.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
            expected_sections = [vec.inplay.LIVE_NOW_EVENTS_SECTION, vec.inplay.UPCOMING_EVENTS_SECTION]
            sections = self.site.inplay.tab_content.items_as_ordered_dict.keys()
        else:
            self.site.contents.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
            current_tab = self.site.contents.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.in_play,
                             msg=f'Current tab: "{current_tab}" opened is not `as '
                                 f'expected: "{self.expected_sport_tabs.in_play}"')
            expected_sections = [vec.inplay.LIVE_NOW_SWITCHER, vec.inplay.UPCOMING_SWITCHER]
            sections = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict

            widget = self.site.tennis.in_play_widget.items_as_ordered_dict
            self.assertFalse(widget, msg=f'"{vec.siteserve.IN_PLAY_TAB}" widget is found on Tennis page')

        self.assertTrue(sections, msg=f'No tabs are present in "{vec.siteserve.IN_PLAY_TAB}" tab')
        self.assertEqual(list(sections), expected_sections, msg=f'In-Play tab is not loaded with sections.'
                                                                f'Actual: "{list(sections)}",'
                                                                f'Expected: "{expected_sections}"')

    def test_003_expand_one_event_type(self):
        """
        DESCRIPTION: Tap/Click on the Competition tab
        EXPECTED: Event types are displayed.
        EXPECTED: Click any event type, Matches/ Outright tabs are displayed
        """
        self.site.tennis.tabs_menu.click_button(vec.sb.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        if self.device_type == 'mobile':
            competitions = self.site.tennis.tab_content.competitions_categories.items_as_ordered_dict
        else:
            competitions = self.site.tennis.tab_content.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on Tennis page')
        event = list(competitions.values())[0]
        event.click()

        if self.device_type == 'mobile':
            tab_content = self.site.competition_league.tab_content
            current_tab_content = self.site.competition_league.current_tab_content
            if not tab_content.has_no_events_label():
                if current_tab_content[0] is CompetitionsOutrightsTabContent:
                    tab_content.click()
                else:
                    sections = tab_content.accordions_list.items_as_ordered_dict
                    self.assertTrue(sections, msg='No events sections are present on page')
        market_tab = None
        if self.device_type == 'mobile':
            market_tab = self.site.tennis.tab_content.accordions_list.items
        else:
            expected_tabs = [vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                             vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()]
            market_tab = self.site.tennis.tab_content.grouping_buttons.items_as_ordered_dict
            for tab_name in list(market_tab):
                self.assertIn(tab_name.upper(), expected_tabs, msg=f'Competition tab is not loaded with sections.'
                                                                   f'Actual: "{list(market_tab)}",'
                                                                   f'Expected: "{expected_tabs}"')
        self.assertTrue(market_tab, msg='Matches/ Outright tab is not present for event type in Competition')

    def test_004_tapclick_on_back_button_and_then_tapclick_on_outright_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Back' button and then tap/click on 'Outright' tab
        EXPECTED: The 'Outrights' tab is loaded
        EXPECTED: Leagues and Competitions are all collapsed by default
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content (**For Desktop**)
        """
        self.site.back_button.click()
        self.site.wait_content_state_changed()
        if self.device_type == 'mobile':
            self.site.back_button.click()
            self.site.wait_content_state_changed()
        outright_tab = self.site.tennis.tabs_menu.click_button(vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
        self.assertTrue(outright_tab, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
        if self.device_type == 'mobile':
            sections = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
            self.assertTrue(sections, msg='No sections found in Outright tab')
            accordions_list_length = len(sections)
            for i in range(accordions_list_length):
                self.assertFalse(sections[i].is_expanded(), msg=f'Event "{sections[i]}" is  not collapsed')
        else:
            current_tab = self.site.tennis.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.outrights,
                             msg=f'Tab: "{current_tab}"opened is not as expected: "{self.expected_sport_tabs.outrights}"')
            sections = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
            widget = self.site.tennis.in_play_widget.items_as_ordered_dict
            self.assertFalse(widget, msg=f'"{vec.siteserve.IN_PLAY_TAB}" widget is found on Tennis page')
            accordions_list_length = len(sections)
            for i in range(accordions_list_length):
                self.assertFalse(sections[i].is_expanded(), msg=f'Event "{sections[i]}" is not collapsed')
