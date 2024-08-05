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
class Test_C62764774_Verify_Edit_surface_bet_with_segment_with_single_segments_inclusion_and_verify_in_FE(Common):
    """
    TR_ID: C62764774
    NAME: Verify Edit surface bet with segment (with single segment(s) inclusion) and verify in FE
    DESCRIPTION: This test case verifies editing of existing Segment(s) inclusion surface bet
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
    PRECONDITIONS: 2) Create a Segment(s) inclusion surface bet
    PRECONDITIONS: 3) Segment should be created in Optimove and user should mapped to respective segment
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_precondition_1(self):
        """
        DESCRIPTION: Navigate to module from precondition 1.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_surface_bet__link(self):
        """
        DESCRIPTION: Click on surface bet  link.
        EXPECTED: User should be able to view existing surface bet  should be displayed.
        """
        pass

    def test_004_click_on_existing_surface_bet__with_segment_inclusion(self):
        """
        DESCRIPTION: Click on existing surface bet  with segment inclusion
        EXPECTED: surface bet  detail page should be opened  with universal and segment(s) inclusion text box
        """
        pass

    def test_005_edit_existing_surface_bet(self):
        """
        DESCRIPTION: Edit existing surface bet
        EXPECTED: Add one segments in segment(s) inclusion text box
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: surface bet should be update successfully.
        """
        pass

    def test_007_load_oxygen_and_verify_surface_bet(self):
        """
        DESCRIPTION: Load oxygen and verify surface bet
        EXPECTED: Updated surface bet  should be shown for specific segmented user
        """
        pass
