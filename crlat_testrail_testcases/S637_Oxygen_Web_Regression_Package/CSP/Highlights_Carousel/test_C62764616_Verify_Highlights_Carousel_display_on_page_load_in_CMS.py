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
class Test_C62764616_Verify_Highlights_Carousel_display_on_page_load_in_CMS(Common):
    """
    TR_ID: C62764616
    NAME: Verify Highlights Carousel display on page load in CMS
    DESCRIPTION: This test case verifies display of Highlights Carousel module page in CMS
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
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
        EXPECTED: User should be able to view the Highlights Carousel Module page
        """
        pass

    def test_003_verify_highlights_carousel_page(self):
        """
        DESCRIPTION: Verify Highlights Carousel page
        EXPECTED: The Highlights Carousel Module page as per the designs below
        EXPECTED: Create Highlights Carousel, Segment, Download CSV and Search field.
        """
        pass

    def test_004_verify_segment_dropdown(self):
        """
        DESCRIPTION: Verify Segment dropdown
        EXPECTED: The dropdown will show all the segments, Segmented drop down should Universal is highlighted by default
        """
        pass

    def test_005_verify_segment_dropdown_defaulted_by_universal(self):
        """
        DESCRIPTION: Verify Segment dropdown defaulted by Universal
        EXPECTED: Should display Universal records by default
        """
        pass
