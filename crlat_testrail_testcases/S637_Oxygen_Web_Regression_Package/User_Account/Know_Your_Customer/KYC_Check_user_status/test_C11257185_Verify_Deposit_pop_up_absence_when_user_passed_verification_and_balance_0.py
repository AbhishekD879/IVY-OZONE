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
class Test_C11257185_Verify_Deposit_pop_up_absence_when_user_passed_verification_and_balance_0(Common):
    """
    TR_ID: C11257185
    NAME: Verify 'Deposit' pop-up absence when user passed verification and  balance > 0
    DESCRIPTION: This test case verifies that 'Deposit' pop-up is absent after 'Account In Review' info bar when user passed verification and has balance > 0
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User has finished the registration flow and is auto logged in or has logged in to application as already existing one
    PRECONDITIONS: - User's balance is > 0.
    PRECONDITIONS: - User is on Home page and is able to browse the site
    PRECONDITIONS: - User account is under verification (Check for IMS 'age verification result' status = "Active Grace period" and Player tags = "AGP_Success_Upload" with 'Tag value' <=5   & "Verfication_Review")
    PRECONDITIONS: -  'account in review' info bar is present
    PRECONDITIONS: Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_ims__find_a_user__change_age_verification_result_to_under_review__tap_update_info(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a user
        DESCRIPTION: - Change 'Age Verification result' to 'under review'
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_002_in_apptap_check_status_on_account_in_review_bar(self):
        """
        DESCRIPTION: In app:
        DESCRIPTION: Tap 'Check Status' on 'account in review' bar
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - ageVerificationStatus' = "review" is received (in response with "ID":31083)
        EXPECTED: - 'account in review' bar disappears
        EXPECTED: - 'Deposit' pop-up does NOT appear
        """
        pass
