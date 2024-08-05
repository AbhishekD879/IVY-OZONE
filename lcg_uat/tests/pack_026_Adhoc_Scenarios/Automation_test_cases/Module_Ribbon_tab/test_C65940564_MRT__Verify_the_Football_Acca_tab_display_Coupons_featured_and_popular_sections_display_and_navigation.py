import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@pytest.mark.adhoc_suite
@pytest.mark.coupons
@vtest
class Test_C65940564_MRT__Verify_the_Football_Acca_tab_display_Coupons_featured_and_popular_sections_display_and_navigation(
    Common):
    """
    TR_ID: C65940564
    NAME: MRT - Verify the Football Acca tab display -Coupons featured and popular sections display and navigation
    DESCRIPTION: This test case is to Verify the Football Acca tab display -Coupons featured and popular sections display and navigation
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
    PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
    PRECONDITIONS: 3) Click on "+ Create Module ribbon tab" button to create new MRT.
    PRECONDITIONS: 4) Enter All mandatory Fields and click on save button:
    PRECONDITIONS: -Module ribbon tab title
    PRECONDITIONS: -Directive name option from dropdown like Featured, Coupon,In-play, Live stream,Multiples, next races, top bets, Build your bet
    PRECONDITIONS: -id
    PRECONDITIONS: -URL
    PRECONDITIONS: -Click on "Create" CTA button
    PRECONDITIONS: 5)Check and select below required fields in module ribbon tab configuration:
    PRECONDITIONS: -Active
    PRECONDITIONS: -IOS
    PRECONDITIONS: -Android
    PRECONDITIONS: -Windows Phone
    PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
    PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
    PRECONDITIONS: -Click on "Save changes" button
    """
    keep_browser_open = True

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should be loaded succesfully
        """
        # ****************************** Navigating to Home page ************************
        self.site.wait_content_state(state_name="Homepage")

    def test_002_verify_next_acca_tab_present_in_mrt(self):
        """
        DESCRIPTION: Verify next Acca tab present in MRT
        EXPECTED: Acca tab should be present at MRT
        """
        cms_module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        expected_module_ribbon_tab_name = next((tab['title'].upper() for tab in cms_module_ribbon_tabs if
                                           tab['visible'] is True and tab['directiveName'] == 'Coupons'), None)
        self.assertTrue(expected_module_ribbon_tab_name, msg='Module Ribbon tab with directive name Coupons is not available in CMS')
        # ****************************** Navigating to Module Ribbon Tab ************************
        module_ribbon_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        module_ribbon_tabs.get(expected_module_ribbon_tab_name).click()
        wait_for_haul(5)
        current_module_ribbon_tab_name = self.site.home.module_selection_ribbon.tab_menu.current.upper()
        self.assertEqual(expected_module_ribbon_tab_name, current_module_ribbon_tab_name,
                         msg=f'Expected module ribbon tab is {expected_module_ribbon_tab_name} but actual is {current_module_ribbon_tab_name}')

    def test_003_verify_the_display_of_acca_tab_page(self):
        """
        DESCRIPTION: verify the display of Acca tab page
        EXPECTED: Today coupons need to display on the top followed by the popular coupons
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
        all_coupons = self.site.coupon.coupons_list.items_as_ordered_dict
        self.__class__.all_coupons = {coupon_name.upper(): coupon for coupon_name, coupon in all_coupons.items()}
        actual_coupons_list = list(self.all_coupons.keys())
        actual_coupons_list.sort()
        # ********************** Comparing expected and  actual coupons lists ****************************************************
        self.assertListEqual(self.expected_coupons_list, actual_coupons_list, msg=f'expected coupons list is {self.expected_coupons_list} but actual coupons list {actual_coupons_list}')

    def test_004_click_on_any_one_of_the_coupon_and_verify_the_page(self):
        """
        DESCRIPTION: Click on any one of the coupon and verify the page
        EXPECTED: Selected coupan and market releated data need to be loaded
        """
        # ********************** Navigating to one of the Coupon ****************************************************
        self.all_coupons.get(self.expected_coupons_list[0]).click()
        wait_for_haul(5)
        # ********************** Verification of Coupon details ****************************************************
        actual_class_id = self.device.get_current_url().split('/')[-1]
        coupon_ids = {coupon['coupon']['name'].upper(): coupon['coupon']['id'] for coupon in self.res}
        expected_class_id = coupon_ids.get(self.expected_coupons_list[0])
        self.assertEqual(expected_class_id, actual_class_id, msg=f'Expected class id is {expected_class_id} but actual is {actual_class_id}')