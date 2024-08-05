import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.sanity
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C1143946_Navigation_Tennis(BaseSportTest):
    """
    TR_ID: C1143946
    NAME: Navigation Tennis
    DESCRIPTION: This test case verifies navigation across Tennis Landing and Details page
    DESCRIPTION: if 'Coupons' Tab is not available see instruction how to generate [Coupon](https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system)
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True
    sport_name = vec.bma.TENNIS
    widget_section_name = 'In-Play LIVE Tennis'
    autotest_coupon = vec.siteserve.TENNIS_COUPON_NAME

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get football enhanced multiples events
        """
        if tests.settings.backend_env != 'prod':
            # enhanced multiple event
            self.ob_config.add_tennis_event_enhanced_multiples()
            # live event
            self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True)
            # outright event
            self.ob_config.add_tennis_outright_event_to_autotest_league()
            # matches/competition event
            event_matches_params = self.ob_config.add_tennis_event_to_autotest_trophy()
            # coupons
            market_id = self.ob_config.market_ids[event_matches_params.event_id]['match_betting']
            self.ob_config.add_event_to_coupon(market_id=market_id, coupon_name=None,
                                               coupon_id=self.ob_config.tennis_config.coupons[self.autotest_coupon])

    def test_001_tapclick_on_tennis_button_from_the_main_menu(self):
        """
        DESCRIPTION: Tap/Click on Tennis button from the Main Menu
        EXPECTED: 1. Tennis Page is loaded
        EXPECTED: 2. The 'Matches' tab is selected by default
        EXPECTED: 3. The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: 4. All events which are available are displayed for the League
        EXPECTED: 5. **For Mobile/Tablet:**
        EXPECTED: Enhanced Multiple events section(if available) is displayed on the top of the list and is expanded
        EXPECTED: **For Desktop:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed as carousel above tabs
        EXPECTED: 6. **For Desktop:**
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel
        """
        self.site.open_sport(self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)

        self.device.driver.implicitly_wait(0.5)
        current_tab = self.site.tennis.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Default tab: "{current_tab}" opened'
                             f'Expected tab: "{self.expected_sport_tabs.matches}" opened')

        leagues_status = self.site.tennis.tab_content.accordions_list.has_items
        self.assertTrue(leagues_status, msg='No leagues are display on Tennis page')

        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                em_carousel = self.site.tennis.sport_enhanced_multiples_carousel
                self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
            else:
                events = self.site.tennis.tab_content.accordions_list.get_items(vec.racing.ENHANCED_MULTIPLES_NAME)
                self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, events,
                              msg='No "ENHANCED MULTIPLES" section found in list')

        # In-Play widget is disabled in cms for Ladbrokes Prod Desktop
        # TODO Tobe tested once In-Play widget is enabled in CMS for Ladbrokes Prod Desktop
        if self.device_type == 'desktop' and self.brand == 'bma':
            widget = self.site.tennis.in_play_widget.items_as_ordered_dict
            self.assertTrue(widget, msg=f'{vec.siteserve.IN_PLAY_TAB} widget is not found on Tennis page')
            self.assertIn(self.widget_section_name, widget.keys(),
                          msg=f'{self.widget_section_name} not found in {widget.keys()}')

    def test_002_tapclick_on_coupons_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Coupons' tab
        EXPECTED: 1. The 'Coupons' tab is loaded
        EXPECTED: 2. Sections with events are displayed on the page and are all collapsed by default
        EXPECTED: 3. It is possible to collapse/expand all of the sections by clicking the header
        EXPECTED: 4. The first 5 events load within 1 second after clicking on the section and incrementally render more events when user scrolls down
        EXPECTED: 5. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        # coupons tab is not applicable for tennis

    def test_003_select_one_event_from_the_section(self):
        """
        DESCRIPTION: Select one event from the section
        EXPECTED: The event details page is opened
        """
        # coupons tab is not applicable for tennis

    def test_004_tapclick_on_back_button_and_then_tapclick_on_outrights_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Back' button and then tap/click on 'Outrights' tab
        EXPECTED: 1. The 'Outrights' tab is loaded
        EXPECTED: 2. Leagues and Competitions are all collapsed by default
        EXPECTED: 3. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        if tests.settings.backend_env == 'prod':
            if vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper() in self.site.tennis.tabs_menu.items_names:
                self.__class__.outright_tab = True
                self.site.tennis.tabs_menu.click_button(vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
            else:
                self._logger.info("Outrights events are not present")
                self.__class__.outright_tab = False
        else:
            self.__class__.outright_tab = self.site.tennis.tabs_menu.click_button(
                vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
            self.assertTrue(self.outright_tab, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
        if self.outright_tab:
            current_tab = self.site.tennis.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.outrights,
                             msg=f'Tab: "{current_tab}" opened is not as expected: "{self.expected_sport_tabs.outrights}"')

            result = wait_for_result(
                lambda: self.site.contents.tab_content.accordions_list.is_displayed(timeout=10) is True, timeout=20)

            self.assertTrue(result, msg='Outright section is not loaded completely')

            count_of_items = self.site.contents.tab_content.accordions_list.count_of_items
            self.assertTrue(count_of_items, msg='No sections found in Outright tab')

            sections = self.site.contents.tab_content.accordions_list.get_items(number=2)
            section_name, section = next(iter(sections.items()))
            section.expand()
            wait_for_result(lambda: section.is_expanded() == True,
                            name=f'waiting for section "{section_name}" is to be expand')
            self.assertTrue(section.is_expanded(), msg=f'Section "{section_name}" is not expanded')

            if self.device_type == 'desktop':
                widget = self.site.tennis.in_play_widget.items_as_ordered_dict
                self.assertFalse(widget, msg=f'"{vec.siteserve.IN_PLAY_TAB}" widget is found on Tennis page')

    def test_005_expand_one_event_type(self):
        """
        DESCRIPTION: Expand one event type
        EXPECTED: The list of outrights from that event type is displayed
        """
        # covered in step4

    def test_006_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: 1. The 'In-Play' tab is loaded with the 'Live Now'/'Upcoming' sections
        EXPECTED: 2. The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 3. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        if self.device_type == 'mobile':
            self.site.tennis.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
            expected_sections = [vec.inplay.LIVE_NOW_EVENTS_SECTION, vec.inplay.UPCOMING_EVENTS_SECTION]
            wait_for_result(lambda: self.site.inplay.tab_content.items_as_ordered_dict, timeout=15,
                            name='Current tab is not displayed')
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
