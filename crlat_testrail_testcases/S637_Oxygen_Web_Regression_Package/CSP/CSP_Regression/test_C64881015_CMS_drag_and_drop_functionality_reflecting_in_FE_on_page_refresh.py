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
class Test_C64881015_CMS_drag_and_drop_functionality_reflecting_in_FE_on_page_refresh(Common):
    """
    TR_ID: C64881015
    NAME: CMS drag and drop functionality reflecting in FE on page refresh
    DESCRIPTION: Test case verifies possibility to order super button module for Universal
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
        EXPECTED: User should be able to view existing super buttons
        """
        pass

    def test_004_verify_newly_created_super_buttons_ordering(self):
        """
        DESCRIPTION: Verify newly created super buttons ordering
        EXPECTED: User should be able to view new configuration at the end of the list of existing  configurations by default.
        """
        pass

    def test_005_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_006_verify_super_button_in_home_page(self):
        """
        DESCRIPTION: Verify super button in Home page
        EXPECTED: Super button should display as per CMS configuration
        """
        pass

    def test_007_change_the_order_by_drag_and_drop_in_cms_verify_in_fe(self):
        """
        DESCRIPTION: Change the order by drag and drop in CMS ,Verify in FE
        EXPECTED: Changes should reflect upon page refresh only.
        """
        pass

    def test_008_repeat_same_steps_for_segment_user_logged_in(self):
        """
        DESCRIPTION: Repeat same steps for segment user logged in
        EXPECTED: 1.Super button should display as per CMS segment configuration
        """
        pass

    def test_009_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2.Changes should reflect upon page refresh only.
        """
        pass
