import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C10841489_Verify_user_after_pending_verification_KYC_is_redirected_to_Failed_Flow_after_login(Common):
    """
    TR_ID: C10841489
    NAME: Verify user after pending verification KYC is redirected to Failed Flow after login
    DESCRIPTION: This test case validates existing user redirection to Failed Flow after login with AVR 'unknown'
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User is NOT logged in
    PRECONDITIONS: - User's Age Verification Result = Unknown
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: __________
    PRECONDITIONS: Ladbrokes Account One:
    PRECONDITIONS: * Stage Navigation URL - https://accountone-stg.ladbrokes.com/entry-point
    PRECONDITIONS: * Prod Navigation URL - https://accountone.ladbrokes.com/entry-point
    """
    keep_browser_open = True

    def test_001_login_to_app(self):
        """
        DESCRIPTION: Login to app
        EXPECTED: - Verification spinner displayed for 5-7seconds (CMS configurable)
        EXPECTED: **Coral:**
        EXPECTED: User is redirected to KYC Failed Flow (documents upload page)
        EXPECTED: **Ladbrokes:**
        EXPECTED: User is redirected to Account one page
        """
        pass
