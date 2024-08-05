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
class Test_C60094474_Verify_grid_view_of_Quick_Links_on_Sports_Landing_Page(BaseFeaturedTest):
    """
    TR_ID: C60094474
    NAME: Verify grid view of Quick Links on Sports Landing Page
    DESCRIPTION: This test case verifies grid view of Quick links to Sports Landing Page
    DESCRIPTION: **VALID AFTER BMA-57288**
    PRECONDITIONS: 1) There should be **2** active Quick links for any Sport Landing Page in CMS
    PRECONDITIONS: 2) Go to Oxygen app and navigate to Homepage.
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True
    quick_link_names = ['Autotest ' + Faker().city() for _ in range(0, 3)]

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Go to CMS and configure active Quick link for current Time period for any <Sport name> landing page
        PRECONDITIONS: 2. Load oxygen application and navigate to first <Sport name> landing page.
        PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
        PRECONDITIONS: Design for Coral(now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
        PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
        PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
        PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')

        self.__class__.football_page_id = {'football': self.ob_config.backend.ti.football.category_id}
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.football_page_id.get('football')):
            raise CmsClientException('"Quick links" module is disabled for football')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        date_from = self.get_current_time()
        self.__class__.date_from = self.get_current_time()
        self.__class__.quick_link_object_0 = self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                                                               sport_id=self.football_page_id.get('football'),
                                                                               date_from=date_from)
        self.__class__.quick_link_object_1 = self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                                                               sport_id=self.football_page_id.get('football'),
                                                                               date_from=date_from)

    def test_001__go_to_oxygen_application_and_navigate_to_sport_landing_page_with_configured_quick_links_from_preconditions_verify_that_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: * Go to Oxygen application and navigate to Sport Landing page with configured Quick Links from Preconditions
        DESCRIPTION: * Verify that configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick links are displayed on Featured tab on Homepage.
        EXPECTED: * Quick links are shown in grid (in the same line, divided in half)
        EXPECTED: ![](index.php?/attachments/get/122312550)
        """
        # Quick links are shown in grid (in the same line, divided in half) can not automated
        self.wait_for_quick_link(name=self.quick_link_names[0], delimiter='42/16,')
        self.verify_quick_link_displayed(name=self.quick_link_names[0], page_name='football')
        self.wait_for_quick_link(name=self.quick_link_names[1], delimiter='42/16,')
        self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='football')

    def test_002__configure_one_more_active_quick_link_in_cms_to_have_3_active_links_verify_that_configured_quick_links_are_displayed_on_sport_landing_page(self):
        """
        DESCRIPTION: * Configure one more active quick link in CMS (to have 3 active links)
        DESCRIPTION: * Verify that configured Quick links are displayed on Sport Landing page
        EXPECTED: If there are odd number of Quick Links (1,3,5 etc.) in Grid view:
        EXPECTED: * First Quick link is stretched to fit the width of the screen
        EXPECTED: * Other Quick links are displayed in grid view
        EXPECTED: ![](index.php?/attachments/get/122312551)
        """
        self.__class__.quick_link_object_2 = self.cms_config.create_quick_link(title=self.quick_link_names[2],
                                                                               sport_id=self.football_page_id.get('football'),
                                                                               date_from=self.date_from)
        self.wait_for_quick_link(name=self.quick_link_names[2], delimiter='42/16,')
        self.verify_quick_link_displayed(name=self.quick_link_names[2], page_name='football')

    def test_003__configure_more_active_quick_link_in_cms_to_have_even_number_of_active_links_eg_468_etc_verify_that_configured_quick_links_are_displayed_on_sport_landing_page(self):
        """
        DESCRIPTION: * Configure more active quick link in CMS to have even number of active links (e.g 4,6,8 etc.)
        DESCRIPTION: * Verify that configured Quick links are displayed on Sport Landing page
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick links are displayed on Sport Landing page
        EXPECTED: * Quick links are shown in grid (2 links in the same line, divided in halves)
        EXPECTED: ![](index.php?/attachments/get/122312552)
        """
        # this step is covered into step 2

    def test_004__remove_all_active_quick_links_except_one_in_cms_to_have_1_active_quick_link_verify_that_configured_quick_link_is_displayed_on_sport_landing_page(self):
        """
        DESCRIPTION: * Remove all active quick links except one in CMS to have **1** active quick link
        DESCRIPTION: * Verify that configured Quick link is displayed on Sport Landing page
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Quick link is stretched to fit the width of the screen
        EXPECTED: ![](index.php?/attachments/get/122312554)
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
