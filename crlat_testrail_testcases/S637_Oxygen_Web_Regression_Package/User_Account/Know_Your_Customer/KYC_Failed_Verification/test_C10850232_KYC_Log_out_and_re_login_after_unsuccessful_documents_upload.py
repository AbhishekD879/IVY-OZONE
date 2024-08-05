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
class Test_C10850232_KYC_Log_out_and_re_login_after_unsuccessful_documents_upload(Common):
    """
    TR_ID: C10850232
    NAME: KYC. Log out and re-login after unsuccessful documents upload
    DESCRIPTION: Test case verifies logging out (and re-login, login with different user) after unsuccessful documents upload
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab. In WS Active Grace Period = “inprocess”
    PRECONDITIONS: References
    PRECONDITIONS: IMS status = Active Grace Period:
    PRECONDITIONS: Verification needed overlay when Player tags  POA_Required & AGP_Success_Upload < 5 - [TC 10850078][1]
    PRECONDITIONS: Verification needed overlay when Player tag  AGP_Success_Upload < 5 - [TC 10850076][2]
    PRECONDITIONS: IMS status = "unknown" or not received - [TC 10841421][3] [TC 0841422][4]
    PRECONDITIONS: IMS status = "review" [TC 10843716][5]
    PRECONDITIONS: **User IMS status = Active Grace Period and Player tags** (AGP_Success_Upload < 5) OR (POA_Required AND AGP_Success_Upload < 5) OR (POA_Required) **User is sees overlay with Try again button a result of failure of documents upload to Jumio**
    PRECONDITIONS: [1]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10850078
    PRECONDITIONS: [2]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10850076
    PRECONDITIONS: [3]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10841421
    PRECONDITIONS: [4]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10841422
    PRECONDITIONS: [5]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10843716
    """
    keep_browser_open = True

    def test_001_tap_on_log_out_button_on_overlay_with_try_again_button(self):
        """
        DESCRIPTION: Tap on Log out button on overlay with Try Again button
        EXPECTED: User is logged out, overlay is hidden
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
