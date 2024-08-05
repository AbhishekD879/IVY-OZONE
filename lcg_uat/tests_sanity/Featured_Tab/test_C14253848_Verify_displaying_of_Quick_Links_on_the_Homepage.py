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
@pytest.mark.high
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.homepage_featured
@pytest.mark.quick_links
@pytest.mark.mobile_only
@pytest.mark.cms
@pytest.mark.slow
@pytest.mark.safari
@vtest
class Test_C14253848_Verify_displaying_of_Quick_Links_on_the_Homepage(BaseFeaturedTest):
    """
    TR_ID: C14253848
    VOL_ID: C57995347
    NAME: Verify displaying of 'Quick Links' on the Homepage
    DESCRIPTION: This test case verifies displaying of 'Quick Links' on the Homepage
    DESCRIPTION: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA34140
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to the Homepage > 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) Go to CMS > Sports Pages > Homepage and configure 1 active 'Quick link' for the Homepage
    PRECONDITIONS: 2) Set 'Active'/'Inactive' flag to 'Active' for the configured 'Quick link' for the Homepage to make it visible on the front end
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments++to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    quick_link_object = None
    max_amount = 3

    @classmethod
    def custom_tearDown(cls):
        if tests.settings.cms_env != 'prd0':
            cls.get_cms_config().update_system_configuration_structure(
                config_item='Sport Quick Links', field_name='maxAmount', field_value=cls.cms_number_of_quick_links)

    def verify_quick_link_is_not_present_on_page(self, page):
        if page.tab_content.has_quick_links():
            names = page.tab_content.quick_links.items_as_ordered_dict.keys()
            presense_status = any([quick_link_name in names for quick_link_name in self.quick_link_names])
            self.assertFalse(presense_status, msg=f'At least one Quick link from "{self.quick_link_names}" is present in "{names}"')
        else:
            self.assertFalse(page.tab_content.has_quick_links(expected_result=False),
                             msg=f'Quick links module is shown on page')

    def navigate_to_homepage_featured_tab(self):
        """
        This method navigates to Homepage and checks if the Featured tab selected
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        featured_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)

    def verify_redirection_from_quick_link(self):
        """
        This method checks redirection from Quick link
        """
        self.site.wait_content_state(state_name='Football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url: "{current_url}" '
                             f'is not the same as expected: "{self.destination_url}"')

    def click_on_quick_link(self, name=None):
        """
        This method clicks on specified Quick link
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(name)
        self.assertTrue(quick_link, msg=f'Quick link "{name}" not found')
        quick_link.click()

    def verify_quick_links_rows_blocks(self):
        """
        This method verifies whether Quick links are displayed as rows or blocks
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick Links found on page')
        quick_links_x_list, quick_links_y_list, quick_links_width = [], [], []
        window_width = self.device.driver.get_window_size().get('width')
        for item in quick_links.keys():
            quick_links_y_list.append(quick_links.get(item).location.get('y'))
            quick_links_x_list.append(quick_links.get(item).location.get('x'))
            quick_links_width.append(quick_links.get(item).size.get('width'))
            if self.brand == 'ladbrokes':
                quick_link_width = quick_links.get(item).size.get('width')
                self.assertAlmostEqual(quick_link_width, window_width, delta=31,
                                       msg=f'Quick Link "{item}" is not stretched to the width of the screen. '
                                           f'Width: {quick_link_width} != {window_width}')
        if self.brand == 'ladbrokes':
            self.assertListEqual(quick_links_y_list, sorted(quick_links_y_list),
                                 msg='Quick Links are not displayed as rows in the list')
        else:
            self.assertListEqual(quick_links_x_list, sorted(quick_links_x_list),
                                 msg='Quick Links are not displayed as rows in the list')
            self.assertGreater(len(set(quick_links_x_list + quick_links_y_list)), 2,
                               msg='Quick Links containers does not have flexible width')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        self.__class__.cms_number_of_quick_links = sport_quick_links.get('maxAmount')
        if not self.cms_number_of_quick_links:
            raise CmsClientException('Max number of quick links is not configured in CMS')
        self.__class__.homepage_id = {'homepage': 0}
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for Homepage')
        self.__class__.quick_link_names = ['Autotest ' + Faker().city() + ' ' for _ in range(0, self.max_amount)]
        self.quick_link_names[1] *= 6
        self.__class__.quick_link_object = self.cms_config.create_quick_link(
            title=self.quick_link_names[0], sport_id=self.homepage_id.get('homepage'), destination=self.destination_url)
        self.navigate_to_homepage_featured_tab()

    def test_001_verify_displaying_of_configured_quick_link_on_homepage(self):
        """
        DESCRIPTION: Verify displaying of configured 'Quick Link' on Homepage
        EXPECTED: * 'Quick links' container is displayed on the Homepage
        EXPECTED: * Configured 'Quick link' is displayed on the Homepage
        EXPECTED: * 'Quick link' is stretched to fit the width of the screen
        """
        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[0], timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[0])
            self.verify_quick_link_displayed(name=self.quick_link_names[0])

    def test_002_click_on_the_newly_configured_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the configured 'Quick link'
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        self.click_on_quick_link(name=self.quick_link_names[0])
        self.verify_redirection_from_quick_link()

    def test_003_configure_2nd_quick_link_for_homepage_with_a_long_name(self):
        """
        DESCRIPTION: Go to CMS > Sports Pages > Homepage
        DESCRIPTION: Configure 2nd Quick link for Homepage with a long name (long enough in order not to fit the remaining width of the screen)
        EXPECTED: * 'Quick links' container is displayed on the Homepage
        EXPECTED: * Configured 'Quick links' are displayed on the Homepage
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed in the carousel as 2 separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: * 2nd 'Quick link' is cut off. The only part that can fit the remaining width of the screen is shown
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as a fixed vertical list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        self.cms_config.create_quick_link(
            title=self.quick_link_names[1], sport_id=self.homepage_id.get('homepage'), destination=self.destination_url)
        self.navigate_to_homepage_featured_tab()
        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[0], timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[0])
            self.verify_quick_link_displayed(name=self.quick_link_names[0])

        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[1], timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[1])
            self.verify_quick_link_displayed(name=self.quick_link_names[1])

        self.verify_quick_links_rows_blocks()

    def test_004_click_on_the_newly_configured_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the newly configured 'Quick link'
        DESCRIPTION: Verify redirection to the specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        self.click_on_quick_link(name=self.quick_link_names[1])
        self.verify_redirection_from_quick_link()

    def test_005_set_the_max_number_of_quick_links_to_be_displayed_in_one_time_period_to_6(self):
        """
        DESCRIPTION: Go to CMS > System Configuration > Structure > Sport Quick Links module and set the max number of quick links to be displayed in one Time period to 6
        """
        self.cms_config.update_system_configuration_structure(
            config_item='Sport Quick Links', field_name='maxAmount', field_value=self.max_amount)
        result = wait_for_result(
            lambda: int(self.cms_config.get_system_configuration_item('Sport Quick Links').get(
                'maxAmount')) == self.max_amount,
            name='Sport Quick Links "maxAmount" value to be changed', poll_interval=5, timeout=60)
        self.assertTrue(result, msg=f'"maxAmount" value is not set to: {self.max_amount}')

    def test_006_configure_more_quick_links_in_order_to_have_6_active_quick_links_for_the_current_time_period(self):
        """
        DESCRIPTION: Go to CMS > Sports Pages > Homepage and configure more 'Quick links' in order to have 6 active 'Quick links' for the current Time period
        """
        self.navigate_to_homepage_featured_tab()
        for item in range(2, self.max_amount):
            self.cms_config.create_quick_link(
                title=self.quick_link_names[item], sport_id=self.homepage_id.get('homepage'), destination=self.destination_url)

            if self.is_safari:
                self.verify_quick_link_displayed(name=self.quick_link_names[item], timeout=40)
            else:
                self.wait_for_quick_link(name=self.quick_link_names[item])

    def test_007_verify_that_6_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to the application Homepage
        DESCRIPTION: Verify that maximum amount of configured 'Quick links' are displayed
        EXPECTED: * 'Quick links' container is displayed on the Homepage
        EXPECTED: * Configured 'Quick links' are displayed on the Homepage
        EXPECTED: Maximum amount of configured 'Quick links' are displayed
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed as separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: * 'Quick links' that don't fit the width of the screen are cut off
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as a fixed vertical list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick Links found on page')
        # Using API we can create more than 'maxAmount' Quick links. Mainly occurs on HL
        self.softAssert(self.assertLessEqual, self.max_amount, len(list(quick_links.items())),
                        msg=f'Actual number of Quick links: {len(list(quick_links.items()))}, '
                            f'is not as expected: {self.max_amount}')
        for item in range(0, self.max_amount):
            self.verify_quick_link_displayed(name=self.quick_link_names[item])
        self.verify_quick_links_rows_blocks()

    def test_008_click_on_one_of_the_newly_configured_quick_links_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on one of the newly configured 'Quick links'
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        self.click_on_quick_link(name=choice(self.quick_link_names))
        self.verify_redirection_from_quick_link()

    def test_009_verify_displaying_of_quick_links_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on the Homepage (e.g. InPlay, Coupons, Next races, Build your bet, etc.)
        DESCRIPTION: Verify displaying of 'Quick links' on other tabs
        EXPECTED: * Configured 'Quick links' are displayed only on the 'Featured' tab
        EXPECTED: * 'Quick links' container is NOT displayed on other 'Homepage' tabs
        EXPECTED: * Configured 'Quick links' are NOT displayed on other 'Homepage' tabs
        """
        self.navigate_to_homepage_featured_tab()
        inplay_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
        self.site.home.module_selection_ribbon.tab_menu.click_button(inplay_featured_tab_name)
        self.assertFalse(self.site.home.tab_content.has_quick_links(expected_result=False),
                         msg=f'Quick links module is shown on InPlay tab')

    def test_010_observe_the_quick_links_section_and_verify_displaying_of_homepage(self):
        """
        DESCRIPTION: Go to any Sports page (e.g. Football, Tennis) and observe the 'Quick links' section
        DESCRIPTION: Verify displaying of Homepage configured 'Quick links' on any Sports landing page
        EXPECTED: * Configured 'Quick link' for Homepage is NOT displayed on other Sports pages
        EXPECTED: * Only 'Quick links' that are configured for Sports landing page are shown (if there are some)
        EXPECTED: * 'Quick links' container and links are NOT displayed If no 'Quick links' are configured for Sports pages
        """
        self.navigate_to_page(name='horse-racing/featured')
        self.site.wait_content_state(state_name='Horseracing')
        self.verify_quick_link_is_not_present_on_page(page=self.site.horse_racing)

        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        self.verify_quick_link_is_not_present_on_page(page=self.site.basketball)

    def test_011_set_flag_for_the_configured_quick_link_for_homepage_to_inactive(self):
        """
        DESCRIPTION: Go to CMS > Sports Pages > Homepage > Quick Links
        DESCRIPTION: Set "Active"/"Inactive" flag for the configured 'Quick link' for Homepage to 'Inactive'
        """
        self.cms_config.change_quick_link_state(active=False, quick_link_object=self.quick_link_object)

    def test_012_verify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Navigate to the 'Featured' tab on the Homepage
        DESCRIPTION: Verify that 'Quick link' is no longer displayed
        EXPECTED: * 'Quick links' container is NOT displayed
        EXPECTED: * 'Quick link' is no longer displayed
        """
        self.navigate_to_homepage_featured_tab()

        if self.is_safari:
            self.verify_quick_link_displayed(name=self.quick_link_names[0], expected_result=False, timeout=40)
        else:
            self.wait_for_quick_link(name=self.quick_link_names[0], expected_result=False)
            self.verify_quick_link_displayed(name=self.quick_link_names[0], expected_result=False)
