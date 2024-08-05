import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64881009_Super_button__with_universal_excluded(Common):
    """
    TR_ID: C64881009
    NAME: Super button - with universal excluded
    DESCRIPTION: This test case verifies universal exclusion
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on super button link.
        EXPECTED: User should be able to view existing super buttons should be displayed.
        """
        pass

    def test_004_click_on_super_button_cta_button(self):
        """
        DESCRIPTION: Click on super button CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select Universal radio button
        EXPECTED: Upon selecting Universal radio button ,Segment(s) Exclusion text field should be enabled and able to enter text (ex: Football)
        """
        pass

    def test_006_click_on_create_button(self):
        """
        DESCRIPTION: Click on create button
        EXPECTED: On successful creation, page should redirect to super button module page
        """
        pass

    def test_007_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_008_login_in_fe_with_userexcept_specific_segmented_user__which_is_excluded(self):
        """
        DESCRIPTION: Login in FE with user(except specific segmented user  which is excluded)
        EXPECTED: Universal user should able to view super buttons across the application except in football segment (as we have configured segment(s) Exclusion as Football)
        """
        pass

    def test_009_login_with_specific_excluded_segmented_user(self):
        """
        DESCRIPTION: Login with specific excluded segmented user
        EXPECTED: Excluded record should not displayed for specific segmented user.
        """
        pass
