import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28077_Verify_Body_View_for_Desktop(Common):
    """
    TR_ID: C28077
    NAME: Verify Body View for Desktop
    DESCRIPTION: This test case verifies Desktop Body View.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    PRECONDITIONS: NOTE: Main view second column is present on Sports Landing page and Racing Landing page(when widgets are available)
    """
    keep_browser_open = True

    def test_001_verify_desktop_bodyviewup_to_1099px(self):
        """
        DESCRIPTION: Verify Desktop Body View up to 1099px
        EXPECTED: Desktop View is displayed with Left menu navigation and 2 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: *   Header
        EXPECTED: *   Left Navigation - fixed 160px
        EXPECTED: *   Main view - fluid width
        EXPECTED: *   Right Column View - fixed 320px
        EXPECTED: *   Global footer
        """
        pass

    def test_002_verify_desktop_bodyview1100px(self):
        """
        DESCRIPTION: Verify Desktop Body View 1100px
        EXPECTED: Desktop View is displayed with Left menu navigation and 3 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: *   Header
        EXPECTED: *   Left Navigation - fixed width 160px
        EXPECTED: *   Main view column 1- width 60%
        EXPECTED: *   Main view column 2 - width 40%
        EXPECTED: *   Right Column View - fixed width 320px
        EXPECTED: *   Global footer
        """
        pass

    def test_003_verify_desktop_bodyviewfrom_1100_to_1599px(self):
        """
        DESCRIPTION: Verify Desktop Body View from 1100 to 1599px
        EXPECTED: Desktop View is displayed with Left menu navigation and 3 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: *   Header
        EXPECTED: *   Left Navigation - fixed width 160px
        EXPECTED: *   Main view column 1- fluid width 60%
        EXPECTED: *   Main view column 2 - fluid width 40%
        EXPECTED: *   Right Column View - fixed width 320px
        EXPECTED: *   Global footer
        """
        pass

    def test_004_verify_desktop_bodyviewfrom_1600_to_1919px(self):
        """
        DESCRIPTION: Verify Desktop Body View from 1600 to 1919px
        EXPECTED: Desktop View is displayed with Left menu navigation and 3 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: *   Header - fixed width 1600px
        EXPECTED: *   Left Navigation - fixed width 160px
        EXPECTED: *   Main view column 1 - fixed width 660px
        EXPECTED: *   Main view column 2 - fixed width 430px
        EXPECTED: *   Right Column View - fixed width 320px
        EXPECTED: *   Global footer
        EXPECTED: *   Fluid margins along two sides of the page
        """
        pass

    def test_005_verify_desktop_bodyviewfrom_1920px(self):
        """
        DESCRIPTION: Verify Desktop Body View from 1920px
        EXPECTED: Desktop View is displayed with Left menu navigation and 3 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: *   Header - fixed witdth 1600px
        EXPECTED: *   Left Navigation - fixed width 160px
        EXPECTED: *   Main view column 1- fixed width 660px
        EXPECTED: *   Main view column 2 - fixed width 430px
        EXPECTED: *   Right Column View - fixed width 320px
        EXPECTED: *   Global footer
        EXPECTED: *   Fluid margins along two sides of the page
        """
        pass

    def test_006_verify_desktop_bodyviewmore_than_1920px(self):
        """
        DESCRIPTION: Verify Desktop Body View more than 1920px
        EXPECTED: Desktop View is displayed with Left menu navigation and 3 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: *   Header - fixed witdth 1600px
        EXPECTED: *   Left Navigation - fixed width 160px
        EXPECTED: *   Main view column 1- fixed width 660px
        EXPECTED: *   Main view column 2 - fixed width 430px
        EXPECTED: *   Right Column View - fixed width 320px
        EXPECTED: *   Global footer
        EXPECTED: *   Fluid margins along two sides of the page
        """
        pass

    def test_007_verify_that_desktop_view_is_not_displayed_for_tablets_where_width_is_1024px_and_less(self):
        """
        DESCRIPTION: Verify that Desktop View is not displayed for Tablets where width is 1024px and less
        EXPECTED: Tablet View is displayed and consists of:
        EXPECTED: *   Header
        EXPECTED: *   Sports Ribbon
        EXPECTED: *   Main view
        EXPECTED: *   Right Column View
        EXPECTED: *   Fixed footer
        """
        pass
