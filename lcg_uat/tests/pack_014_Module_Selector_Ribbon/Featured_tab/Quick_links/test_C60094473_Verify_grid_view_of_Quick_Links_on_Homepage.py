import tests
import pytest
import time
from datetime import datetime
from faker import Faker
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create quick links on prod
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C60094473_Verify_grid_view_of_Quick_Links_on_Homepage(BaseFeaturedTest):
    """
    TR_ID: C60094473
    NAME: Verify grid view of Quick Links on Homepage
    DESCRIPTION: This test case verifies grid view of Quick links to Homepage
    DESCRIPTION: **VALID AFTER BMA-57288**
    PRECONDITIONS: 1) There should be **2** active Quick links for Homepage in CMS
    PRECONDITIONS: 2) Go to Oxygen app and navigate to Homepage.
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

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
        cms_number_of_quick_links = int(sport_quick_links['maxAmount'])
        self.__class__.quick_link_names = ['Autotest ' + Faker().city() for _ in range(0, cms_number_of_quick_links)]

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.date_from = self.get_current_time()
        self.__class__.quick_link_object_0 = self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                                                               sport_id=self.homepage_id.get('homepage'),
                                                                               destination=self.destination_url,
                                                                               date_from=self.date_from)
        self.__class__.quick_link_object_1 = self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                                                               sport_id=self.homepage_id.get('homepage'),
                                                                               destination=self.destination_url,
                                                                               date_from=self.date_from)
        self.navigate_to_homepage_featured_tab()

    def test_001__go_to_oxygen_application_and_navigate_to_featured_tab_verify_that_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: * Go to Oxygen application and navigate to Featured tab.
        DESCRIPTION: * Verify that configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick links are displayed on Featured tab on Homepage.
        EXPECTED: * Quick links are shown in grid (in the same line, divided in half)
        EXPECTED: ![](index.php?/attachments/get/122312546)
        """
        self.wait_for_quick_link(name=self.quick_link_names[0])
        self.verify_quick_link_displayed(name=self.quick_link_names[0])
        self.wait_for_quick_link(name=self.quick_link_names[1])
        self.verify_quick_link_displayed(name=self.quick_link_names[1])

    def test_002__configure_one_more_active_quick_link_in_cms_to_have_3_active_links_verify_that_configured_quick_links_are_displayed_on_featured(self):
        """
        DESCRIPTION: * Configure one more active quick link in CMS (to have 3 active links)
        DESCRIPTION: * Verify that configured Quick links are displayed on Featured
        EXPECTED: If there are odd number of Quick Links (1,3,5 etc.) in Grid view:
        EXPECTED: * First Quick link is stretched to fit the width of the screen
        EXPECTED: * Other Quick links are displayed in grid view
        EXPECTED: ![](index.php?/attachments/get/122312547)
        """
        self.__class__.quick_link_object_2 = self.cms_config.create_quick_link(title=self.quick_link_names[2],
                                                                               sport_id=self.homepage_id.get('homepage'),
                                                                               destination=self.destination_url,
                                                                               date_from=self.date_from)
        self.navigate_to_homepage_featured_tab()
        self.wait_for_quick_link(name=self.quick_link_names[2])
        self.verify_quick_link_displayed(name=self.quick_link_names[2])

    def test_003__configure_more_active_quick_link_in_cms_to_have_even_number_of_active_links_eg_468_etc_verify_that_configured_quick_links_are_displayed_on_featured(self):
        """
        DESCRIPTION: * Configure more active quick link in CMS to have even number of active links (e.g 4,6,8 etc.)
        DESCRIPTION: * Verify that configured Quick links are displayed on Featured
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick links are displayed on Featured tab on Homepage.
        EXPECTED: * Quick links are shown in grid (2 links in the same line, divided in halves)
        EXPECTED: ![](index.php?/attachments/get/122312549)
        """
        # this step is covered into step 2

    def test_004__remove_all_active_quick_links_except_one_in_cms_to_have_1_active_quick_link_verify_that_configured_quick_link_is_displayed_on_featured(self):
        """
        DESCRIPTION: * Remove all active quick links except one in CMS to have **1** active quick link
        DESCRIPTION: * Verify that configured Quick link is displayed on Featured
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Quick link is stretched to fit the width of the screen
        EXPECTED: ![](index.php?/attachments/get/122312553)
        """
        quick_link_id_1 = self.quick_link_object_1.get('id')
        self.cms_config.delete_quick_link(quick_link_id=quick_link_id_1)
        self.cms_config._created_quick_links.remove(quick_link_id_1)
        quick_link_id_2 = self.quick_link_object_2.get('id')
        self.cms_config.delete_quick_link(quick_link_id=quick_link_id_2)
        self.cms_config._created_quick_links.remove(quick_link_id_2)

        self.site.wait_splash_to_hide(timeout=40)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.wait_for_quick_link(name=self.quick_link_names[1], expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_names[1], expected_result=False)
        self.wait_for_quick_link(name=self.quick_link_names[2], expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_names[2], expected_result=False)
