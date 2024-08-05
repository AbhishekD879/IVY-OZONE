import pytest
import datetime
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.reg156_fix
@pytest.mark.mobile_only
@vtest
class Test_C65599281_Segmented_view_for_segmented_user_for_super_button(Common):
    """
    TR_ID: C65599281
    NAME: Verify segmented view for segmented user for Super Button.
    DESCRIPTION: This test case verifies segmented view for segmented user
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Super Button
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    super_button_title = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Super Button
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        super_buttons = self.cms_config.get_mobile_super_buttons()
        current_time = datetime.datetime.now().strftime(self.ob_format_pattern)
        for super_button in super_buttons:
            if super_button['enabled'] and current_time < super_button['validityPeriodEnd']:
                self.__class__.super_button_title = super_button['title']
                self.cms_config.update_mobile_super_button(name=self.super_button_title,
                                                           inclusionList=[vec.bma.CSP_CMS_SEGEMENT], universalSegment=False)
                break
        if not self.super_button_title:
            super_button_data = self.cms_config.add_mobile_super_button(inclusionList=[vec.bma.CSP_CMS_SEGEMENT],universalSegment=False)
            self.__class__.super_button_title = super_button_data['title']


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
        self.assertTrue(self.site.home.quick_link_section.has_button, msg='Super button is not displayed')
        button_name = self.site.home.quick_link_section.button.name
        self.assertEqual(button_name.upper(), self.super_button_title.upper(),
                         msg=f'Actual button name "{button_name}" is not same as '
                             f'Expected button name {self.super_button_title}')
