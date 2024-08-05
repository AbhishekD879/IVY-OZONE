import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870191_Verify_Golf_journey(BaseSportTest):
    """
    TR_ID: C44870191
    NAME: Verify Golf journey
    PRECONDITIONS: "Site is loaded,
    PRECONDITIONS: User navigates to Sport page page via Homepage -> Carousel Link or Via Homepage -> All Sports (Menu) -> Golf"
    """
    keep_browser_open = True

    def accordion_expand_collapse(self, accordions):
        if accordions is not None:
            for accordion in accordions[:3]:
                if accordion.is_expanded():
                    accordion.collapse()
                    self.device.driver.implicitly_wait(5)
                    self.assertFalse(wait_for_result(lambda: accordion.is_expanded(), timeout=7),
                                     msg='Accordion is not collapsed ')
                else:
                    accordion.expand()
                    self.device.driver.implicitly_wait(5)
                    self.assertTrue(wait_for_result(lambda: accordion.is_expanded(), timeout=5),
                                    msg='Accordion is not expanded ')
        else:
            self._logger.info('*** No events are available')

    def test_001_verify_golf_journey___navigation_from_different_pages_and_display(self):
        """
        DESCRIPTION: Verify Golf journey - navigation from different pages and display
        EXPECTED: User should be able to navigate successfully
        """
        self.site.wait_content_state(state_name='HomePage')
        if self.device_type == 'desktop':
            all_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(all_sports, msg='sports are  not available')
            all_sports[vec.sb.GOLF].click()
        else:
            if self.brand == 'ladbrokes':
                self.site.home.menu_carousel.click_item(vec.sb.GOLF)
            else:
                self.site.home.menu_carousel.click_item(vec.sb.GOLF.upper())
        self.site.wait_content_state(vec.sb.GOLF)

    def test_002_verify_collapseexpandable_accordion(self):
        """
        DESCRIPTION: Verify Collapse/Expandable accordion
        EXPECTED: Collapsible and expandable accordions should be accessible
        """
        # covered in step 004

    def test_003_verify_display_of_landing_page_and_all_tabs_and_sub_tabs_are_accessible_journey_is_smooth_user_can_navigate_forward_and_backwards_pages_load_and_all_features_including_banners_links_are_displayed(self):
        """
        DESCRIPTION: Verify display of landing page and all tabs and sub tabs are accessible, journey is smooth, user can navigate forward and backwards, pages load and all features including Banners, links, are displayed.
        EXPECTED: Sub tabs, landing page and  all other tabs should be accessible
        """
        # sub tabs covered in step 004
        if self.device_type == 'desktop':
            self.site.golf.header_line.back_button.click()
            self.site.wait_content_state(state_name='HomePage')
            self.device.go_back()

        self.assertTrue(wait_for_result(lambda: self.site.home.aem_banner_section.is_displayed(), timeout=5),
                        msg="Banner section is not displayed")
        if self.device_type == 'mobile':
            self.navigate_to_page('Homepage')
            if self.brand == 'ladbrokes':
                self.site.home.menu_carousel.click_item('Golf', timeout=5)
            else:
                self.site.home.menu_carousel.click_item('GOLF')
            self.site.wait_content_state('Golf')

    def test_004_verify_that_user_is_able_to_switch_between_the_tabs_and_subtabs_and_each_tab_displays_data_grouped_by_type_as_links_or_expandable_areas_as_per_requirements_and_functionality_works_fine_for_each_one_in_play_events_outright_coupons_etc(self):
        """
        DESCRIPTION : Verify that user is able to switch between the tabs and subtabs, and each tab displays data grouped by Type,
         as links or expandable areas, as per requirements and functionality works fine for each one: In Play, Events, Outright, Coupons, etc.
        EXPECTED : User journey between the tabs and subtabs should be smooth enough
        """
        sections = self.site.golf.tabs_menu.items_as_ordered_dict
        self.assertTrue(sections, msg='No tabs are available in golf page')
        if self.device_type == 'desktop':
            sections.get(vec.siteserve.IN_PLAY_TAB).click()
            inplay_subtabs = list(self.site.golf.tab_content.grouping_buttons.items_as_ordered_dict.values())
            for item in range(len(inplay_subtabs)):
                inplay_subtabs = list(self.site.golf.tab_content.grouping_buttons.items_as_ordered_dict.values())
                inplay_subtabs[item].click()
                accordions = list(self.site.golf.tab_content.accordions_list.items_as_ordered_dict.values())
                self.accordion_expand_collapse(accordions)

            sections.get(vec.sb.EVENTS.upper()).click()
            events_groups = self.site.golf.date_tab.items_as_ordered_dict.values()
            for group in events_groups:
                group.click()
                try:
                    accordions = list(self.site.golf.tab_content.accordions_list.items_as_ordered_dict.values())
                    self.accordion_expand_collapse(accordions)
                except VoltronException:
                    self._logger.info("**** No events are found ")

            sections.get(vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()).click()
            outrights = list(self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values())
            self.accordion_expand_collapse(outrights)
            sections.get(vec.sb.SPORT_TABS_INTERNAL_NAMES.competitions.upper()).click()
        else:
            for section in list(sections.values()):
                section.click()
                accordions = list(self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values())
                self.accordion_expand_collapse(accordions)

    def test_005_verify_that_on_edp_user_is_able_to_switch_between_the_markets_and_the_page_is_updated_with_the_correct_specific_market_display_and_respective_data(self):
        """
        DESCRIPTION: Verify that on EDP user is able to switch between the markets, and the page is updated with the correct specific Market display and respective data
        EXPECTED: Successful pages should be loaded
        """
        accordions = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg='No accordions are available')
        accordion = list(accordions.values())[0]
        if not accordion.is_expanded():
            accordion.expand()
        event_name, event = list(accordion.items_as_ordered_dict.items())[0]
        self.device.driver.implicitly_wait(5)
        event.click()
        if self.device_type == 'desktop':
            page_title = list(self.site.sport_event_details.breadcrumbs.items_as_ordered_dict.keys())[-1]
            self.assertIn(event_name, page_title, msg='Event details page is not loaded')
        else:
            if self.brand == 'ladbrokes':
                page_title = self.site.sport_event_details.header_line.page_title
                page_title.click()
                self.site.wait_content_state_changed(timeout=15)
                self.assertTrue(page_title, msg='Event details page is not loaded')
                markets_tabs_list = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict
                self.assertTrue(markets_tabs_list, msg='No markets found')
                for tab_name, tab in list(markets_tabs_list.items()):
                    tab.click()
                    self.assertTrue(tab_name, msg='Market display page is not loaded')
            else:
                page_title = self.site.sport_event_details.event_title_bar
                self.assertTrue(page_title, msg='Event details page is not loaded')
