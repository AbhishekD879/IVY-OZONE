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
class Test_C62900236_Verify_Quick_links_display_on_page_load_in_CMS(Common):
    """
    TR_ID: C62900236
    NAME: Verify Quick links display on page load in CMS
    DESCRIPTION: This test case verifies display of Quick links module page in CMS
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >Home page > Quick links
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
        EXPECTED: User should be able to view the Quick links Module page
        """
        pass

    def test_003_verify_quick_links_page(self):
        """
        DESCRIPTION: Verify Quick links page
        EXPECTED: The Quick links Module page as per the designs below
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: Create Quick links
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: Segment
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: Download CSV
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: Search field
        """
        pass

    def test_008_verify_segment_dropdown(self):
        """
        DESCRIPTION: Verify Segment dropdown
        EXPECTED: The dropdown will show all the segments,
        """
        pass

    def test_009_(self):
        """
        DESCRIPTION: 
        EXPECTED: Segmented drop down should Universal is highlighted  by default
        """
        pass

    def test_010_verify_segment_dropdown_defaulted_by_universal(self):
        """
        DESCRIPTION: Verify Segment dropdown defaulted by Universal
        EXPECTED: Should display Universal records by default
        """
        pass
