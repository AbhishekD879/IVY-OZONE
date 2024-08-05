import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870189_Verify_football_journey(BaseSportTest):
    """
    TR_ID: C44870189
    NAME: Verify football journey
    DESCRIPTION: "Site is loaded,
    DESCRIPTION: User navigates to Sport page via Homepage -> Carousel Link or Via Homepage -> All Sports (Menu) -> Football"
    DESCRIPTION: Also user can navigate form A-Z menu.
    """
    keep_browser_open = True
    sport_name = vec.FOOTBALL_SPORT_NAME
    widget_section_name = 'In-PlayLIVE\nFootball'

    def accordion_expand_collapse(self):
        accordions = list(self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values())
        if accordions is not None:
            for accordion in accordions[:3]:
                if not accordion.is_expanded():
                    self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values()
                    accordion.expand()
                    self.device.driver.implicitly_wait(5)
                    self.assertTrue(wait_for_result(lambda: accordion.is_expanded(), timeout=5),
                                    msg=f'"{accordion.name}" Accordion is not expanded')
                else:
                    self.site.contents.scroll_to()
                    self.device.driver.implicitly_wait(3)
                    accordion.collapse()
                    self.assertFalse(wait_for_result(lambda: accordion.is_expanded(), timeout=5),
                                     msg=f'"{accordion.name}" Accordion is not collapsed')
        else:
            self._logger.info('*** No events are available')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Site is loaded,
        PRECONDITIONS: Verify football journey - navigation from different pages and display > User should be able to navigate successfully
        """
        self.site.open_sport(self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)
        self.navigate_to_page("Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.click_item(vec.ALL_SPORTS_MENU_ITEM)
            self.site.all_sports.a_z_sports_section.items_as_ordered_dict[vec.FOOTBALL_TAB.capitalize()].click()
        else:
            self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict[vec.FOOTBALL_TAB.capitalize()].click()
        self.site.wait_content_state(state_name=vec.FOOTBALL_TAB.capitalize())
        self.navigate_to_page("Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.click_item(vec.IN_PLAY_MODULE_NAME.upper())
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            in_play_tab = menu_items[vec.IN_PLAY_MODULE_NAME.upper()]
            in_play_tab.click()
        self.site.wait_content_state(state_name=vec.IN_PLAY_TAB)
        sports_categorie = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.values())
        self.assertTrue(sports_categorie, msg='"sports Categories" are not displayed')
        football_sport = sports_categorie[1]
        self.assertTrue(football_sport.is_selected(), msg=f'"{football_sport.name}" tab is not opened by default')

    def test_001_tapclick_on_football_button_from_the_main_menuorselect_football_from_a_z_menu(self):
        """
        DESCRIPTION: Tap/Click on Football button from the Main Menu
        DESCRIPTION: or
        DESCRIPTION: Select Football from A-Z menu.
        EXPECTED: Football page is loaded.
        EXPECTED: The 'Matches' tab is selected by default
        EXPECTED: The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: All events which are available are displayed for the League
        EXPECTED: Enhanced Multiple events (if available) are displayed on the top of the list and is expanded (**For Mobile/Tablet**) Enhanced Multiple events (if available) are displayed as carousel above tabs (**For Desktop**)
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel (**For Desktop**)
        """
        self.navigate_to_page("Homepage")
        self.site.open_sport(self.sport_name)
        self.__class__.sport_fb = self.site.football
        self.site.wait_content_state(state_name=self.sport_name)
        current_tab = self.sport_fb.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Default tab: "{current_tab}" opened'
                             f'Expected tab: "{self.expected_sport_tabs.matches}" opened')
        # Enhanced Multiple events needs to be configured in OB, hence cannot customise and test it on prod.
        events = list(self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values())
        if events:
            events = list(self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values())
            self.assertTrue(events, msg='No leagues are display on Football page')
            for event in range(len(events)):
                if event <= 3:
                    self.assertTrue(events[event].is_expanded(), msg='event is not expanded by default')
                if 4 <= event <= 6:
                    self.assertFalse(events[event].is_expanded(), msg="event is not collapsed by default")
                break
            if self.device_type == 'desktop':
                self.device.driver.implicitly_wait(5)
                widget = self.sport_fb.in_play_widget._list_item_type.live_label
                self.assertTrue(widget, msg=f'{vec.IN_PLAY_TAB} widget is found on Football page')
        else:
            self._logger.info('*** No events are available')

    def test_002_verify_collapseexpandable_accordion(self):
        """
        DESCRIPTION: Verify Collapse/Expandable accordion
        EXPECTED: Collapsible and expandable accordions should be accessible
        """
        # covered in step 06

    def test_003_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: The 'In-Play' tab is loaded with the 'Live Now'/'Upcoming' sections
        EXPECTED: The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content (**For Desktop**)
        """
        if self.device_type == 'mobile':
            self.sport_fb.tabs_menu.click_button(vec.IN_PLAY_TAB)
            current_tab = self.sport_fb.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.in_play,
                             msg=f'Current tab: "{current_tab}" opened is not `as '
                                 f'expected: "{self.expected_sport_tabs.in_play}"')
            expected_sections = [vec.LIVE_NOW_EVENTS_SECTION, vec.UPCOMING_EVENTS_SECTION]
            sections = self.site.inplay.tab_content.items_as_ordered_dict.keys()
        else:
            self.site.contents.tabs_menu.click_button(vec.IN_PLAY_TAB)
            current_tab = self.site.contents.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.in_play,
                             msg=f'Current tab: "{current_tab}" opened is not `as '
                                 f'expected: "{self.expected_sport_tabs.in_play}"')
            expected_sections = [vec.LIVE_NOW_EVENTS_SECTION, vec.UPCOMING_SWITCHER]
            sections = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
            self.device.refresh_page()
            try:
                widget = self.sport_fb.in_play_widget._list_item_type.live_label
                self.assertFalse(widget, msg=f'{vec.IN_PLAY_TAB} widget is found on Football page')
            except VoltronException as e:
                self._logger.info(e)

        self.assertTrue(sections, msg=f'No tabs are present in "{vec.IN_PLAY_TAB}" tab')
        self.assertEqual(list(sections), expected_sections, msg=f'In-Play tab is not loaded with sections.'
                                                                f'Actual: "{list(sections)}",'
                                                                f'Expected: "{expected_sections}"')

    def test_004_tapclick_on_the_competition_tab_accumulators_outrights__specials(self):
        """
        DESCRIPTION: Tap/Click on the Competition tab/ Accumulators/ Outrights / Specials
        EXPECTED: Event types are displayed.
        """
        self.__class__.sport_fb = self.site.football
        outright_tab = self.sport_fb.tabs_menu.click_button(vec.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
        self.assertTrue(outright_tab, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
        if self.device_type == 'mobile':
            sections = self.sport_fb.tab_content.accordions_list.items_as_ordered_dict
        else:
            current_tab = self.sport_fb.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.outrights,
                             msg=f'Tab: "{current_tab}"opened is not as expected: "{self.expected_sport_tabs.outrights}"')
            sections = self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.keys()
        self.assertTrue(sections, msg='No sections found in Outright tab')

        accumulators_tab = self.sport_fb.tabs_menu.click_button(vec.SPORT_TABS_INTERNAL_NAMES.accumulators.upper())
        self.assertTrue(accumulators_tab, msg=f'"{vec.SPORT_TABS_INTERNAL_NAMES.accumulators.upper()}" is not opened')
        groups = list(self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(groups, msg='No event types are displayed in "ACCUMULATORS"')

        competitions_tab = self.sport_fb.tabs_menu.click_button(vec.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        self.assertTrue(competitions_tab, msg=f'"{self.expected_sport_tabs.competitions}" is not opened')
        if self.device_type == 'mobile':
            sections = self.sport_fb.tab_content.accordions_list.items_as_ordered_dict
        else:
            current_tab = self.sport_fb.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.competitions,
                             msg=f'Tab: "{current_tab}"opened is not as expected: "{self.expected_sport_tabs.competitions}"')
            sections = self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.keys()
        self.assertTrue(sections, msg='No sections found in Competition tab')

        specials_tab = self.sport_fb.tabs_menu.click_button(vec.SPORT_TABS_INTERNAL_NAMES.specials.upper())
        self.assertTrue(specials_tab, msg=f'"{self.expected_sport_tabs.specials}" is not opened')
        if self.device_type == 'mobile':
            sections = self.sport_fb.tab_content.accordions_list.items_as_ordered_dict
        else:
            current_tab = self.sport_fb.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.specials,
                             msg=f'Tab: "{current_tab}"opened is not as expected: "{self.expected_sport_tabs.specials}"')
            sections = self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.keys()
        self.assertTrue(sections, msg='No sections found in specials tab')

    def test_005_verify_display_of_landing_page_and_all_tabs_and_sub_tabs_are_accessible_journey_is_smooth_user_can_navigate_forward_and_backwards_pages_load_and_all_features_including_banners_links_are_displayed(self):
        """
        DESCRIPTION: Verify display of landing page and all tabs and sub tabs are accessible, journey is smooth, user can navigate forward and backwards, pages load and all features including Banners, links, are displayed
        EXPECTED: Subtabs, landing page and  all other tabs should be accessible
        """
        #  all tabs and sub tabs are accessible is covered in step 07
        self.device.go_back()
        self.site.wait_content_state_changed()
        banners = self.site.home.aem_banner_section
        self.assertTrue(banners.is_displayed(), msg="Banner section is not displayed")

    def test_006_verify_that_user_is_able_to_switch_between_the_tabs_and_subtabs_and_each_tab_displays_data_grouped_by_type_as_links_or_expandable_areas_as_per_requirements_and_functionality_works_fine_for_each_one_in_play_events_outright_coupons_etc(self):
        """
        DESCRIPTION: Verify that user is able to switch between the tabs and subtabs, and each tab displays data grouped by Type, as links or expandable areas, as per requirements and functionality works fine for each one: In Play, Competitions etc
        EXPECTED: User journey between the tabs and subtabs should be smooth enough
        """
        self.sport_fb.tabs_menu.items_as_ordered_dict.get(vec.IN_PLAY_TAB).click()
        if self.device_type == 'desktop':
            inplay_subtabs = list(self.sport_fb.tab_content.grouping_buttons.items_as_ordered_dict.values())
            for item in range(len(inplay_subtabs)):
                inplay_subtabs = list(self.sport_fb.tab_content.grouping_buttons.items_as_ordered_dict.values())
                inplay_subtabs[item].click()
                self.accordion_expand_collapse()
        else:
            self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values()
            self.site.contents.scroll_to()
            self.accordion_expand_collapse()
        self.sport_fb.tabs_menu.click_button(vec.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        if self.device_type == 'desktop':
            competitions_subtabs = list(self.sport_fb.date_tab.items_as_ordered_dict.values())
            for group in competitions_subtabs:
                self.sport_fb.date_tab.items_as_ordered_dict.values()
                group.click()
                self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values()

                self.accordion_expand_collapse()
        else:
            self.sport_fb.tab_content.accordions_list.items_as_ordered_dict.values()
            self.accordion_expand_collapse()

    def test_007_verify_that_on_edp_user_is_able_to_switch_between_the_markets_and_the_page_is_updated_with_the_correct_specific_market_display_and_respective_data(self):
        """
        DESCRIPTION: Verify that on EDP user is able to switch between the markets, and the page is updated with the correct specific Market display and respective data
        EXPECTED: Successful pages should be loaded
        """
        competitions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        for comp_name, comp in competitions.items():
            if not comp.is_expanded():
                comp.expand()
            event_type = list(comp.items_as_ordered_dict.values())
            event_type[0].click()
            event = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
            event[0].click()
            markets_tabs_list = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
            self.assertTrue(markets_tabs_list, msg='No markets found')
            for tab_name, tab in list(markets_tabs_list.items()):
                tab.click()
                self.assertTrue(tab_name, msg='market display page is not loaded')
            break
        else:
            self._logger.info('*** No events are available')
