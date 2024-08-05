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
@pytest.mark.cms
@pytest.mark.quick_links
@pytest.mark.featured
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.tennis
@vtest
class Test_C2552889_Verify_displaying_of_Quick_Links_on_any_Sports_Landing_page(BaseFeaturedTest):
    """
    TR_ID: C2552889
    VOL_ID: C9698733
    NAME: Verify displaying of Quick Links on any Sports Landing page
    DESCRIPTION: This test case verifies displaying of Quick Links on All Sports landing pages
    PRECONDITIONS: 1. Go to CMS -> Sport Pages-><Sport name> -> Quick Links  and configure 1 active Quick link for <Sport name> landing page
    PRECONDITIONS: 2. Load oxygen application and navigate to <Sport name> landing page
    PRECONDITIONS: [Tab name]- This tab is selected by default aftec accessing Sport Landing Page. Name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True
    quick_link_name = 'auto ' + Faker().city()
    quick_link_name2 = 'auto ' + Faker().city()
    quick_link_name3 = 'auto tennis3 with very very long long long'
    sport_id = None
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    fake_name = 'autotest ' + Faker().city()
    quick_link_objects = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Quick links module is enabled in CMS
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and configure one Quick Link for Homepage
        """
        self.__class__.sport_id = {'tennis': self.ob_config.backend.ti.tennis.category_id}
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('tennis')):
            raise CmsClientException('"Quick links" module is disabled for tennis')

        self.__class__.quick_link_object = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                             sport_id=self.sport_id.get('tennis'),
                                                                             destination=self.destination_url
                                                                             )
        self.quick_link_objects.append(self.quick_link_object)

    def test_001_navigate_to_sport_name_landing_page_and_verify_that_configured_quick_link_is_displayed(self):
        """
        DESCRIPTION: Navigate to <Sport name> landing page and verify that configured Quick link is displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick link is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        self.wait_for_quick_link(name=self.quick_link_name, delimiter='42/34,')
        self.verify_quick_link_displayed(name=self.quick_link_name, page_name='tennis')

    def test_002_click_anywhere_on_the_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.tennis.tab_content.quick_links.items_as_ordered_dict
        self.assertIn(self.quick_link_name, quick_links,
                      msg=f'Can not find "{self.quick_link_name}" in "{quick_links}"')
        quick_links.get(self.quick_link_name).click()
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url "{current_url}" is not equal to expected "{self.destination_url}"')

    def test_003_go_to_cms_sport_pages_sport_name_quick_links_and_configure_2nd_quick_link_for_the_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name> -> Quick Links and configure 2nd Quick link for the <Sport name> landing page
        """
        self.__class__.quick_link_object2 = self.cms_config.create_quick_link(title=self.quick_link_name2,
                                                                              sport_id=self.sport_id.get('tennis'),
                                                                              destination=self.destination_url
                                                                              )
        self.quick_link_objects.append(self.quick_link_object2)
        sleep(10)  # wait for changes from CMS to be available for Featured MS

    def test_004_go_to_oxygen_application_sport_page_and_verify_that_2_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application <Sport Page> and verify that 2 configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick links are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**:
        EXPECTED: * Quick links are displayed in one row as 2 separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        self.wait_for_quick_link(name=self.quick_link_name2, delimiter='42/34,')
        self.verify_quick_link_displayed(name=self.quick_link_name2, page_name='tennis')

    def test_005_click_anywhere_on_the_newly_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.tennis.tab_content.quick_links.items_as_ordered_dict
        self.assertIn(self.quick_link_name2, quick_links,
                      msg=f'Can not find "{self.quick_link_name2}" in "{quick_links}"')
        quick_links.get(self.quick_link_name2).click()
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url "{current_url}" is not equal to expected "{self.destination_url}"')

    def test_006_go_to_cms_sport_pages_sport_name_quick_links_and_configure_3rd_quick_link_for_sport_name_landing_page_with_a_long_namelong_enough_in_order_not_to_fit_the_remaining_width_of_the_screen(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name> -> Quick Links and configure 3rd Quick link for <Sport name> landing page with a long name(Long enough in order not to fit the remaining width of the screen)
        """
        self.__class__.quick_link_object3 = self.cms_config.create_quick_link(title=self.quick_link_name3,
                                                                              sport_id=self.sport_id.get('tennis'),
                                                                              destination=self.destination_url
                                                                              )
        self.quick_link_objects.append(self.quick_link_object3)
        sleep(10)  # wait for changes from CMS to be available for Featured MS

    def test_007_go_to_oxygen_application_football_page_and_verify_that_3_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Football page and verify that 3 configured Quick links are displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick links are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**::
        EXPECTED: * Quick links are displayed in one row as 3 separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * 3d Quick link is cut off. Only part that can fit the remaining width of the screen is shown.
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        self.wait_for_quick_link(name=self.quick_link_name3, delimiter='42/34,')
        self.verify_quick_link_displayed(name=self.quick_link_name3, page_name='tennis')

    def test_008_click_anywhere_on_the_newly_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated  to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application.
        """
        quick_links = self.site.tennis.tab_content.quick_links.items_as_ordered_dict
        self.assertIn(self.quick_link_name3, quick_links,
                      msg=f'Can not find "{self.quick_link_name3}" in "{quick_links}"')
        quick_links.get(self.quick_link_name3).click()
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url "{current_url}" is not equal to expected "{self.destination_url}"')

    def test_009_go_to_cms_system_configuration_structure_sport_quick_links_module_set_max_number_of_quick_links_to_be_displayed_to_6(self):
        """
        DESCRIPTION: Go to CMS->System Configuration-> Structure-> Sport Quick Links module set max number of quick links to be displayed to 6.
        EXPECTED:
        """
        # Can not automate because of system config. We can get only actual max number of quick links
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        self.__class__.configured_number_of_quick_links = sport_quick_links.get('maxAmount')
        if not self.configured_number_of_quick_links:
            raise CmsClientException('Max number of quick links is not configured in CMS')

    def test_010_go_to_cms_sport_pages_sport_name_quick_links_and_configure_3_more_quick_links_in_order_to_have_6_active_quick_links_for_current_time_period(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name> -> Quick Links and configure 3 more Quick links in order to have 6 active Quick links for current Time period.
        """
        # Automated in step 11
        pass

    def test_011_go_to_oxygen_application_sport_name_landing_page_and_verify_that_6_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application <Sport name> landing page and verify that 6 configured Quick links are displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick links are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**::
        EXPECTED: * Quick links are displayed as 6 separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * Quick links that don't fit the width of the screen are cut off
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        self.__class__.quick_links = self.site.tennis.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(self.quick_links, msg='Quick links is not shown')
        quick_links_statuses = self.cms_config.get_quick_links(sport_id=self.sport_id.get('tennis'))
        enabled_quick_links = list(filter(lambda param: not param['disabled'], quick_links_statuses))

        items_to_create = int(self.configured_number_of_quick_links) - len(enabled_quick_links)
        if len(enabled_quick_links) != int(self.configured_number_of_quick_links):
            for _ in range(0, items_to_create):
                quick_link_fake_object = self.cms_config.create_quick_link(title=self.fake_name,
                                                                           sport_id=self.sport_id.get('tennis')
                                                                           )
                self.quick_link_objects.append(quick_link_fake_object)
        for quick_link_item in self.quick_link_objects:
            self.wait_for_quick_link(name=str(quick_link_item.get('title')), delimiter='42/34,')
            self.verify_quick_link_displayed(name=str(quick_link_item.get('title')), page_name='tennis')

    def test_012_click_anywhere_on_one_of_the_newly_configured_quick_linksverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on one of the newly configured quick links.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        quick_links = self.site.tennis.tab_content.quick_links.items_as_ordered_dict
        quick_links.get(self.quick_link_name3).click()
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url "{current_url}" is not equal to expected "{self.destination_url}"')
