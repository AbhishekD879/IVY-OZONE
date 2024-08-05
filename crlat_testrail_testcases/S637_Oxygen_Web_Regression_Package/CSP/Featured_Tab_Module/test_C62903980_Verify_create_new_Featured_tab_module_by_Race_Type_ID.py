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
class Test_C62903980_Verify_create_new_Featured_tab_module_by_Race_Type_ID(Common):
    """
    TR_ID: C62903980
    NAME: Verify create new Featured tab module by Race Type ID
    DESCRIPTION: This test case verifies the CMS configurations for Featured tab module with Race Type ID
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Featured tab module
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

    def test_003_click_on_featured_tab_module_link(self):
        """
        DESCRIPTION: click on Featured tab module link.
        EXPECTED: a) User should be able to view Create Featured tab module CTA.
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Existing Featured tab modules should be displayed.
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: c) Name,Segment(s),Segment(s) exclusion,Enabled,Display From,Display To,Channels,Personalized,Remove,Edit Columns should be displayed.
        """
        pass

    def test_006_click_on_create_featured_tab_module_with_race_type_id(self):
        """
        DESCRIPTION: Click on create Featured tab module with Race Type ID
        EXPECTED: User should able to create Featured module with Race Type ID and appended at the end of the list of existing segment-specific configurations by default and allow reordering.
        """
        pass
