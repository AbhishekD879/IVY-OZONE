import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.other
@vtest
class Test_C65949641_Verify_popular_coupons_display_andnavigation_to_coupons(Common):
    """
    TR_ID: C65949641
    NAME: Verify popular coupons display and
navigation to coupons
    DESCRIPTION: This test case verify popular
    DESCRIPTION: coupons display and navigation
    DESCRIPTION: to coupons
    PRECONDITIONS: CMS->sport category->football->(enable)accumulators
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS->sport category->football->(enable)accumulators
        """
        # checking whether coupons tab is enable or disable
        sport_id = self.ob_config.football_config.category_id
        response = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name='coupons')
        self.__class__.coupons_tab_name = response['name'].upper
        # making coupons tab is enabled in cms if it is disable in cms
        if not response['enabled']:
            tab_id = self.cms_config.get_sport_tab_id(sport_id=sport_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=sport_id)
        self.__class__.tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                                          self.ob_config.football_config.category_id)

    def test_001_1launch_bma_application(self):
        """
        DESCRIPTION: 1.Launch BMA application
        EXPECTED: Application Launched successfully
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_navigate_to_football_page_and_clickon_coupons_tabnote_for_coral_accumulators(self):
        """
        DESCRIPTION: Navigate to football page and click
        DESCRIPTION: on coupons tab
        DESCRIPTION: Note for coral: Accumulators
        EXPECTED: Navigated to football page and coupons
        EXPECTED: tab opened
        """
        result = self.site.football.tabs_menu.click_button(self.tab_name)
        self.assertTrue(result,
                        msg=f'"{self.tab_name}" tab was not opened, active is "{self.site.football.tabs_menu.current}"')

    def test_003_find_the_popular_coupons_displayedbelow_the_featured_coupons_incoupons_tab(self):
        """
        DESCRIPTION: Find the popular coupons displayed
        DESCRIPTION: below the featured coupons in
        DESCRIPTION: coupons tab
        EXPECTED: Popular coupons displayed below the
        EXPECTED: featured coupons
        """
        # ********************** Getting expected coupons ****************************************************
        filters = [
            simple_filter(LEVELS.COUPON, attribute=ATTRIBUTES.CATEGORY_ID, operator=OPERATORS.EQUALS, value=16),
            simple_filter(LEVELS.COUPON, attribute=ATTRIBUTES.SITE_CHANNELS, operator=OPERATORS.CONTAINS, value='M'),
            exists_filter(LEVELS.COUPON,
                          simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, operator=OPERATORS.IS_FALSE))
        ]
        ss_bulider = self.ss_query_builder
        for fil in filters:
            ss_bulider.add_filter(fil)
        self.__class__.res = self.ss_req.ss_coupon(query_builder=ss_bulider)
        self.__class__.expected_coupons_list = [coupon['coupon']['name'].upper() for coupon in self.res]
        self.expected_coupons_list.sort()
        # ********************** Getting actual coupons ****************************************************
        wait_for_haul(2)
        all_coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.all_coupons = {coupon_name.upper(): coupon.items_as_ordered_dict for coupon_name, coupon in all_coupons.items()}
        actual_coupons_list = [coupon_name.upper() for coupons in self.all_coupons.values() for coupon_name in coupons]
        actual_coupons_list.sort()
        # ********************** Comparing expected and  actual coupons lists ****************************************************
        self.assertListEqual(self.expected_coupons_list, actual_coupons_list,
                             msg=f'expected coupons list is {self.expected_coupons_list} but actual coupons list {actual_coupons_list}')

    def test_004_click_on_any_of_the_popular_couponand_navigate_to_coupons_page(self):
        """
        DESCRIPTION: Click on any of the popular coupon
        DESCRIPTION: and navigate to coupons page
        EXPECTED: Coupons page is open and found
        """
        popular_coupons = self.all_coupons.get(vec.coupons.POPULAR_COUPONS.upper())
        self.assertTrue(popular_coupons,msg=f'No popular_coupons leagues are found in FE')
        random_pc_league_name, random_pc_league = next(iter(popular_coupons.items()))
        random_pc_league.click()

    def test_005_verify_edp_displayed_with_respectivecoupon_leagues_events_in_expanded_mode(self):
        """
        DESCRIPTION: Verify EDP displayed with respective
        DESCRIPTION: coupon leagues events in expanded mode
        EXPECTED: EDP displayed with respective leagues
        EXPECTED: and events in expanded mode
        """
        sleep(2)
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections,msg=f'No sections found in leagues')
        show_stats_verified = False
        for section_name, section in list(sections.items()):
            section.expand()
            if section.has_league_table_link:
                events = section.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events found in section')
                for event_name, event in events.items():
                    event.scroll_to()
                    self.assertTrue(event.has_show_stats_link, msg=f'show stats link is not display')
                    self.assertFalse(event.has_hide_stats_link, msg=f'Hide stats link is display')
                    if event.has_show_stats_link:
                        event.show_stats_link.click()
                        wait_for_haul(3)
                        self.assertTrue(event.has_coupon_stat_widget, msg = f'coupons stat widget is not display')
                        self.assertTrue(event.has_hide_stats_link, msg = f'Hide stats link is not display')
                        event.hide_stats_link.click()
                        show_stats_verified = True
                        break
            if show_stats_verified:
                section.league_table_link.click()
                break

    def test_006_click_on_league_table_of_the_respectiveleague_which_shown_below_theleague_header_and_verify_cross_button_on_the_displayed_league_table(self):
        """
        DESCRIPTION: Click on league table of the respective
        DESCRIPTION: league which shown below the
        DESCRIPTION: league header and verify cross button on the displayed league table
        EXPECTED: League table displayed with proper stats data
        EXPECTED: and league table closed on clicking cross button
        """
        # covered in step5

    def test_007_click_on_show_stats_and_verify_thedisplay_of__respective_data_and_alsoverify_the_hide_stats_which_undisplay_the_stats_data(self):
        """
        DESCRIPTION: Click on show stats and verify the
        DESCRIPTION: display of  respective data and also
        DESCRIPTION: verify the hide stats which undisplay the stats data
        EXPECTED: Show stats displayed with respective data and hide stats undisplayed the stats data
        """
        # covered in step5
