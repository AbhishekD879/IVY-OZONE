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
class Test_C64881018_User_with_wrong_segment_which_is_other_than_CSP_(Common):
    """
    TR_ID: C64881018
    NAME: User with wrong segment which is other than CSP_
    DESCRIPTION: This test case verifies segment name
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.( all modules )
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
        DESCRIPTION: Click on super button link.
        EXPECTED: User should be able to view existing super buttons
        """
        pass

    def test_004_create_a_segmented_super_button_with_csp__excsp_1_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented super button with CSP_ (Ex:CSP_1) segment name and Login with Segmented user Verify in FE
        EXPECTED: User should able to view segmented super button
        """
        pass

    def test_005_create_a_segmented_super_button_otherthan_csp__exsegment_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented super button otherthan CSP_ (ex:Segment )segment name and Login with Segmented user Verify in FE
        EXPECTED: If user should belongs to wrong segment (without CSP_) Universal view should be displayed.
        """
        pass

    def test_006_repeat_same_steps_for_all_the_modules(self):
        """
        DESCRIPTION: Repeat same steps for all the modules
        EXPECTED: Universal view should displayed for wrong segmented name
        """
        pass
