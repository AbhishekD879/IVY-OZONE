import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.other
@vtest
class Test_C60709314_Euro_Loyalty__Badge_display(Common):
    """
    TR_ID: C60709314
    NAME: Euro Loyalty - Badge display
    DESCRIPTION: This test case is to validate display of badge in FE
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created,activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyality_page(self):
        """
        DESCRIPTION: Navigate to Euro Loyality page
        EXPECTED: Matchday rewards page should display with all the details
        """
        pass

    def test_003_verify_badge_display_for_mobile_and_desktop(self):
        """
        DESCRIPTION: Verify badge display for mobile and desktop
        EXPECTED: Total no of badges should be the last value in Freebet location config in CMS for that tier
        EXPECTED: In desktop in one row 6 badges should display and in mobile 3 badges should display in one row
        EXPECTED: E.g for tier one if total no of badges is 30 then
        EXPECTED: desktop total of 30 badges in 6 Columns and 5 Rows
        EXPECTED: In mobile total of 30 badgets in 3 Columns and 10 Rows
        """
        pass

    def test_004_verify_disabled_badges(self):
        """
        DESCRIPTION: Verify disabled badges
        EXPECTED: Disabled Badges, which are greyed out signifying they have not been collected.
        """
        pass

    def test_005_verify_enabled_badges(self):
        """
        DESCRIPTION: Verify Enabled badges
        EXPECTED: Enabled Badges, which are illumined signifying they have been collected.
        EXPECTED: For Mobile:
        EXPECTED: First badge collected- Highlighted in White color
        EXPECTED: Second badge collected-Highlighted in White color
        EXPECTED: Third badge collected-Highlighted in Green color
        EXPECTED: For Desktop:
        EXPECTED: User should see the badges in the following pattern:
        EXPECTED: White, White,Green,White,White,Green.
        """
        pass

    def test_006_verify_yellow_line_for_next_badge(self):
        """
        DESCRIPTION: Verify yellow line for next badge
        EXPECTED: If user collects 4 badges, 5th badge should have yellow line
        """
        pass

    def test_007_repeat_above_steps_for_users_with_different_tiers(self):
        """
        DESCRIPTION: Repeat above steps for users with different tiers
        EXPECTED: Should work as expected
        """
        pass
