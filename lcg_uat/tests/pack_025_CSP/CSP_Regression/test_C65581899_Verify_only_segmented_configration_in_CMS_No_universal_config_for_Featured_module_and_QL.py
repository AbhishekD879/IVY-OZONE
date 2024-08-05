import pytest
import time
import tests
from datetime import datetime
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65581899_Verify_only_segmented_configration_in_CMS_No_universal_config_for_Featured_module_and_QL(BaseFeaturedTest):
    """
    TR_ID: C65581899
    NAME: This test case verifies only segmented configration in CMS (No universal config) for Featured module and QL.
    DESCRIPTION: This test case verifies only segmented configration in CMS (No universal config) for Featured module and QL.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Featured module/QL
    PRECONDITIONS: Create atleast a record in each module for segment
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    destination_url = f'https://{tests.HOSTNAME}//sport/football/matches'
    homepage_id = {'homepage': 0}

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
        PRECONDITIONS: CMS > sports pages > Featured module/QL
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
        self.__class__.quick_link_title = 'Autotest_' + '2C65581899'
        quick_link_title1 = 'Autotest_' + '1C65581899'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from,
                                          universalSegment=False,
                                          inclusionList=[self.segment])
        self.cms_config.create_quick_link(title=quick_link_title1,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from)
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                             id=eventID,
                                                                             universalSegment=False,
                                                                             inclusionList=[self.segment],
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10
                                                                             )['title'].upper()

    def test_001_launch_coral_and_lads_appmobile_web(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web
        EXPECTED: Homepage should load as per CMS config
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_universal_view_observe__surface_bet_and_HC_as_per_pre_conditions(self):
        """
        DESCRIPTION: verify universal view ,observe all modules(as per pre conditions)
        EXPECTED: No data (records) should be displayed for surface bet and HC as there is no universal configuration
        """
        featured_tab = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertFalse(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name, expected_result=False)
        self.assertFalse(module, msg=f'"{self.module_name}" module is found')

    def test_003_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Homepage should load as per CMS segment config.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_004_verify_homepage(self):
        """
        DESCRIPTION: Verify homepage
        EXPECTED: Segmented records for surface bet and HC should display as per CMS configurations
        """
        featured_tab = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
