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
class Test_C62701230_Verify_univerasal_view_not_segmented_view_for_Non_CSP_associated_modlues(Common):
    """
    TR_ID: C62701230
    NAME: Verify univerasal view (not segmented view ) for Non-CSP associated modlues
    DESCRIPTION: This test case verifies about Non -CSP associated modules
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Menus > Footer menu"
    PRECONDITIONS: 2)Create a some Segmented and universal Footer menus
    PRECONDITIONS: 3)Should enabled  some Non CSP modules
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_footer_menu_link(self):
        """
        DESCRIPTION: Click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus should be displayed.
        """
        pass

    def test_004_verify_non_csp_in_cms__exinplay(self):
        """
        DESCRIPTION: Verify Non CSP in CMS ( ex:Inplay)
        EXPECTED: Non CSP modules should be enabled in CMS
        """
        pass

    def test_005_launch_the_oxygen_application_verify_non_csp_and_csp_modules(self):
        """
        DESCRIPTION: Launch the Oxygen application ,Verify Non CSP and CSP modules
        EXPECTED: Non CSP modules should be shown in universal view
        """
        pass
