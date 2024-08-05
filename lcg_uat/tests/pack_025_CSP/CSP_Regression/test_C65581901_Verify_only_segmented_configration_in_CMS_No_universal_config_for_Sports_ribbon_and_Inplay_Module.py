import pytest
import voltron.environments.constants as vec
from faker import Faker
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65581901_Verify_only_segmented_configration_in_CMS_No_universal_config_for_Sports_ribbon_and_Inplay_Module(Common):
    """
    TR_ID: C65581901
    NAME: This test case verifies only segmented configration in CMS (No universal config) for Sports ribbon and Inplay Module.
    DESCRIPTION: This test case verifies only segmented configration in CMS (No universal config) for Sports ribbon and Inplay Module.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>F
    PRECONDITIONS: CMS > sports pages > for Sports ribbon/Inplay Module.
    PRECONDITIONS: Create atleast a record in each module for segment
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    fake = Faker()
    title = vec.olympics.WRESTLING

    @retry(stop=stop_after_attempt(4),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def verify_sport_category_UI(self, sport=True):
        """
        To verify create sport category used this method
        """
        title = self.title if self.site.brand == 'ladbrokes' else self.title.upper()
        sports = self.site.home.menu_carousel.items_as_ordered_dict
        if sport:
            self.assertTrue(sports.get(title),
                            msg=f'Created sport category "{self.title.upper()}" is not appearing, actual categories "{sports}"')
        else:
            self.assertFalse(sports.get(title),
                             msg=f'Created sport category "{self.title.upper()}" is appearing, actual categories "{sports}"')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Sports ribbon/Inplay Module
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == self.title:
                self.__class__.sport_id = sport['id']
                self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                      inclusionList=[self.segment],
                                                      universalSegment=False)
                break
        else:
            raise VoltronException(f'{vec.olympics.WRESTLING} sport not found in sports categories')

    def test_001_launch_coral_and_lads_appmobile_web(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web
        EXPECTED: Homepage should load as per CMS config
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_universal_view_observe_for_Sports_ribbon_and_Inplay_Module_as_per_pre_conditions(self):
        """
        DESCRIPTION: verify universal view ,observe all modules(as per pre conditions)
        EXPECTED: No data (records) should be displayed for Sports ribbon and Inplay Module as there is no universal configuration
        """
        self.verify_sport_category_UI(sport=False)

    def test_003_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Homepage should load as per CMS segment config.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=60)

    def test_004_verify_homepage(self):
        """
        DESCRIPTION: Verify homepage
        EXPECTED: Segmented records for Sports ribbon and Inplay Module should display as per CMS configurations
        """
        self.verify_sport_category_UI()
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertTrue(sports, msg='No inplay sports found in the module')
        self.__class__.sport_name = sports[-1]
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_name.title(),
                                                   universalSegment=False,
                                                   inclusionList=[self.segment])
        self.device.refresh_page()
        inplay_sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertIn(self.sport_name, inplay_sports,
                      msg=f'Segmented record {self.sport_name} is not displayed among {inplay_sports}')

    @classmethod
    def custom_tearDown(cls):
        cms = cls.get_cms_config()
        cms.update_inplay_sport_module(segment_name=cls.segment,
                                       sport_name=cls.sport_name.title(),
                                       universalSegment=True)
        cms.update_sport_category(sport_category_id=cls.sport_id)
