import pytest
import voltron.environments.constants as vec
from faker import Faker
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.reg156_fix
@pytest.mark.mobile_only
@vtest
class Test_C65026351_Verify_create_edit_sports_configuration_for_universal_segment_in_sports_ribbon_and_verify_in_FE(Common):
    """
    TR_ID: C65026351
    NAME: Verify create/edit sports configuration for universal/segment in sports ribbon and verify in FE
    DESCRIPTION: This testcase verifies create/edit sports configuration in sports ribbon should reflect with refresh only in FE
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > Sports pages > Sports category
    """
    keep_browser_open = True
    segment = vec.bma.CSP_CMS_SEGEMENT
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    fake = Faker()
    title = vec.olympics.RUGBYUNION

    def verify_sport_category_UI(self):
        """
        To verify create sport category used this method
        """
        title = self.title if self.site.brand == 'ladbrokes' else self.title.upper()
        sports = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(sports.get(title),
                        msg=f'sport category "{title}" is not appearing, actual categories "{sports}"')

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Sports pages > Sports category
        """
        # using existing sports category 'Wrestling'

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        # Covered in above step

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should able to see the Sport Categories Page by default 'Sports category' is selected
        """
        # Covered in above step

    def test_003_click_on_create_sport_category_ctaenter_required_fields(self):
        """
        DESCRIPTION: Click on 'Create sport category' CTA,enter required fields
        EXPECTED: User should able view new sport category page with all CSP related fields.
        """
        # Covered in above step

    def test_004_select_universal_and_click_on_save_button(self):
        """
        DESCRIPTION: Select universal and click on save button
        EXPECTED: New Sport should be added in Universal list
        """
        # Covered in above step

    def test_005_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch Oxygen application
        EXPECTED: 'Home page should launch successfully
        """
        self.site.wait_content_state("homepage")

    def test_006_verify_sports_ribbon_before_login(self):
        """
        DESCRIPTION: Verify Sports ribbon before login
        EXPECTED: Universal view should be displayed as per CMS Configuration
        """
        self.verify_sport_category_UI()

    def test_007_login_with_a_usernot_segmentedverify_sports_ribbon(self):
        """
        DESCRIPTION: Login with a user(not segmented)Verify Sports ribbon
        EXPECTED: Universal sports should be displayed as per CMS Configuration
        """
        self.site.login()
        self.verify_sport_category_UI()

    def test_008_verify_sports_ribbon_for_logged_out_user(self):
        """
        DESCRIPTION: Verify sports ribbon for logged out user
        EXPECTED: Universal sports should be displayed as per CMS Configuration
        """
        self.site.logout()
        self.verify_sport_category_UI()

    def test_009_repeate_above_steps_for_segments_inclusion_for_segmented_user_singlemultiple(self):
        """
        DESCRIPTION: Repeate above steps for segment(s) inclusion for Segmented user (single/Multiple)
        EXPECTED: 'Changes should reflect in sports ribbon with refresh only
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == vec.olympics.RUGBYUNION:
                self.__class__.sport_id = sport['id']
                self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                      inclusionList=[self.segment],
                                                      universalSegment=False)
                break
        else:
            raise VoltronException(f'{vec.olympics.RUGBYUNION} sport not found in sports categories')
        sleep(2)
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        sleep(10)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        self.verify_sport_category_UI()
