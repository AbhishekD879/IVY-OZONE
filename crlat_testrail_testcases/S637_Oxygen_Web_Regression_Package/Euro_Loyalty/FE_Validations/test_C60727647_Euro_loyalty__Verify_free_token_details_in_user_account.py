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
class Test_C60727647_Euro_loyalty__Verify_free_token_details_in_user_account(Common):
    """
    TR_ID: C60727647
    NAME: Euro loyalty - Verify free token details in user account
    DESCRIPTION: This test case is to verify free bet token details in user account
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    PRECONDITIONS: 4.  User should awarded with free bet token
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_verify_free_bet_token_details(self):
        """
        DESCRIPTION: Verify free bet token details
        EXPECTED: Freebet token details should be displayed as per CMS/OB Configuration
        """
        pass

    def test_003_verify_the_above_for_different_tier_levels(self):
        """
        DESCRIPTION: Verify the above for different tier levels
        EXPECTED: Different tier users should have freebet tokens as per the eligibility
        """
        pass
