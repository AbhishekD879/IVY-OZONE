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
class Test_C60709309_Euro_Loyalty__Yellow_line_display(Common):
    """
    TR_ID: C60709309
    NAME: Euro Loyalty - Yellow line display
    DESCRIPTION: This test case verifies display of yellow line for next badge
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - EuroLoyality page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyalty_page_and_verify_ui(self):
        """
        DESCRIPTION: Navigate to Euro Loyalty page and verify UI
        EXPECTED: 1.  All the badges should display in grey out
        EXPECTED: 2.  Small yellow line should display under first badge
        EXPECTED: 3.  If user collect one badge, new badge should display yellow line
        """
        pass

    def test_003_repeat_above_steps_for_user_with_different_tier_level(self):
        """
        DESCRIPTION: Repeat above steps for user with different tier level
        EXPECTED: Should work as expected
        """
        pass
