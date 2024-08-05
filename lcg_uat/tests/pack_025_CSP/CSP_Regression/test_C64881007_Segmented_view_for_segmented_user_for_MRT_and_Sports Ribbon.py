import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@vtest
class Test_C64881007_Segmented_view_for_segmented_user_for_MRT_and_Sports_ribbon(Common):
    """
    TR_ID: C64881007
    NAME: Verify segmented view for segmented user for MRT and Sports Ribbon
    DESCRIPTION: This test case verifies segmented view for segmented user
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Homepage > MRT/Sports Ribbon
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    tab_title = 'Auto_CSP_Segment_Dont_DELETE'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Highlights Carousels/Surface bet
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == vec.olympics.WRESTLING:
                self.__class__.sport_id = sport['id']
                self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                      inclusionList=[self.segment],
                                                      universalSegment=False)
                break
        else:
            raise VoltronException(f'{vec.olympics.WRESTLING} sport not found in sports categories')
        self.cms_config.module_ribbon_tabs.update_tab(tab_name=self.tab_title, inclusion_list=[self.segment], universal=False)

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
        EXPECTED: User should able to see segmented record(The first valid Super button)for specific segmented user as per CMS configuration
        """
        module_ribbon_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertIn(self.tab_title.upper(), module_ribbon_tabs,
                      msg=f'Module ribbon tab {self.tab_title.upper()} is not displayed')
        sports = list(self.site.home.menu_carousel.items_as_ordered_dict.keys())
        self.assertIn(vec.olympics.WRESTLING, sports,
                      msg=f'Created sport category "{vec.olympics.WRESTLING}" is not appearing, actual categories "{sports}"')

    @classmethod
    def custom_tearDown(cls):
        cls.get_cms_config().update_sport_category(sport_category_id=cls.sport_id)


