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
class Test_C64881023_Verify_error_message_when_there_are_maxAmount_of_Quick_links_are_active(Common):
    """
    TR_ID: C64881023
    NAME: Verify error message when there are maxAmount of Quick links are active
    DESCRIPTION: This testcase verifies error message when there are maxAmount of Quick links are active
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)Set maxAmount of quicklinks CMS configuration.
    PRECONDITIONS: CMS> System Configuration>Structure
    PRECONDITIONS: 3)CMS configuration:
    PRECONDITIONS: CMS > Sports pages >home page>Quicklinks
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be able to see the Quick links module page with existing Universal Quick links records
        """
        pass

    def test_003_verify_noofrecords_which_are_existing(self):
        """
        DESCRIPTION: Verify no.ofÂ Â records which are existing
        EXPECTED: User should able to create new reocrds until maxAmount reached.
        """
        pass

    def test_004_if_there_are_noof_quicklinks__maxamount(self):
        """
        DESCRIPTION: If there are no.of Quicklinks < maxAmount
        EXPECTED: 
        """
        pass

    def test_005_click_on_create_sports_quick_link_cta_after_reaching_maxamount(self):
        """
        DESCRIPTION: Click on Create sports quick link CTA after reaching maxAmount
        EXPECTED: Error message shouldÂ Â prompt on New Sport Quick Link Pop up ,User should not able to create new record.
        """
        pass

    def test_006_verify_content_of_error_message(self):
        """
        DESCRIPTION: Verify content of error message
        EXPECTED: The error message should contain all segment names which are having maxAmount of active QLs
        """
        pass

    def test_007_verify_error_msg_and_content_upon_drag_and_drop_after_reaching_maxamount(self):
        """
        DESCRIPTION: Verify error msg and content upon drag and drop after reaching maxAmount
        EXPECTED: Error msg should prompt on top of Module screen upon drag and drop.
        """
        pass
