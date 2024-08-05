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
class Test_C57732019_KYC_Verify_opening_1_2_Free_when_user_verification_Failed(Common):
    """
    TR_ID: C57732019
    NAME: KYC. Verify opening 1-2-Free when user verification Failed
    DESCRIPTION: This test case verifies that user can't play -1-2-Free when his Status is 'Failed'
    PRECONDITIONS: To check user status type: 'universal_variable.user' in browser console -> check 'verificationStatus' value
    PRECONDITIONS: Passed user: 'KYCinreview01 / Test1234'
    PRECONDITIONS: In review: 'KYCTEST3/ KYCTEST3123'
    PRECONDITIONS: Failed: 'Sofofika1 / Password01'
    PRECONDITIONS: or go to IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+FE+for+testing+AEM+banners
    PRECONDITIONS: change 'Age verification' status to 'Failed'
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_failed_statusand_tap_on_1_2_free_link(self):
        """
        DESCRIPTION: log in with user that 'Failed' status
        DESCRIPTION: and tap on '1-2-Free' link
        EXPECTED: User can't tap on '1-2-Free' because he should be redirected to 'Account one' page
        """
        pass
