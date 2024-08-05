import time
from datetime import datetime
from time import sleep

import pytest
from faker import Faker

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.prod # we can not create quick links on prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.featured
@pytest.mark.medium
@vtest
class Test_C2552882_Verify_adding_removing_Quick_links_on_any_Sports_Landing_page(BaseFeaturedTest):
    """
    TR_ID: C2552882
    VOL_ID: C9698724
    NAME: Verify adding/removing Quick links on any Sports Landing page
    DESCRIPTION: This test case verifies adding of Quick links to Homepage and All Sports Landing pages
    PRECONDITIONS: 1. <Sport name1>, <Sport name2> - Select any two Sport types(e.g. Football and Tennis)
    PRECONDITIONS: 2. There should be no active Quick links enabled for <Sport name1>, <Sport name2> landing pages
    PRECONDITIONS: 3. Go to Oxygen app and navigate to <Sport name1> landing page
    PRECONDITIONS: [Tab name] - This tab is selected by default after accessing Sport Landing Page
    PRECONDITIONS: Name of the tab depends on the selected Sport
    PRECONDITIONS: Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name1>, <Sport name2> - any sport with following tabs: "Matches", "Events", "Fights" available
    """
    keep_browser_open = True
    homepage_id = {'homepage': 0}
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
        DESCRIPTION: Quick links module is enabled in CMS
        DESCRIPTION: Go to CMS > Sport Pages > Homepage > Quick Links and configure one Quick Link for Homepage
        DESCRIPTION: There should be no active Quick links enabled for <Sport name1>, <Sport name2> landing pages
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_home = self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                                                           sport_id=self.homepage_id.get('homepage'))

        self.__class__.football_page_id = {'football': self.ob_config.backend.ti.football.category_id}
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.football_page_id.get('football')):
            raise CmsClientException('"Quick links" module is disabled for football')

        self.__class__.tennis_page_id = {'tennis': self.ob_config.backend.ti.tennis.category_id}
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.tennis_page_id.get('tennis')):
            raise CmsClientException('"Quick links" module is disabled for tennis')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_001_verify_displaying_of_quick_links_on_sport_name1_landing_page(self):
        """
        DESCRIPTION: Verify displaying of Quick links on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * No Quick Links are displayed on <Sport name1> landing page
        """
        selected_tab = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(selected_tab, expected_tab_name,
                         msg=f'Selected tab is: "{selected_tab}" instead of: "{expected_tab_name}"')
        self.wait_for_quick_link(name=self.quick_link_names[0], delimiter='42/16,', expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_names[0], expected_result=False, page_name='football')

    def test_002_in_cms_sport_pages_sport_name1_configure_one_quick_link_for_sport_name1(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > <Sport name1> > Quick Links
        DESCRIPTION: Configure one Quick Link for <Sport name1> landing page
        """
        date_from = self.get_current_time()
        self.__class__.quick_link_sport_1 = self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                                                              sport_id=self.football_page_id.get('football'), date_from=date_from)
        sleep(10)  # wait for changes from CMS to be available for Featured MS

    def test_003_on_sport_name1_verify_that_configured_quick_link_is_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application and navigate to <Sport name1> landing page
        DESCRIPTION: Verify that configured Quick link is displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Configured Quick link is displayed on [Tab name] of <Sport name1> landing page
        """
        self.wait_for_quick_link(name=self.quick_link_names[1], delimiter='42/16,')
        self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='football')

    def test_004_in_cms_sport_pages_sport_name2_create_new_quick_link_for_sport_name2(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > <Sport name2> > Quick Links
        DESCRIPTION: Create new Quick link for <Sport name2> landing page
        """
        date_from = self.get_current_time()
        self.__class__.quick_link_sport_2 = self.cms_config.create_quick_link(title=self.quick_link_names[2],
                                                                              sport_id=self.tennis_page_id.get('tennis'), date_from=date_from)
        sleep(10)  # wait for changes from CMS to be available for Featured MS

    def test_005_on_sport_name2_verify_that_quick_link_configured_for_sport_name1_is_not_displayed(self):
        """
        DESCRIPTION: Go to <Sport name2> landing page in oxygen application
        DESCRIPTION: Verify that quick link configured for <Sport name1> landing page is not displayed on <Sport name2> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Configured Quick link for <Sport name2> landing page is displayed on [Tab name] of <Sport name2> landing page
        EXPECTED: * Quick links configured for <Sport name1> landing page is not displayed on [Tab name] of <Sport name2> landing page
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name='tennis')

        selected_tab = self.site.tennis.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.tennis_config.category_id)
        self.assertEqual(selected_tab, expected_tab_name,
                         msg=f'Selected tab is: "{selected_tab}" instead of: "{expected_tab_name}"')

        self.wait_for_quick_link(name=self.quick_link_names[2], delimiter='42/34,')
        self.verify_quick_link_displayed(name=self.quick_link_names[2], page_name='tennis')
        self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='tennis', expected_result=False)

    def test_006_on_home_page_verify_that_quick_links_configured_for_sport_name2_and_sport_name1_are_not_displayed(self):
        """
        DESCRIPTION: Go to Home page
        DESCRIPTION: Verify that quick links configured for <Sport name2> and <Sport name1> landing pages are not displayed on Homepage
        EXPECTED: * Quick links configured for <Sport name2> and <Sport name1> landing pages are not displayed on Homepage
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Home')

        self.verify_quick_link_displayed(name=self.quick_link_names[1],
                                         expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_names[2],
                                         expected_result=False)

    def test_007_in_cms_sport_pages_sport_name1_set_active_inactive_flag_in_configured_quick_link_to_inactive(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > <Sport name1> > Quick Links and
        DESCRIPTION: Set "Active/Inactive" flag in configured quick link to 'Inactive'
        """
        self.cms_config.change_quick_link_state(quick_link_object=self.quick_link_sport_1,
                                                active=False)

    def test_008_in_oxygen_navigate_to_sport_name1_and_verify_that_quick_link_is_no_longer_displayed_on_sport_name1(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page
        DESCRIPTION: Verify that Quick link is no longer displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick link is no longer displayed on on [Tab name] of <Sport name1> landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

        selected_tab = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(selected_tab, expected_tab_name,
                         msg=f'Selected tab is: "{selected_tab}" instead of: "{expected_tab_name}"')

        self.wait_for_quick_link(name=self.quick_link_names[1], expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_names[1],
                                         expected_result=False,
                                         page_name='football')

    def test_009_in_cms_sport_pages_sport_name1_set_active_inactive_flag_in_configured_quick_link_for_homepage_to_active(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > <Sport name1> > Quick Links
        DESCRIPTION: Set "Active/Inactive" flag in configured quick link for Homepage to 'Active'
        """
        self.cms_config.change_quick_link_state(quick_link_object=self.quick_link_sport_1,
                                                active=True)
        sleep(20)  # wait for changes from CMS to be available for Featured MS

    def test_010_in_oxygen_navigate_to_sport_name1_and_verify_that_quick_link_is_displayed_on_sport_name1(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page
        DESCRIPTION: Verify that Quick link is displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Configured Quick link is displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Quick link is stretched to fit the width of the screen
        """
        self.wait_for_quick_link(name=self.quick_link_names[1], delimiter='42/16,')
        self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='football')

    def test_011_in_cms_sport_pages_sport_name1_delete_previously_created_quick_link_for_sport_name1(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > <Sport name1> > Quick Links
        DESCRIPTION: Delete previously created Quick link for <Sport name1> landing page
        """
        quick_link_id = self.quick_link_sport_1.get('id')
        self.cms_config.delete_quick_link(quick_link_id=quick_link_id)
        self.cms_config._created_quick_links.remove(quick_link_id)

    def test_012_in_oxygen_navigate_to_sport_name1_and_verify_that_quick_link_is_no_longer_displayed_on_sport_name1(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page
        DESCRIPTION: Verify that Quick link is no longer displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick link is no longer displayed on [Tab name] of <Sport name1> landing page
        """
        selected_tab = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(selected_tab, expected_tab_name,
                         msg=f'Selected tab is: "{selected_tab}" instead of: "{expected_tab_name}"')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.wait_for_quick_link(name=self.quick_link_names[1], expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_names[1], expected_result=False, page_name='football')
