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
class Test_C60727648_Euro_loyalty__Verify_free_bet_value_and_label_as_per_user_tier_config(Common):
    """
    TR_ID: C60727648
    NAME: Euro loyalty - Verify free bet value and label as per user tier config
    DESCRIPTION: This test case is to verify free bet token details in user account
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

    def test_002_verify_free_bet_token_value_for_tier1_user(self):
        """
        DESCRIPTION: Verify free bet token value for tier1 user
        EXPECTED: free bet value in message Free Bets value either Â£5 or Â£10 or Â£20, which is based on the configuration setup in Open Bet and user customer tier segment.
        """
        pass

    def test_003_repeat_above_step_for_tier2tier3_and_tier_4_users(self):
        """
        DESCRIPTION: Repeat above step for tier2,tier3 and tier 4 users
        EXPECTED: free bet value in message Free Bets value either Â£5 or Â£10 or Â£20, which is based on the configuration setup in Open Bet and user customer tier segment.
        """
        pass

    def test_004_verify_free_bet_label_display_for_tier_1_user(self):
        """
        DESCRIPTION: Verify free bet label display for tier 1 user
        EXPECTED: Free bet label should be as CMS config per user tier
        """
        pass

    def test_005_repeat_above_step_for_tier2tier3_and_tier_4_users(self):
        """
        DESCRIPTION: Repeat above step for tier2,tier3 and tier 4 users
        EXPECTED: Free bet label should be as CMS config per user tier
        """
        pass
