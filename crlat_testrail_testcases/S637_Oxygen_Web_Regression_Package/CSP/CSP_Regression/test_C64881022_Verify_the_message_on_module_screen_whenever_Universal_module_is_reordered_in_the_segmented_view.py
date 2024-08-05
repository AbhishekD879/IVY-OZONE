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
class Test_C64881022_Verify_the_message_on_module_screen_whenever_Universal_module_is_reordered_in_the_segmented_view(Common):
    """
    TR_ID: C64881022
    NAME: Verify the message on module screen whenever Universal module is reordered in the segmented view
    DESCRIPTION: This testcase verifies the message on module screen whenever Universal module is reordered in the segmented view
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2.CMS configuration:
    PRECONDITIONS: CMS > Sports pages >home page>Surface bet/HC/QL
    PRECONDITIONS: CMS>Featured tab module/MRT
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_navigate_to_module_from_preconditionsexquicklinks(self):
        """
        DESCRIPTION: Navigate to module from preconditions.(ex:Quicklinks)
        EXPECTED: User should be able to see the Quick links module page with existing Universal Quick links records
        """
        pass

    def test_003_reorder_the_records_in_universal(self):
        """
        DESCRIPTION: Reorder the records in Universal
        EXPECTED: User should able to reorder the records in Universal view.whatever the display order changes in Universal view shouldÂ Â  reflect in segmented view as well
        """
        pass

    def test_004_navigate_to_segmented_view_by_selecting_perticular_segment(self):
        """
        DESCRIPTION: Navigate to Segmented view by selecting perticular segment
        EXPECTED: User should able to navigate and view universal and segment specific records
        """
        pass

    def test_005_edit_the_display_order_of_universal_modules_for_that_segment(self):
        """
        DESCRIPTION: Edit the display order of Universal modules for that segment
        EXPECTED: Segmented view should display a message to Content User "One or more Universal module has been re-ordered for this Segment".
        """
        pass

    def test_006_repeat_steps_from_2_to_5_for_all_other_modules(self):
        """
        DESCRIPTION: Repeat steps from 2 to 5 for all other modules
        EXPECTED: Segmented view should display a message to Content User "One or more Universal module has been re-ordered for this Segment".
        """
        pass
