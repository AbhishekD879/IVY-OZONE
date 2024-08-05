import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C57732018_KYC_Verify_opening_1_2_Free_when_user_Under_Review(Common):
    """
    TR_ID: C57732018
    NAME: KYC. Verify opening 1-2-Free when user Under Review
    DESCRIPTION: This test case verifies that user won't play 1-2-Free when he is under review
    PRECONDITIONS: To check user status type: 'universal_variable.user' in browser console -> check 'verificationStatus' value
    PRECONDITIONS: Passed user: 'KYCinreview01 / Test1234'
    PRECONDITIONS: In review: 'KYCTEST3/ KYCTEST3123'
    PRECONDITIONS: Failed: 'Sofofika1 / Password01'
    PRECONDITIONS: or go to IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+FE+for+testing+AEM+banners
    PRECONDITIONS: change 'Age verification' status to 'under review'
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_in_review_statusand_tap_on_1_2_free_link(self):
        """
        DESCRIPTION: log in with user that 'In review' status
        DESCRIPTION: and tap on '1-2-Free' link
        EXPECTED: User see pop-up with 'Account in Review' title
        """
        pass

    def test_002_go_to_ims_and_change_status_to_passed__and_tap_on_1_2_free_link(self):
        """
        DESCRIPTION: Go to IMS and change status to 'Passed'  and tap on '1-2-Free...' link
        EXPECTED: User should not see pop-up any-more
        EXPECTED: 1-2-Free Splash should be visible and user can play 1-2-Free
        """
        pass
