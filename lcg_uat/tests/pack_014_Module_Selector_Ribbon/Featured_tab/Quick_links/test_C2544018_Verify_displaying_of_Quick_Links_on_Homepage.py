import random
from time import sleep

import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.prod # we can not create quick links on prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.module_ribbon
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.featured
@pytest.mark.medium
@vtest
class Test_C2544018_Verify_displaying_of_Quick_Links_on_Homepage(BaseFeaturedTest):
    """
    TR_ID: C2544018
    VOL_ID: C9698730
    NAME: Verify displaying of Quick links on Homepage
    DESCRIPTION: This test case verifies displaying of Quick links on Homepage
    PRECONDITIONS: 1. Go to CMS > Sport Pages > Homepage and configure 1 active Quick link for Homepage
    PRECONDITIONS: 2. Load oxygen application and navigate to Featured tab
    """
    keep_browser_open = True
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'

    def navigate_to_homepage_featured_tab(self):
        """
        This method navigates to Homepage and checks if the Featured tab selected
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Home')

        selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(selected_tab, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                         msg=f'Selected tab is: "{selected_tab}" '
                         f'instead of: "{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}"')

    def verify_redirection_from_quick_link(self):
        """
        This method checks redirection from Quick link
        """
        self.site.wait_content_state('football')

        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url: "{current_url}" is not the same as expected: "{self.destination_url}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')
        self.__class__.cms_number_of_quick_links = int(sport_quick_links['maxAmount'])
        self.__class__.quick_link_names = ['Autotest ' + Faker().city() for _ in range(0, self.cms_number_of_quick_links)]

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link = self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                                                      sport_id=self.homepage_id.get('homepage'),
                                                                      destination=self.destination_url)
        self.navigate_to_homepage_featured_tab()

    def test_001_verify_displaying_of_configured_quick_link_on_homepage(self):
        """
        DESCRIPTION: Verify displaying of configured Quick link on Homepage
        EXPECTED: * Quick links container is displayed on Homepage
        EXPECTED: * Configured Quick link is displayed on Homepage
        EXPECTED: * Quick link is stretched to fit the width of the screen
        """
        self.wait_for_quick_link(name=self.quick_link_names[0])
        self.verify_quick_link_displayed(name=self.quick_link_names[0])

    def test_002_click_on_the_configured_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the configured Quick link
        DESCRIPTION: Verify redirection to specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')

        quick_link = quick_links.get(self.quick_link_names[0])
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_names[0]}" not found')

        quick_link.click()
        self.verify_redirection_from_quick_link()

    def test_003_in_cms_and_configure_2nd_quick_link(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > Homepage and configure 2nd Quick link
        """
        self.__class__.quick_link = self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                                                      sport_id=self.homepage_id.get('homepage'),
                                                                      destination=self.destination_url)

    def test_004_on_oxygen_homepage_verify_that_2_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Homepage and verify that 2 configured Quick links are displayed
        EXPECTED: * Quick links container is displayed on Homepage
        EXPECTED: * Configured Quick links are displayed on Homepage
        """
        self.navigate_to_homepage_featured_tab()

        self.wait_for_quick_link(name=self.quick_link_names[1])
        self.verify_quick_link_displayed(name=self.quick_link_names[0])
        self.verify_quick_link_displayed(name=self.quick_link_names[1])

    def test_005_click_on_the_new_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')

        quick_link = quick_links.get(self.quick_link_names[1])
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_names[1]}" not found')

        quick_link.click()
        self.verify_redirection_from_quick_link()

    def test_006_in_cms_and_configure_3rd_quick_link_for_homepage_with_a_long_name(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages -> Homepage and configure 3rd Quick link for Homepage with a long name
        DESCRIPTION: (Long enough in order not to fit the remaining width of the screen)
        """
        self.__class__.quick_link = self.cms_config.create_quick_link(title=self.quick_link_names[2],
                                                                      sport_id=self.homepage_id.get('homepage'),
                                                                      destination=self.destination_url)

    def test_007_in_oxygen_homepage_verify_that_3_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Homepage and verify that 3 configured Quick links are displayed
        EXPECTED: * Quick links container is displayed on Homepage
        EXPECTED: * Configured Quick links are displayed on Homepage
        """
        self.navigate_to_homepage_featured_tab()
        self.wait_for_quick_link(name=self.quick_link_names[2])

        for item in range(0, 3):
            self.verify_quick_link_displayed(name=self.quick_link_names[item])

    def test_008_click_on_the_newly_configured_quick_link_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated  to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')

        quick_link = quick_links.get(self.quick_link_names[2])
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_names[2]}" not found')

        quick_link.click()
        self.verify_redirection_from_quick_link()

    def test_009_in_cms_set_max_number_of_quick_links_to_be_displayed_to_6(self):
        """
        DESCRIPTION: Go to CMS > System Configuration > Structure > Sport Quick links module
        DESCRIPTION: Set max number of quick links to be displayed in one Time period to 6
        """
        # Can not automate because of system config. We can get only actual max number of quick links
        self.navigate_to_homepage_featured_tab()
        sports_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links')
        if not sports_quick_links:
            sports_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        if not sports_quick_links:
            raise CmsClientException('"Sport Quick Links" section was not found in CMS')

    def test_010_in_cms_configure_3_more_quick_links_in_order_to_have_6_active_quick_links(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage and configure 3 more Quick links
        DESCRIPTION: In order to have 6 active Quick links for current Time period
        """
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        for item in range(3, self.cms_number_of_quick_links):
            self.__class__.quick_link = self.cms_config.create_quick_link(title=self.quick_link_names[item],
                                                                          sport_id=self.homepage_id.get('homepage'),
                                                                          destination=self.destination_url)
            sleep(10)  # wait for changes from CMS to be available for Featured MS
            self.wait_for_quick_link(name=self.quick_link_names[item])

    def test_011_go_to_oxygen_application_homepage_and_verify_that_6_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Homepage and verify that 6 configured Quick links are displayed
        EXPECTED: * Quick links container is displayed on Homepage
        EXPECTED: * Configured Quick links are displayed on Homepage
        EXPECTED: * 6 Quick links are displayed
        EXPECTED: **[CORAL]**:
        EXPECTED: * Quick links are displayed as 6 separate blocks
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * Quick links that don't fit the width of the screen are cut off
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as fixed vertical list
        EXPECTED: * Quick links are stretched to fit the width of the screen
        """
        for item in range(0, self.cms_number_of_quick_links):
            self.verify_quick_link_displayed(name=self.quick_link_names[item])

    def test_012_click_on_one_of_configured_quick_links_and_verify_redirection(self):
        """
        DESCRIPTION: Click anywhere  on one of the newly configured quick links
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')

        item = random.randint(0, self.cms_number_of_quick_links - 1)
        quick_link = quick_links.get(self.quick_link_names[item])
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_names[item]}" not found')

        quick_link.click()
        self.verify_redirection_from_quick_link()
