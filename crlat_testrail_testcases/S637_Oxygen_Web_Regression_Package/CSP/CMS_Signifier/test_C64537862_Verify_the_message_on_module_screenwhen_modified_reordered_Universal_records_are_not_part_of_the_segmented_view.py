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
class Test_C64537862_Verify_the_message_on_module_screenwhen_modified_reordered_Universal_records_are_not_part_of_the_segmented_view(Common):
    """
    TR_ID: C64537862
    NAME: Verify the message on module screenwhen modified/reordered Universal records are not part of the segmented view.
    DESCRIPTION: This testcase verifies the message on module screenwhen modified/reordered Universal records are not part of the segmented view.
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2.CMS configuration:
    PRECONDITIONS: CMS &gt; Sports pages &gt;home page&gt;Surface bet/HC/QL
    PRECONDITIONS: CMS&gt;Featured tab module/MRT
    PRECONDITIONS: 3."One or more Universal module has been re-ordered for this Segment". Message is displayed in Module screen as Universal records are reorderd for that particular segment
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

    def test_003_navigate_to_segmented_view(self):
        """
        DESCRIPTION: Navigate to Segmented view
        EXPECTED: "One or more Universal module has been re-ordered for this Segment". Message is displayed in Module screen as Universal records are reorderd for that particular segment
        """
        pass

    def test_004_navigate_to_universal_view_and_exclude_remove_records_which_are_reorderd_in_segmented_view(self):
        """
        DESCRIPTION: Navigate to Universal view and exclude /Remove records which are reorderd in segmented view
        EXPECTED: No message should appear on the modules screen in segmented view
        """
        pass

    def test_005_repeat_steps_from_2_to_5_for_all_modules(self):
        """
        DESCRIPTION: Repeat steps from 2 to 5 for all modules
        EXPECTED: No message should appear on the modules screen in segmented view
        """
        pass
