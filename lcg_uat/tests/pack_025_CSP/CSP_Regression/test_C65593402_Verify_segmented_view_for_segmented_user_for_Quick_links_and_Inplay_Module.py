import pytest
import tests
from faker import Faker
from crlat_cms_client.utils.date_time import get_date_time_as_string
from datetime import datetime
from voltron.environments import constants as vec
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
class Test_C65593402_Verify_segmented_view_for_segmented_user_for_Quick_links_and_Inplay_Module(BaseFeaturedTest):
    """
    TR_ID: C65593402
    NAME: Verify segmented view for segmented user for Quick links and Inplay Module.
    DESCRIPTION: This test case verifies segmented view for segmented user
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Quick links/Inplay Module
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    quick_link_name = 'Autotest ' + Faker().city()
    homepage_id = {'homepage': 0}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Quick links/Inplay Module
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-7,
                                            minutes=-1)[:-3] + 'Z'
        self.__class__.quick_link = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                      sport_id=self.homepage_id.get('homepage'),
                                                                      destination=self.destination_url,
                                                                      inclusionList=[self.segment],
                                                                      universalSegment=False,
                                                                      date_from=date_from)

    def test_001_launch_the_application_in_mobilewebapp(self):
        """
        DESCRIPTION: Launch the application in mobile(Web/App)
        EXPECTED: Application should launch successfully.
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_(self):
        """
        DESCRIPTION:
        EXPECTED: Home page should be opened.
        """
        # Covered in above step

    def test_003_login_with_specific_segmented_user__as_per_pre_conditions(self):
        """
        DESCRIPTION: Login with specific segmented user ( as per Pre-conditions)
        EXPECTED: User should login successfully
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_004_verify_segmented_record(self):
        """
        DESCRIPTION: Verify segmented record
        EXPECTED: User should able to see segmented record for specific segmented user as per CMS configuration
        """
        self.wait_for_quick_link(name=self.quick_link_name)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_name)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_name}" not found')
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertTrue(sports, msg='No inplay sports found in the module')
        self.__class__.sport = sports[-1]
        try:
            self.cms_config.update_inplay_sport_module(sport_name=self.sport.title(), universalSegment=False,
                                                       inclusionList=[self.segment])
            self.device.refresh_page()
            sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
            self.assertIn(self.sport, sports, msg=f'Segmented record {self.sport} is not displayed among {sports}')
        finally:
            self.get_cms_config().update_inplay_sport_module(segment_name=self.segment, sport_name=self.sport.title(),
                                                             universalSegment=True)
