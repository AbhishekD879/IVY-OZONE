import pytest
import voltron.environments.constants as vec
import time
import tests
from datetime import datetime
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581909_User_with_wrong_segment_which_is_other_than_CSP_for_QL_and_Featured_Module(BaseFeaturedTest):
    """
    TR_ID: C65581909
    NAME: User with wrong segment which is other than CSP_ for QL and Featured Module
    DESCRIPTION: This test case verifies segment name
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > QL/Featured Module
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL.
    """
    keep_browser_open = True
    destination_url = f'https://{tests.HOSTNAME}//sport/football/matches'
    homepage_id = {'homepage': 0}
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    Wrong_segment = vec.bma.UNIVERSAL_SEGMENT

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > QL/Featured Module
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_title = 'Autotest_' + 'C65581909'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from,
                                          universalSegment=False,
                                          inclusionList=[self.segment])
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                             id=eventID,
                                                                             universalSegment=False,
                                                                             inclusionList=[self.segment],
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10
                                                                             )['title'].upper()

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        # Covered in preconditions

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # Covered in preconditions

    def test_003_click_on_QL_Featured_Module_link(self):
        """
        DESCRIPTION: Click on QL/Featured Module link.
        EXPECTED: User should be able to view existing super buttons
        """
        # Covered in preconditions

    def test_004_create_a_segmented_QL_Featured_Module_with_csp__excsp_1_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented QL/Featured Module with CSP_ (Ex:CSP_1) segment name and Login with Segmented user Verify in FE
        EXPECTED: User should able to view segmented QL/Featured Module
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_005_create_a_segmented_QL_Featured_Module_otherthan_csp__exsegment_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented QL/Featured Module otherthan CSP_ (ex:Segment )segment name and Login with Segmented user Verify in FE
        EXPECTED: If user should belongs to wrong segment (without CSP_) Universal view should be displayed.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.Wrong_segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        quick_link_presence = self.site.home.has_quick_link_section()
        if quick_link_presence:
            self._logger.info(msg='Quicklinks are present')
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            quick_link = quick_links.get(self.quick_link_title)
            self.assertFalse(quick_link, msg=f'Quick link "{self.quick_link_title}" is found')
        else:
            self._logger.info(msg='Quicklinks not present')
        result = self.wait_for_featured_module(name=self.module_name, expected_result=False, timeout=20)
        self.assertFalse(result, msg=f"Featured module {self.module_name} is present for segmented user")

    def test_006_repeat_same_steps_for_all_the_modules(self):
        """
        DESCRIPTION: Repeat same steps for all the modules
        EXPECTED: Universal view should displayed for wrong segmented name
        """
        # Covered in above steps
