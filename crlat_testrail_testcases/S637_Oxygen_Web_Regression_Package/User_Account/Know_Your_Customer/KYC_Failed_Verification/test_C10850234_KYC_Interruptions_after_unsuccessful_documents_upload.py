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
class Test_C10850234_KYC_Interruptions_after_unsuccessful_documents_upload(Common):
    """
    TR_ID: C10850234
    NAME: KYC. Interruptions after unsuccessful documents upload
    DESCRIPTION: Test case verifies the behavior if app was interrupted after unsuccessful documents upload
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
    PRECONDITIONS: **User IMS status = Active Grace Period and Player tag** (AGP_Success_Upload < 5) OR (POA_Required AND AGP_Success_Upload < 5) OR (POA_Required) **Upload of documents to Jumio has been failed - user sees overlay with Try again button**
    PRECONDITIONS: [1]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10850078
    PRECONDITIONS: [2]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10850076
    PRECONDITIONS: [3]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10841421
    PRECONDITIONS: [4]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10841422
    PRECONDITIONS: [5]: https://ladbrokescoral.testrail.com/index.php?/cases/view/10843716
    """
    keep_browser_open = True

    def test_001_switch_internet_off_and_tap_on_try_again_button(self):
        """
        DESCRIPTION: Switch internet off and tap on TRY AGAIN button
        EXPECTED: Message about no Internet connection should be displayed
        """
        pass

    def test_002_switch_internet_on(self):
        """
        DESCRIPTION: Switch internet on
        EXPECTED: - No internet connection message disappeared
        EXPECTED: - In network > WS connection with openapi web socket was re-established
        EXPECTED: - Verification Failed screen (with Verify Me or Verify My Address button) is shown
        """
        pass

    def test_003_repeat_pre_conditions_and_refresh_app_on_overlay_with_try_again_button(self):
        """
        DESCRIPTION: Repeat pre-conditions and refresh app on overlay with Try again button
        EXPECTED: Assuming there was no changes on IMS, Verification failed screen (with Verify Me or Verify My Address button) is displayed
        """
        pass

    def test_004_minimize_and_kill_appre_open_app(self):
        """
        DESCRIPTION: Minimize and kill app.
        DESCRIPTION: Re-open app
        EXPECTED: Assuming there was no changes on IMS, Verification failed screen is displayed
        """
        pass

    def test_005_tap_on_verify_me_or_verify_my_address_button(self):
        """
        DESCRIPTION: Tap on Verify Me (or Verify My Address) button
        EXPECTED: User is redirected to Jumio service
        """
        pass
