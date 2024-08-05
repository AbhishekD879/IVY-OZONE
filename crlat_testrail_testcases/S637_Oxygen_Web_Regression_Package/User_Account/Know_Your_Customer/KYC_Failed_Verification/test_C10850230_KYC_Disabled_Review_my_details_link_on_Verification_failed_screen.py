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
class Test_C10850230_KYC_Disabled_Review_my_details_link_on_Verification_failed_screen(Common):
    """
    TR_ID: C10850230
    NAME: KYC. Disabled Review my details link on Verification failed screen
    DESCRIPTION: Test case verifies Review My Details link is disabled if user has made 3 attempts to edit his details before
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab. In WS Active Grace Period = “inprocess”
    PRECONDITIONS: **User IMS status = Active Grace Period and Player tags are** AGP_Success_Upload < 5 or POA_Required and AGP_Success_Upload < 5
    PRECONDITIONS: .
    PRECONDITIONS: **Application local storage contains variable with number of edit attempts = 3**
    """
    keep_browser_open = True

    def test_001_login_as_a_user_from_pre_conditions_who_had_edited_his_details_3_times(self):
        """
        DESCRIPTION: Login as a user from pre-conditions who had edited his details 3 times
        EXPECTED: Verification failed overlay is shown
        """
        pass

    def test_002_verify_review_my_details_link(self):
        """
        DESCRIPTION: Verify Review My Details link
        EXPECTED: Review My Details link is disabled
        EXPECTED: Message 'You can review your details no more than 3 times'
        """
        pass
