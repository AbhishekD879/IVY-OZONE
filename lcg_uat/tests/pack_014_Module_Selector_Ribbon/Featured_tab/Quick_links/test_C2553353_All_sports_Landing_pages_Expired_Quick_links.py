import time
from datetime import datetime
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
@pytest.mark.mobile_only
@pytest.mark.featured
@pytest.mark.medium
@vtest
class Test_C2553353_All_sports_Landing_pages_Expired_Quick_links(BaseFeaturedTest):
    """
    TR_ID: C2553353
    VOL_ID: C9698711
    NAME: All sports Landing pages: Expired Quick links
    DESCRIPTION: This test case verifies Expired Quick links on All sports Landing pages
    PRECONDITIONS: 1. Go to CMS -> Sport Pages-><Sport name>-> Quick Links and configure a Quick link for <Sport name> landing page with Validity period End Date=current time +10 minutes. - (<Quick Link1>)
    PRECONDITIONS: 2. There should be no other active Quick links for selected <Sport name> landing page expect <Quick Link1>.
    PRECONDITIONS: 3. Go to Oxygen app and navigate to <Sport name> landing page.
    PRECONDITIONS: [Tab name]- This tab is selected by default after accessing Sport Landing Page. Name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True
    quick_link_name = 'auto ' + Faker().city()
    quick_link_name2 = 'auto2 ' + Faker().city()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Quick links module is enabled in CMS
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and configure one Quick Link for Homepage
        DESCRIPTION: Quick Links and configure a Quick link for Homepage with Validity period End Date=current time +1 minute. - (<Quick Link1>)
        """
        self.__class__.sport_id = {'basketball': self.ob_config.backend.ti.basketball.category_id}
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('basketball')):
            raise CmsClientException('"Quick links" module is disabled for basketball')
        hours_delta = 0 if tests.location in tests.settings.utc_locations else time.timezone // (60 * 60)  # it will set for local time -2/-3 depends on the current GMT difference - winter/summer time
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_to = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                      hours=hours_delta, minutes=1)[:-3] + 'Z'
        self.__class__.quick_link_object = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                             sport_id=self.sport_id.get('basketball'),
                                                                             date_to=date_to)

    def test_001_go_to_oxygen_app_sport_name_landing_page__tab_name_and_verify_that_configured_quick_link1_is_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that configured <Quick Link1> is displayed on <Sport name> landing page.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * <Quick Link1> is displayed.
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        self.wait_for_quick_link(name=self.quick_link_name, delimiter='42/6,')
        self.verify_quick_link_displayed(name=self.quick_link_name, page_name='basketball')

    def test_002_go_to_cms_sport_pages_sport_name_quick_links_and_create_the_second_active_quick_link_with_validity_period_end_datecurrent_time_plus20_minutes_quick_link2(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name>-> Quick Links  and create the second active Quick link with Validity period End Date=current time +20 minutes. (<Quick Link2>)
        """
        hours_delta = 0 if tests.location in tests.settings.utc_locations else time.timezone // (60 * 60)  # it will set for local time -2/-3 depends on the current GMT difference - winter/summer time
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_to = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                      hours=hours_delta, minutes=2, seconds=30)[:-3] + 'Z'
        self.__class__.quick_link_object2 = self.cms_config.create_quick_link(title=self.quick_link_name2,
                                                                              sport_id=self.sport_id.get('basketball'),
                                                                              date_to=date_to
                                                                              )
        sleep(10)  # wait for changes from CMS to be available for Featured MS

    def test_003_go_to_oxygen_app_sport_name_landing_page_tab_name_and_verify_that_configured_quick_links_are_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that configured Quick links are displayed on <Sport name> landing page.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick Links are displayed.
        """
        self.wait_for_quick_link(name=self.quick_link_name2, delimiter='42/6,')
        self.verify_quick_link_displayed(name=self.quick_link_name2, page_name='basketball')

    def test_004_wait_for_quick_link_from_step_2_to_get_expired_in_1_minute(self):
        """
        DESCRIPTION: Wait for Quick link from Step 2 to get expired (in 1 minute)
        """
        self._logger.info(f'*** Waiting for 60 seconds to get expired Quick Link with name "{self.quick_link_name2}"')
        sleep(60)

    def test_005_go_to_oxygen_app__sport_name_landing_page__tab_name_and_verify_that_quick_link1_is_not_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that <Quick Link1> is not displayed on <Sport name> landing page.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * <Quick Link1> is not displayed.
        EXPECTED: * <Quick Link2> is displayed
        """
        self.wait_for_quick_link(name=self.quick_link_name, expected_result=False, delimiter='42/6,')
        self.verify_quick_link_displayed(name=self.quick_link_name, expected_result=False, page_name='basketball')

        self.wait_for_quick_link(name=self.quick_link_name2, delimiter='42/6,')
        self.verify_quick_link_displayed(name=self.quick_link_name2, page_name='basketball')

    def test_006_wait_for_quick_link1_to_get_expired_in_2_minutes(self):
        """
        DESCRIPTION: Wait for <Quick Link1> to get expired (in 60 seconds, is sum of 2 minutes)
        """
        self._logger.info(f'*** Waiting for 60 seconds to get expired Quick Link with name "{self.quick_link_name2}"')
        sleep(60)

    def test_007_go_to_oxygen_app_sport_name_landing_page__tab_name_and_verify_that_quick_link2_is_not_displayed_on_homepage(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that <Quick Link2> is not displayed on Homepage
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * No Quick links are displayed.
        """
        self.wait_for_quick_link(name=self.quick_link_name, expected_result=False, delimiter='42/6,')
        self.verify_quick_link_displayed(name=self.quick_link_name, expected_result=False, page_name='basketball')
        self.wait_for_quick_link(name=self.quick_link_name2, expected_result=False, delimiter='42/6,')
        self.verify_quick_link_displayed(name=self.quick_link_name2, expected_result=False, page_name='basketball')
