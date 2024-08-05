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
class Test_C10850231_KYC_Log_out_and_re_login_before_documents_upload(Common):
    """
    TR_ID: C10850231
    NAME: KYC. Log out and re-login before documents upload
    DESCRIPTION: Test case verifies logging out on "Verification failed" screen and re-login, login with different user
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab. In WS Active Grace Period = “inprocess”
    PRECONDITIONS: References
    PRECONDITIONS: IMS status = Active Grace Period:
    PRECONDITIONS: Verification needed overlay when Player tags are POA_Required and  AGP_Success_Upload < 5 - [TC 10850078][1]
    PRECONDITIONS: Verification needed overlay when Player tag = AGP_Success_Upload < 5 - [TC 10850076][2]
    PRECONDITIONS: IMS status = "unknown" or not received - [TC 10841421][3] [TC 0841422][4]
    PRECONDITIONS: IMS status = "review" [TC 10843716][5]
    PRECONDITIONS: **User IMS status = Active Grace Period and Player tags are** (AGP_Success_Upload < 5) OR (POA_Required AND AGP_Success_Upload < 5) OR (POA_Required) **User is on Verification failed screen**
    PRECONDITIONS: [1]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10850078
    PRECONDITIONS: [2]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10850076
    PRECONDITIONS: [3]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10841421
    PRECONDITIONS: [4]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10841422
    PRECONDITIONS: [5]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10843716
    """
    keep_browser_open = True

    def test_001_tap_on_log_out_button_on_verification_failed_overlay(self):
        """
        DESCRIPTION: Tap on Log out button on Verification failed overlay
        EXPECTED: User is logged out, "Verification failed" overlay is hidden
        """
        pass

    def test_002_re_login_with_the_same_user(self):
        """
        DESCRIPTION: Re-login with the same user
        EXPECTED: Assuming there was no changes on IMS, Verification failed screen is displayed
        """
        pass

    def test_003_log_out_and_login_with_different_user(self):
        """
        DESCRIPTION: Log out and login with different user
        EXPECTED: User sees relevant screen based on his IMS status and tags (see references in pre-conditions)
        """
        pass
