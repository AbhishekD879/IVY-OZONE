import pytest
from datetime import datetime
from time import sleep
from faker import Faker
from tzlocal import get_localzone
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.prod # we can not create quick links on prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.module_ribbon
@pytest.mark.cms
@pytest.mark.quick_links
@pytest.mark.featured
@pytest.mark.mobile_only
@pytest.mark.medium
@vtest
class Test_C2553321_Homepage_Expired_Quick_links(BaseFeaturedTest):
    """
    TR_ID: C2553321
    VOL_ID: C9698700
    NAME: Homepage: Expired Quick links
    DESCRIPTION: This test case verifies expiration of Quick links on homepage
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Homepage -> Quick Links and configure a Quick link for Homepage with Validity period End Date=current time +10 minutes. - (<Quick Link1>)
    PRECONDITIONS: 2. There should be no other active Quick links for Homepage expect <Quick Link1>.
    PRECONDITIONS: 3. Go to Oxygen app and navigate to Homepage Featured tab.
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True
    sport_id = {'homepage': 0}
    quick_link_name = 'auto expired ' + Faker().city()
    quick_link_name2 = 'auto expired2 ' + Faker().city()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Quick links module is enabled in CMS
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and configure one Quick Link for Homepage
        DESCRIPTION: Quick Links and configure a Quick link for Homepage with Validity period End Date=current time +1 minute. - (<Quick Link1>)
        """
        # Note: if timezone in jenkins changed from UTC use the commented code
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        # if tests.location in 'Mac_Mini_GRID':
        #     hours_delta = 0
        # else:
        hours_delta = 0
        # is_dst = time.localtime().tm_isdst
        # hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                        hours=hours_delta, minutes=-1)[:-3] + 'Z'
        date_to = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                      hours=hours_delta, minutes=2)[:-3] + 'Z'
        self._logger.info(f'Sending date to "{date_to}"')
        timezone = str(get_localzone())
        self._logger.info(f'Sending time zone "{timezone}"')
        self.__class__.quick_link_object = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                             sport_id=self.sport_id.get('homepage'),
                                                                             date_from=date_from,
                                                                             date_to=date_to)

    def test_001_verify_displaying_if_configured_quick_link_is_displayed_on_homepage_featured_tab(self):
        """
        DESCRIPTION: Verify displaying if configured Quick link is displayed on Homepage Featured tab.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed.
        """
        selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(selected_tab, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                         msg=f'Selected tab is "{selected_tab}" instead of "{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}" tab')
        self.wait_for_quick_link(name=self.quick_link_name)
        self.verify_quick_link_displayed(name=self.quick_link_name)

    def test_002_go_to_cms_sport_pages_homepage_quick_links_and_create_the_second_active_quick_link_with_validity_period_end_datecurrent_time_plus_2_minute_quick_link2(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and create the second active Quick link with Validity period End Date=current time +2 minute. (<Quick Link2>)
        """
        # if tests.location in tests.settings.utc_locations:
        #     hours_delta = 0
        # else:
        hours_delta = 0
        # is_dst = time.localtime().tm_isdst
        # hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                        hours=hours_delta, minutes=-1)[:-3] + 'Z'
        date_to = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                      hours=hours_delta, minutes=3)[:-3] + 'Z'
        self.__class__.quick_link_object2 = self.cms_config.create_quick_link(title=self.quick_link_name2,
                                                                              sport_id=self.sport_id.get('homepage'),
                                                                              date_from=date_from,
                                                                              date_to=date_to)

    def test_003_go_to_oxygen_app_and_navigate_to_homepage_featured_tab_verify_that_configured_quick_links_are_displayed_on_homepage(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Homepage Featured tab.
        DESCRIPTION: Verify that configured Quick links are displayed on Homepage.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick Links are displayed.
        """
        selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(selected_tab, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                         msg=f'Selected tab is "{selected_tab}" instead of "{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}" tab')
        self.wait_for_quick_link(name=self.quick_link_name2)
        self.verify_quick_link_displayed(name=self.quick_link_name2)

    def test_004_wait_for_quick_link1_to_get_expired_in_1_minute(self):
        """
        DESCRIPTION: Wait for<Quick Link1> to get expired (in 1 minute)
        """
        self._logger.info(f'*** Waiting for 60 seconds to get expired Quick Link with name "{self.quick_link_name}"')
        sleep(60)

    def test_005_go_to_oxygen_app_and_navigate_to_homepage_featured_tabverify_that_configured_quick_link1_is_not_displayed_on_homepage(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Homepage Featured tab.
        DESCRIPTION: Verify that configured <Quick Link1> is not displayed on Homepage.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * <Quick Link1> is not displayed.
        EXPECTED: * <Quick Link2> is displayed
        """
        self.wait_for_quick_link(name=self.quick_link_name, expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_name, expected_result=False)
        self.wait_for_quick_link(name=self.quick_link_name2)
        self.verify_quick_link_displayed(name=self.quick_link_name2)

    def test_006_wait_for_quick_link2_to_get_expired_in_2_minutes(self):
        """
        DESCRIPTION: Wait for <Quick Link2> to get expired (in 2 minutes)
        """
        self._logger.info(f'*** Waiting for 60 seconds to get expired Quick Link with name "{self.quick_link_name2}"')
        sleep(60)

    def test_007_go_to_oxygen_app_and_navigate_to_homepage_featured_tabverify_that_configured_quick_link2_is_not_displayed_on_homepage(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Homepage Featured tab.
        DESCRIPTION: Verify that configured <Quick Link2> is not displayed on Homepage
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * No Quick links are displayed.
        """
        self.wait_for_quick_link(name=self.quick_link_name2, expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_name2, expected_result=False)
