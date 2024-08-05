import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.sanity
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C1143945_Navigation_Basketball(BaseCouponsTest, BaseSportTest):
    """
    TR_ID: C1143945
    NAME: Navigation Basketball
    DESCRIPTION: This test case verifies navigation across Basketball Landing and Details page
    DESCRIPTION: if 'Coupons' Tab is not available see instruction how to generate [Coupon](https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system)
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True
    sport_name = vec.sb.BASKETBALL
    autotest_coupon = vec.siteserve.BASKETBALL_COUPON_NAME_1
    widget_section_name = 'In-Play LIVE Basketball'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create BasketBall events
        """
        if tests.settings.backend_env != 'prod':
            # Enhanced multiple events
            self.ob_config.add_basketball_event_enhanced_multiples()
            # live event
            self.ob_config.add_basketball_event_to_autotest_league(is_live=True)
            # outright event
            self.ob_config.add_basketball_outright_event_to_autotest_league()
            # matches/competition event
            event_matches_params = self.ob_config.add_basketball_event_to_autotest_league()
            # coupons
            event_market_id = self.ob_config.market_ids[event_matches_params.event_id]['money_line']
            self.ob_config.add_event_to_coupon(market_id=event_market_id, coupon_name=None, coupon_id=self.ob_config.basketball_config.coupons[self.autotest_coupon])

    def test_001_tapclick_on_basketball_button_from_the_main_menu(self):
        """
        DESCRIPTION: Tap/Click on Basketball button from the Main Menu
        EXPECTED: 1. Basketball Page is loaded
        EXPECTED: 2. The 'Matches' tab is selected by default
        EXPECTED: 3. The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: 4. All events which are available are displayed for the League
        EXPECTED: 5. **For Mobile/Tablet:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed on the top of the list and is expanded
        EXPECTED: **For Desktop:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed as carousel above tabs
        EXPECTED: 6. **For Desktop:** 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='Basketball')
        current_tab_name = self.site.basketball.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Default tab is not "{self.expected_sport_tabs.matches}", it is "{current_tab_name}"')

        accordion_list = self.site.basketball.tab_content.accordions_list
        total_no_of_accordions = accordion_list.count_of_items
        self.assertTrue(total_no_of_accordions, msg=f'No one event section found in for sport: "{self.sport_name}"')
        expanded_sections = accordion_list.expanded_items

        if vec.racing.ENHANCED_MULTIPLES_NAME == accordion_list.first_item[0]:
            expected_expanded_section = total_no_of_accordions if total_no_of_accordions < 4 else 4
        else:
            expected_expanded_section = total_no_of_accordions if total_no_of_accordions < 3 else 3

        self.assertEqual(len(expanded_sections), expected_expanded_section, f'Actual Expanded Sections Count : "{len(expanded_sections)}" is not same as '
                                                                            f'Expected Expanded Sections Count : "{expected_expanded_section}"')

        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                em_carousel = self.site.basketball.sport_enhanced_multiples_carousel
                self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
            else:
                self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, expanded_sections,
                              msg='No "ENHANCED MULTIPLES" section found in list')

        # In-Play widget is disabled in cms for Ladbrokes Prod Desktop
        # TODO Tobe tested once In-Play widget is enabled in CMS for Ladbrokes Prod Desktop
        if self.device_type == 'desktop' and self.brand == 'bma':
            widget = self.site.sports_page.in_play_widget.items_as_ordered_dict
            if widget:
                self.assertTrue(widget, msg=f'{vec.siteserve.IN_PLAY_TAB} widget is not found on BasketBall page')
                self.assertIn(self.widget_section_name, widget.keys(),
                              msg=f'{self.widget_section_name} not found in {widget.keys()}')
            else:
                raise PreconditionNotMetException('No live basketball events found to test')

    def test_002_tapclick_on_coupons_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Coupons' tab
        EXPECTED: 1. The 'Coupons' tab is loaded
        EXPECTED: 2. Sections with events are displayed on the page and all collapsed by default
        EXPECTED: 3. It is possible to collapse/expand all of the sections by clicking the header
        EXPECTED: 4. The first 5 events load within 1 second after clicking on the section and incrementally render more events when user scrolls down
        EXPECTED: 5. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        # coupons tab is not applicable for basketball

    def test_003_select_one_event_from_the_section(self):
        """
        DESCRIPTION: Select one event from the section
        EXPECTED: The event details page is opened
        """
        # coupons tab is not applicable for basketball

    def test_004_tapclick_on_back_button_and_then_tapclick_on_outrights_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Back' button and then tap/click on 'Outrights' tab
        EXPECTED: 1. The 'Outrights' tab is loaded
        EXPECTED: 2. Leagues and Competitions are all collapsed by default
        EXPECTED: 3. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """

        def accordions_list_values():
            return wait_for_result(
                lambda: self.site.contents.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=4),
                timeout=5,
                expected_result=True,
                name='accordions list is not available',
                bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, IndexError, VoltronException)
            )

        if tests.settings.backend_env == 'prod':
            if vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper() in self.site.basketball.tabs_menu.items_names:
                self.__class__.outright_tab = self.site.basketball.tabs_menu.click_button(vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
                self.assertTrue(self.outright_tab, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
            else:
                self._logger.info("Outrights events are not present")
                self.__class__.outright_tab = False
        else:
            self.__class__.outright_tab = self.site.basketball.tabs_menu.click_button(
                vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
            self.assertTrue(self.outright_tab, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')

        if self.outright_tab:
            sections = accordions_list_values()
            self.assertTrue(sections, msg='No sections found in Outright tab')

            for section_name, section in sections.items():
                self.assertFalse(section.is_expanded(), msg=f'Event "{section_name}" is not collapsed by default')
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'Event "{section_name}" is not expanded')
                section.collapse()
                self.assertFalse(section.is_expanded(), msg=f'Event "{section_name}" is not collapsed')

            if self.device_type == 'desktop':
                widget = self.site.sports_page.in_play_widget.items_as_ordered_dict
                self.assertFalse(widget, msg=f'"{vec.siteserve.IN_PLAY_TAB}" widget is found on basketball page')

    def test_005_expand_one_event_type(self):
        """
        DESCRIPTION: Expand one event type
        EXPECTED: The list of outrights from that event type is displayed
        """
        # covered in step 04

    def test_006_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: 1. The 'In-Play' tab is loaded with the 'Live Now' /'Upcoming' sections
        EXPECTED: 2. The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 3. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        if self.device_type == 'mobile':
            self.site.basketball.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
            expected_sections = [vec.inplay.LIVE_NOW_EVENTS_SECTION, vec.inplay.UPCOMING_EVENTS_SECTION]
            sections = self.site.inplay.tab_content.items_as_ordered_dict.keys()
        else:
            is_in_play_tab_selected = self.site.contents.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
            self.assertTrue(is_in_play_tab_selected,
                             msg=f'IN-PLAY Tab is not selected')
            expected_sections = [vec.inplay.LIVE_NOW_SWITCHER, vec.inplay.UPCOMING_SWITCHER]
            sections = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict

            widget = self.site.sports_page.in_play_widget.items_as_ordered_dict
            self.assertFalse(widget, msg=f'"{vec.siteserve.IN_PLAY_TAB}" widget is found on Tennis page')

        self.assertTrue(sections, msg=f'No tabs are present in "{vec.siteserve.IN_PLAY_TAB}" tab')
        self.assertEqual(list(sections), expected_sections, msg=f'In-Play tab is not loaded with sections.'
                                                                f'Actual: "{list(sections)}",'
                                                                f'Expected: "{expected_sections}"')
