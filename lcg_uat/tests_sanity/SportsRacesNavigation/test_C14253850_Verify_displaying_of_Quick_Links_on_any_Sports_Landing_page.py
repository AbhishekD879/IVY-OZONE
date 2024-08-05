from random import choice

import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # we can not create quick links on prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.navigation
@pytest.mark.module_ribbon
@pytest.mark.homepage_featured
@pytest.mark.quick_links
@pytest.mark.mobile_only
@pytest.mark.football
@pytest.mark.sports
@pytest.mark.cms
@pytest.mark.safari
@vtest
class Test_C14253850_Verify_displaying_of_Quick_Links_on_any_Sports_Landing_page(BaseFeaturedTest):
    """
    TR_ID: C14253850
    VOL_ID: C58068809
    NAME: Verify displaying of 'Quick Links' on any Sports Landing page
    DESCRIPTION: This test case verifies displaying of Quick Links on All Sports landing pages
    DESCRIPTION: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    PRECONDITIONS: 1. Go to CMS -> Sport Pages-><Sport name> -> Quick Links  and configure 1 active Quick link for <Sport name> landing page
    PRECONDITIONS: 2. Set 'Active'/'Inactive' flag to 'Active' for the configured 'Quick link' for the <Sport name> landing page to make it visible on the front end
    PRECONDITIONS: 3. Load the application
    PRECONDITIONS: 4. Navigate to <Sport name> landing page
    PRECONDITIONS: [Tab name]- This tab is selected by default after accessing the Sport Landing Page. The name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in the application
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Max amount of Quick Links, which can be displayed, is configurable in the CMS (CMS > System configuration > Structure > Sport Quick Links > maxAmount)
    """
    keep_browser_open = True
    destination_url = f'https://{tests.HOSTNAME}/sport/tennis/matches'
    quick_link_object = None
    max_amount = 3

    @classmethod
    def custom_tearDown(cls):
        if tests.settings.cms_env != 'prd0':
            cls.get_cms_config().update_system_configuration_structure(
                config_item='Sport Quick Links', field_name='maxAmount', field_value=cls.cms_number_of_quick_links)

    def navigate_to_sport_landing_page(self):
        """
        This method navigates to the Football landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

    def verify_selected_tab_for_sport(self):
        """
        This method verifies whether default tab for sport is selected
        """
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Current tab "{current_tab}"'
                             f'is not as expected "{self.expected_sport_tabs.matches}"')

    def verify_redirection_from_quick_link(self):
        """
        This method checks redirection from Quick link
        """
        self.site.wait_content_state(state_name='Tennis')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url: "{current_url}" '
                             f'is not the same as expected: "{self.destination_url}"')

    def click_on_quick_link(self, name=None):
        """
        This method clicks on specified Quick link
        """
        quick_links = self.site.football.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(name)
        self.assertTrue(quick_link, msg=f'Quick link "{name}" not found')
        quick_link.click()

    def verify_quick_links_rows_blocks(self):
        """
        This method verifies whether Quick links are displayed as rows or blocks
        """
        quick_links = self.site.football.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick Links found on page')
        quick_links_x_list, quick_links_y_list, quick_links_width = [], [], []
        window_width = self.device.driver.get_window_size().get('width')
        for item in quick_links.keys():
            quick_links_y_list.append(quick_links.get(item).location.get('y'))
            quick_links_x_list.append(quick_links.get(item).location.get('x'))
            quick_links_width.append(quick_links.get(item).size.get('width'))
            if self.brand == 'ladbrokes':
                quick_link_width = quick_links.get(item).size.get('width')
                self.assertAlmostEqual(quick_link_width, window_width, delta=25,
                                       msg=f'Quick Link "{item}" is not stretched to the width of the screen. '
                                           f'Width: {quick_link_width} != {window_width}')
        if self.brand == 'ladbrokes':
            self.assertListEqual(quick_links_y_list, sorted(quick_links_y_list),
                                 msg='Quick Links are not displayed as rows in the list')
        else:
            self.assertListEqual(quick_links_x_list, sorted(quick_links_x_list),
                                 msg='Quick Links are not displayed as rows in the list')
            self.assertGreater(len(set(quick_links_width)), 1,
                               msg='Quick Links containers does not have flexible width')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages -> <Sport name> -> Quick Links and configure 1 active Quick link for <Sport name> landing page
        DESCRIPTION: Set 'Active'/'Inactive' flag to 'Active' for the configured 'Quick link' for the <Sport name> landing page to make it visible on the front end
        DESCRIPTION: Load the application
        DESCRIPTION: Navigate to <Sport name> landing page
        """
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        self.__class__.cms_number_of_quick_links = sport_quick_links.get('maxAmount')
        if not self.cms_number_of_quick_links:
            raise CmsClientException('Max number of quick links is not configured in CMS')
        homepage_id = {'homepage': 0}
        if self.is_quick_link_disabled_for_sport_category(sport_id=homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for Homepage')
        self.__class__.football_page_id = {'football': self.ob_config.backend.ti.football.category_id}
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.football_page_id.get('football')):
            raise CmsClientException('"Quick links" module is disabled for football')
        self.__class__.quick_link_names = ['Autotest ' + Faker().city() + ' ' for _ in range(0, self.max_amount)]
        self.quick_link_names[1] *= 6
        self.__class__.quick_link_object = self.cms_config.create_quick_link(
            title=self.quick_link_names[0], sport_id=self.football_page_id.get('football'), destination=self.destination_url)
        self.navigate_to_sport_landing_page()

    def test_001_verify_displaying_of_configured_quick_link_on_sport_landing_page(self):
        """
        DESCRIPTION: Verify displaying of configured 'Quick link' is displayed on <Sport name> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * 'Quick links' container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured 'Quick link' is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * 'Quick link' is stretched to fit the width of the screen
        """
        self.verify_selected_tab_for_sport()
        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[0], page_name='football', timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[0], delimiter='42/16,')
            self.verify_quick_link_displayed(name=self.quick_link_names[0], page_name='football')

    def test_002_click_anywhere_on_the_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the configured quick link
        DESCRIPTION: Verify redirection to specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        self.click_on_quick_link(name=self.quick_link_names[0])
        self.verify_redirection_from_quick_link()

    def test_003_configure_2nd_quick_link_for_sport_name_landing_page_with_a_long_name(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> <Sport name> -> Quick Links
        DESCRIPTION: Configure 2nd Quick link for <Sport name> landing page with a long name
        DESCRIPTION: (Long enough in order not to fit the remaining width of the screen)
        """
        self.cms_config.create_quick_link(
            title=self.quick_link_names[1], sport_id=self.football_page_id.get('football'), destination=self.destination_url)

    def test_004_verify_that_2_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to the application <Sport name> landing page
        DESCRIPTION: Verify that 2 configured 'Quick links' are displayed
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * 'Quick links' container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured 'Quick links' are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed in one row as separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as rows in the list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        self.navigate_to_sport_landing_page()
        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[0], page_name='football', timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[0], delimiter='42/16,')
            self.verify_quick_link_displayed(name=self.quick_link_names[0], page_name='football')
        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='football', timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[1], delimiter='42/16,')
            self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='football')
        self.verify_quick_links_rows_blocks()

    def test_005_click_anywhere_on_the_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated  to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        self.click_on_quick_link(name=self.quick_link_names[1])
        self.verify_redirection_from_quick_link()

    def test_006_set_the_max_amount_of_quick_links_to_be_displayed(self):
        """
        DESCRIPTION: Go to CMS -> System Configuration -> Structure -> Sport Quick Links module
        DESCRIPTION: Set the max number of 'Quick links' to be displayed
        """
        self.cms_config.update_system_configuration_structure(
            config_item='Sport Quick Links', field_name='maxAmount', field_value=self.max_amount)
        result = wait_for_result(
            lambda: int(self.cms_config.get_system_configuration_item('Sport Quick Links').get('maxAmount')) == self.max_amount,
            name='Sport Quick Links "maxAmount" value to be changed', poll_interval=5, timeout=60)
        self.assertTrue(result, msg=f'"maxAmount" value is not set to: {self.max_amount}')

    def test_007_configure_more_quick_links_in_order_to_have_maximum_amount_of_active_quick_links_for_the_current_time_period(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> <Sport name> -> Quick Links
        DESCRIPTION: Configure more 'Quick links' in order to have maximum amount of active 'Quick links' for the current Time period
        """
        self.navigate_to_sport_landing_page()
        for item in range(2, self.max_amount):
            self.cms_config.create_quick_link(
                title=self.quick_link_names[item], sport_id=self.football_page_id.get('football'), destination=self.destination_url)
            if self.is_safari:
                self.verify_quick_link_displayed(name=self.quick_link_names[item], timeout=40)
            else:
                self.wait_for_quick_link(name=self.quick_link_names[item], delimiter='42/16,')

    def test_008_verify_that_maximum_amount_of_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to the application <Sport name> landing page
        DESCRIPTION: Verify that maximum amount of configured 'Quick links' are displayed
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * 'Quick links' container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured 'Quick links' are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed as separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as rows in the list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        quick_links = self.site.football.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick Links found on page')
        # Using API we can create more than 'maxAmount' Quick links. Mainly occurs on HL
        self.softAssert(self.assertLessEqual, len(list(quick_links.items())), self.max_amount,
                        msg=f'Actual number of Quick links: {len(list(quick_links.items()))}, '
                            f'is not as expected: {self.max_amount}')
        for item in range(0, self.max_amount):
            self.verify_quick_link_displayed(name=self.quick_link_names[item], page_name='football')
        self.verify_quick_links_rows_blocks()

    def test_009_click_anywhere_on_one_of_the_quick_links_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on one of the newly configured 'Quick links'
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        self.click_on_quick_link(name=choice(self.quick_link_names))
        self.verify_redirection_from_quick_link()

    def test_010_select_any_other_tab_on_the_sport_name_landing_page_and_verify_displaying_of_quick_links_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on the <Sport name> landing page (e.g. Outrights, Coupons, etc.)
        DESCRIPTION: Verify displaying of 'Quick links' on other tabs
        EXPECTED: * Configured 'Quick links' are displayed only on the <Sport name> landing page -> 'Matches' tab
        EXPECTED: * 'Quick links' container is NOT displayed on other tabs on <Sport name> landing page
        EXPECTED: * Configured 'Quick links' are NOT displayed on other tabs on <Sport name> landing page
        """
        self.navigate_to_sport_landing_page()
        self.site.football.tabs_menu.click_button(button_name=self.expected_sport_tabs.competitions)
        self.assertFalse(self.site.football.tab_content.has_quick_links(expected_result=False),
                         msg=f'Quick links module is shown on "{self.expected_sport_tabs.competitions}" tab')

    def test_011_on_the_homepage_featured_tab_and_verify_displaying_of_sport_landing_page_configured_quick_links_on_the_homepage(self):
        """
        DESCRIPTION: Go to the Homepage -> 'Featured' tab and observe the 'Quick links' section
        DESCRIPTION: Verify displaying of <Sport name> landing page configured 'Quick links' on the Homepage
        EXPECTED: * Configured 'Quick link' for <Sport name> landing page is NOT displayed on the Homepage
        EXPECTED: * Only 'Quick links' that are configured for the Homepage are shown (if there are some)
        EXPECTED: 'Quick links' container and links are NOT displayed If no 'Quick links' are configured for the Homepage
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        featured_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
        if self.site.home.tab_content.has_quick_links():
            random_quick_link_name = choice(self.quick_link_names)
            if self.is_safari:
                self.verify_quick_link_displayed(name=random_quick_link_name, expected_result=False, timeout=40)
            else:
                self.wait_for_quick_link(name=random_quick_link_name, expected_result=False)
                self.verify_quick_link_displayed(name=random_quick_link_name, expected_result=False)

    def test_012_set_active_inactive_flag_for_the_configured_quick_link_for_sport_name_landing_page_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> <Sport name> -> Quick Links
        DESCRIPTION: Set "Active"/"Inactive" flag for the configured 'Quick link' for <Sport name> landing page to 'Inactive'
        """
        self.cms_config.change_quick_link_state(active=False, quick_link_object=self.quick_link_object)

    def test_013_navigate_to_the_sport_landing_page_and_verify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to the app
        DESCRIPTION: Navigate to the <Sport name> landing page
        DESCRIPTION: Verify that 'Quick link' is no longer displayed
        EXPECTED: * 'Quick links' container is NOT displayed
        EXPECTED: * 'Quick link' is no longer displayed
        """
        self.navigate_to_sport_landing_page()
        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[0], expected_result=False, page_name='football', timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[0], expected_result=False, delimiter='42/16,')
            self.verify_quick_link_displayed(name=self.quick_link_names[0], expected_result=False, page_name='football')
