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
class Test_C57732017_KYC_Verify_opening_1_2_Free_when_user_Passed(Common):
    """
    TR_ID: C57732017
    NAME: KYC. Verify opening 1-2-Free when user Passed
    DESCRIPTION: This test case verifies successful playing of 1-2-Free when customer is verified
    PRECONDITIONS: To check user status type: 'universal_variable.user' in browser console -> check 'verificationStatus' value
    PRECONDITIONS: Passed user: 'KYCinreview01 / Test1234'
    PRECONDITIONS: In review: 'KYCTEST3/ KYCTEST3123'
    PRECONDITIONS: Failed: 'Sofofika1 / Password01'
    PRECONDITIONS: or go to IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+FE+for+testing+AEM+banners
    PRECONDITIONS: change 'Age verification' status to 'Passed'
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_passed_verification(self):
        """
        DESCRIPTION: log in with user that 'Passed' verification
        EXPECTED: User navigated to 1-2-Free Splash page and can play Game
        """
        pass

    def test_002_verificationstatus_value_is_not_foundto_check_user_status_type_universal_variableuser_in_browser_console___check_verificationstatus_value__(self):
        """
        DESCRIPTION: 'verificationStatus' *value is not found*
        DESCRIPTION: To check user status type: 'universal_variable.user' in browser console -> check 'verificationStatus' value -
        EXPECTED: User navigated to 1-2-Free Splash page and can play Game
        """
        pass
