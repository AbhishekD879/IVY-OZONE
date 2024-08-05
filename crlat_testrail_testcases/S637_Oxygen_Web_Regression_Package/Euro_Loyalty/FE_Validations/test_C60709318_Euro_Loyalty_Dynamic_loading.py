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
class Test_C60709318_Euro_Loyalty_Dynamic_loading(Common):
    """
    TR_ID: C60709318
    NAME: Euro Loyalty- Dynamic loading
    DESCRIPTION: This test case is to validate current stage should always show in 2nd place
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

    def test_002_verify_current_stage_is_showing_in_2nd_place(self):
        """
        DESCRIPTION: verify current stage is showing in 2nd place
        EXPECTED: 1.  Always current stage should display in 2nd place
        EXPECTED: 2.  First time navigation user has not placed any bet - first stage should display in first row
        EXPECTED: 3.  User is in second stage after placing 3 bets
        EXPECTED: 4.  First row should display with active badges and second stage should display in second row
        EXPECTED: 5.  If user is in 3rd stage, first row should scroll up and 3rd stage should display in 2nd row
        EXPECTED: 6.  It should repeat till 7th stage
        """
        pass

    def test_003_repeat_above_steps_for_users_with_different_tiers(self):
        """
        DESCRIPTION: Repeat above steps for users with different tiers
        EXPECTED: Should work as expected
        """
        pass
