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
class Test_C40876_Verify_users_time_zone_clock_on_the_footer(Common):
    """
    TR_ID: C40876
    NAME: Verify user's time zone clock on the footer
    DESCRIPTION: This test case verifies user's time zone clock on the global footer
    DESCRIPTION: ONLY FOR CORAL. For Ladbrokes, this shouldn't be shown.
    DESCRIPTION: AUTOTEST [C2594274]
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify__users_time_zone_clock_on_the_global_footer(self):
        """
        DESCRIPTION: Verify  user's time zone clock on the Global Footer
        EXPECTED: User's time zone clock is absent
        """
        pass

    def test_003_log_in_to_oxygen_application(self):
        """
        DESCRIPTION: Log in to Oxygen application
        EXPECTED: User is logged in
        """
        pass

    def test_004_verify_users_time_zone_clock_on_the_global_footercoral_only(self):
        """
        DESCRIPTION: Verify user's time zone clock on the Global Footer
        DESCRIPTION: (Coral Only)
        EXPECTED: - User's time zone clock is present on the Global Footer
        EXPECTED: - User's time zone clock is separated from session timer by '|' (Only for Coral. For Ladbrokes session timer shouldn't be shown)
        EXPECTED: - User's time zone clock consists of clock icon and time
        EXPECTED: - User's time zone clock shows current time as it is in user's time zone
        """
        pass

    def test_005_verify_users_time_zone_clock_format(self):
        """
        DESCRIPTION: Verify user's time zone clock format
        EXPECTED: Time format is 24 hours e.g. **HH:MM:SS** (e.g. 14:59:59 or 05:01:01)
        """
        pass

    def test_006_turn_phone_to_the_sleep_mode_and_check_users_time_zone_clock_after_few_minutes(self):
        """
        DESCRIPTION: Turn phone to the sleep mode and check user's time zone clock after few minutes
        EXPECTED: User's time zone clock is reflected accordingly to current time of the user's time zone
        """
        pass

    def test_007_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User's time zone clock is no more shown on the Global Footer
        """
        pass
