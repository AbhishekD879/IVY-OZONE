import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60727642_Verify_display_of_Banner_in_content_area(Common):
    """
    TR_ID: C60727642
    NAME: Verify display of Banner in content area
    DESCRIPTION: This test case verifies banner display in content area
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyalty_page_and_verify_banner_display(self):
        """
        DESCRIPTION: Navigate to Euro Loyalty page and verify banner display
        EXPECTED: TBD
        """
        pass
