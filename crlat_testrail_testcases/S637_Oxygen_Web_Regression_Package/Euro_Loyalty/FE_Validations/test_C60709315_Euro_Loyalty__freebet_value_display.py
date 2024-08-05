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
class Test_C60709315_Euro_Loyalty__freebet_value_display(Common):
    """
    TR_ID: C60709315
    NAME: Euro Loyalty - freebet value display
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

    def test_003_verify_free_bet_value_display(self):
        """
        DESCRIPTION: Verify free bet value display
        EXPECTED: Free Bets value either £5 or £10 or £20, which is based on the configuration setup in Open Bet for the offer and user customer tier segment.
        """
        pass

    def test_004_configure_multiple_offers_with_different_freebet_rewards_token_for_same_tier_user_and_verifyoffer1_with_5_rewards_tokenoffer1_with_10_rewards_token(self):
        """
        DESCRIPTION: Configure multiple offers with different freebet rewards token for same tier user and verify
        DESCRIPTION: Offer1 with £5 rewards token
        DESCRIPTION: Offer1 with £10 rewards token
        EXPECTED: After user placing qualifying bets in stage1 he should get £5 rewards token and after placing qualifying bets in stage2 he should rewarded with £10 freebet token
        """
        pass

    def test_005_verify_freebet_label(self):
        """
        DESCRIPTION: Verify freebet label
        EXPECTED: freebet label should be displayed
        """
        pass

    def test_006_repeat_above_steps_for_users_with_different_tiers(self):
        """
        DESCRIPTION: Repeat above steps for users with different tiers
        EXPECTED: Should work as expected
        """
        pass
