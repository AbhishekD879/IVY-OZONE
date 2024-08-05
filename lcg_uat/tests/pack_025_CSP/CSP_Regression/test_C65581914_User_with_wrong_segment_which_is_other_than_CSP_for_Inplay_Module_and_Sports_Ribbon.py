import pytest
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581914_User_with_wrong_segment_which_is_other_than_CSP_for_Inplay_Module_and_Sports_Ribbon(Common):
    """
    TR_ID: C65581914
    NAME: User with wrong segment which is other than CSP_ for Inplay Module and Sports Ribbon
    DESCRIPTION: This test case verifies segment name
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Inplay Module/Sports Ribbon
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL.
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    Wrong_segment = vec.bma.UNIVERSAL_SEGMENT
    title = vec.olympics.WRESTLING

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Inplay Module/Sports Ribbon
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

    def test_003_click_on_Inplay_Module_Sports_Ribbon_link(self):
        """
        DESCRIPTION: Click on  Inplay Module/Sports Ribbon link.
        EXPECTED: User should be able to view existing  Inplay Module/Sports Ribbon
        """
        # Covered in preconditions

    def test_004_create_a_segmented_Inplay_Module_Sports_Ribbon_with_csp__excsp_1_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented Inplay Module/Sports Ribbon with CSP_ (Ex:CSP_1) segment name and Login with Segmented user Verify in FE
        EXPECTED: User should able to view segmented Inplay Module/Sports Ribbon
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertTrue(sports, msg='No inplay sports found in the module')
        self.__class__.sport_name = sports[-1]
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_name.title(),
                                                   universalSegment=False,
                                                   inclusionList=[self.segment])
        self.device.refresh_page()
        inplay_sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertIn(self.sport_name, inplay_sports, msg=f'Segmented record {self.sport_name} is not displayed among {inplay_sports}')
        title = self.title if self.site.brand == 'ladbrokes' else self.title.upper()
        sports = list(self.site.home.menu_carousel.items_as_ordered_dict.keys())
        self.assertIn(title, sports,
                      msg=f'Created sport category "{title}" is not appearing, actual categories "{sports}"')
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_005_create_a_segmented_Inplay_Module_Sports_Ribbon_otherthan_csp__exsegment_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented Inplay Module/Sports Ribbon otherthan CSP_(ex:Segment )segment name and Login with Segmented user Verify in FE
        EXPECTED: If user should belongs to wrong segment (without CSP_) Universal view should be displayed.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.Wrong_segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        inplay_sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertNotIn(self.sport_name, inplay_sports,
                         msg=f'Segmented record {self.sport_name} is not displayed among {inplay_sports}')
        sports = list(self.site.home.menu_carousel.items_as_ordered_dict.keys())
        self.assertNotIn(self.title, sports,
                         msg=f'Created sport category "{self.title}" is appearing, actual categories "{sports}"')

    def test_006_repeat_same_steps_for_all_the_modules(self):
        """
        DESCRIPTION: Repeat same steps for all the modules
        EXPECTED: Universal view should displayed for wrong segmented name
        """
        # Covered in above steps

    @classmethod
    def custom_tearDown(cls):
        cms = cls.get_cms_config()
        cms.update_inplay_sport_module(segment_name=cls.segment,
                                       sport_name=cls.sport_name.title(),
                                       universalSegment=True)
        cms.update_sport_category(sport_category_id=cls.sport_id)
