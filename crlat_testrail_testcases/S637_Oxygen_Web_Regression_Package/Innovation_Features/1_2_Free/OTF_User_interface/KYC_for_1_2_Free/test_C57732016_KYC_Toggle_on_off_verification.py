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
class Test_C57732016_KYC_Toggle_on_off_verification(Common):
    """
    TR_ID: C57732016
    NAME: KYC. Toggle on/off verification
    DESCRIPTION: This test cases verifies toggling of verification of user.
    PRECONDITIONS: Passed user: 'KYCinreview01 / Test1234'
    PRECONDITIONS: In review: 'KYCTEST3/ KYCTEST3123'
    PRECONDITIONS: Failed: 'Sofofika1 / Password01'
    PRECONDITIONS: or go to IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+FE+for+testing+AEM+banners
    PRECONDITIONS: change 'Age verification' status to 'under review'
    """
    keep_browser_open = True

    def test_001_turn_on_enable_kyc_verification__httpsappqubitcomp3209experiences161041(self):
        """
        DESCRIPTION: Turn on 'Enable KYC verification'  'https://app.qubit.com/p/3209/experiences/161041/'
        EXPECTED: 
        """
        pass

    def test_002_log_in_with_in_review_account_see_pre_conditions(self):
        """
        DESCRIPTION: Log in with 'In review' account (see pre-conditions)
        EXPECTED: User is successfully logged in
        """
        pass

    def test_003_navigate_to_football_tap_on_1_2_free_link(self):
        """
        DESCRIPTION: Navigate to Football, tap on '1-2-Free...' link
        EXPECTED: User should see pop-up 'Account in Review'
        """
        pass

    def test_004_verify_pop_up_view(self):
        """
        DESCRIPTION: Verify Pop-up view
        EXPECTED: Title: 'Account in Review'
        EXPECTED: Body: 'Your Account is in review. We aim to get back to you within 2 hours. You’ll receive an email and onsite message.'
        EXPECTED: Button: 'Ok'
        """
        pass

    def test_005_turn_off_enable_kyc_verification_httpsappqubitcomp3209experiences161041(self):
        """
        DESCRIPTION: Turn off 'Enable KYC verification' 'https://app.qubit.com/p/3209/experiences/161041/'
        EXPECTED: 
        """
        pass

    def test_006_log_in_with_in_review_account_see_pre_conditions(self):
        """
        DESCRIPTION: Log in with 'In review' account (see pre-conditions)
        EXPECTED: User is successfully logged in
        """
        pass

    def test_007_navigate_to_football_tap_on_1_2_free_link(self):
        """
        DESCRIPTION: Navigate to Football, tap on '1-2-Free...' link
        EXPECTED: User can play 1-2-Free
        """
        pass
