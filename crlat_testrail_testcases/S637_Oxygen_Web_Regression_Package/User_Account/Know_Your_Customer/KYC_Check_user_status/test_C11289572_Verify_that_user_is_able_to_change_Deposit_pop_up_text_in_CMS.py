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
class Test_C11289572_Verify_that_user_is_able_to_change_Deposit_pop_up_text_in_CMS(Common):
    """
    TR_ID: C11289572
    NAME: Verify that user is able to change 'Deposit' pop-up text in CMS
    DESCRIPTION: This test case verifies ability of user to change text of Deposit popup with success KYC message
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User has finished the registration flow and is auto logged in or has logged in to application as already existing user
    PRECONDITIONS: - User is on Home page and is able to browse the site
    PRECONDITIONS: - User account is under verification (Check for IMS 'age verification result' status = Active Grace period and Player tags = "AGP_Success_Upload < 5 & Verfication_Review")
    PRECONDITIONS: ======
    PRECONDITIONS: - CMS Envs. https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments#LadbrokesEnvironments-CMSEnvironmentsforLadbrokes
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_oxygen_appclick_on_check_status_link_on_account_in_review_info_bar(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: Click on 'Check status' link on 'account in review' info bar
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - When response from IMS is received, user is shown 'Account In Review' overlay
        """
        pass

    def test_002_navigate_to_cms__static_blocks__kyc___deposit_now__change_success_message_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS > STATIC BLOCKS > KYC - DEPOSIT NOW > change Success message and Save Changes
        EXPECTED: Success message successfully changed
        """
        pass

    def test_003_in_ims__change_user_to_age_verification_result_status__under_review_user_passed_verificationin_oxygen_app__click_check_status_link(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - change user to 'age verification result' status = "Under Review" (user passed verification)
        DESCRIPTION: In Oxygen App:
        DESCRIPTION: - click 'Check status' link
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - After response is received the ribbon disappears
        EXPECTED: - 'Deposit' pop-up appears
        EXPECTED: - Text is the same as set in CMS
        """
        pass

    def test_004_navigate_to_cms__change_success_message_to_default_one__save_changes(self):
        """
        DESCRIPTION: Navigate to CMS > change Success message to default one > Save changes
        EXPECTED: Success message successfully changed
        """
        pass
