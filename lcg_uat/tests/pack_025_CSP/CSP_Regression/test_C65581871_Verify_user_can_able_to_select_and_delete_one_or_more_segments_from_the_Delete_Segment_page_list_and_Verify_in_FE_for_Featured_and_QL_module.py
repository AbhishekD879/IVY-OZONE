import pytest
import tests
import time
from datetime import datetime
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65581871_Verify_user_can_able_to_select_and_delete_one_or_more_segments_from_the_Delete_Segment_page_list_and_Verify_in_FE_for_Featured_and_QL_module(BaseFeaturedTest):
    """
    TR_ID: C65581871
    NAME: Verify user can able to select and delete one or more segments from the 'Delete Segment' page list and Verify in FE for Featured and QL module.
    DESCRIPTION: This testcase verifies delete one or more segments from the 'Delete Segment' page list
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > delete segment page
    PRECONDITIONS: CMS > Main navigation>Surface bet/SB/Footermenu/HC/MRT/Inplay/Featured/QL/Sports ribbon
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    destination_url = f'https://{tests.HOSTNAME}//sport/football/matches'
    homepage_id = {'homepage': 0}
    segment = 'CSP_AUTO_C65581871'

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
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Featured module/QL
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
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
        self.__class__.quick_link_title = 'Autotest_' + 'C65581871'

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
        EXPECTED: User should able to login successfully
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        featured_tab = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab, timeout=10)

        self.wait_for_quick_link(name=self.quick_link_title, timeout=20)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')

    def test_002_navigate_to_delete_segments_page(self):
        """
        DESCRIPTION: Navigate to Delete segments page
        EXPECTED: Delete segment page should be opened with 'Segments list' dropdown
        """
        # covered in below step

    def test_003_verify_segments_list_dropdown(self):
        """
        DESCRIPTION: Verify Segments list dropdown
        EXPECTED: When user expand segments list ,all existing  segments should display with delete option
        """
        # can not validate CMS UI

    def test_004_select_segment_from_the_dropdown(self):
        """
        DESCRIPTION: Select segment from the dropdown
        EXPECTED: User should able to select segments with check boxes.
        """
        # can not validate CMS UI

    def test_005_select_single_segment_from_the_list(self):
        """
        DESCRIPTION: Select single segment from the list
        EXPECTED: 1. user should able to delete segment through delete icon
        EXPECTED: 2. User can able to delete selected segment from the list"
        """

        self.cms_config.delete_segment(segment_name=self.segment)
        time.sleep(5)

    def test_006_select_multiple_segments_from_the_list(self):
        """
        DESCRIPTION: Select multiple segments from the list
        EXPECTED: User should able to select and delect multiple segments from the list
        """
        # covered in above step

    def test_007_navigate_to_surfacebet_module_and_verify(self):
        """
        DESCRIPTION: Navigate to Surfacebet module and verify
        EXPECTED: 1.Deleted segment should not display in segment dropdown list
        EXPECTED: 2.Existing configuration should not display
        EXPECTED: 3.Excluded record also should not  dispaly in Universal
        """
        # can not validate CMS UI

    def test_008_navigate_to_fe_and_login_with_deleted_segmented_user(self):
        """
        DESCRIPTION: Navigate to FE and login with deleted segmented user
        EXPECTED: Universal view should display as segment is deleted
        """
        featured_tab = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab, timeout=5)
        time.sleep(5)
        self.device.refresh_page()
        module = self.wait_for_featured_module(name=self.module_name, expected_result=False, timeout=10)
        self.assertFalse(module, msg=f'"{self.module_name}" module is found')

    def test_009_Repeat_same_steps_for_QL_module(self):
        """
        EXPECTED: Universal view should displayed when delete segment user logged in
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.device.refresh_page()
        quick_link = quick_links.get(self.quick_link_title)
        self.assertNotIn(quick_link, quick_links, msg='segmented quick link is displaying')
