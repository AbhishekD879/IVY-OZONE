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
class Test_C12587653_Verify_that_navigation_via_Super_button_is_restricted_for_users_with_accounts_in_review(Common):
    """
    TR_ID: C12587653
    NAME: Verify that navigation via 'Super' button is restricted for users with accounts in review
    DESCRIPTION: This test case verifies restricting a user, whose account is in review, to be navigated to any external/internal url via Super button
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. Oxygen app is loaded
    PRECONDITIONS: 3. User is registered
    PRECONDITIONS: 4. In IMS:
    PRECONDITIONS: - 'Age verification result' is set to 'Active Grace Period' (in 'General Player Information' section) for a user
    PRECONDITIONS: - Next Player Tags added "AGP_Success_Upload < 5 & "Verification_Review" for a user
    PRECONDITIONS: 5. Super Button should be added and configured in CMS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: (for Ladbrokes: CMS > Sports Pages > SUPER BUTTONS)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - Playtech IMS Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    """
    keep_browser_open = True

    def test_001_login_with_a_user_from_preconditions_steps_4__5(self):
        """
        DESCRIPTION: Login with a user from Preconditions steps 4 & 5
        EXPECTED: - User is logged in
        EXPECTED: - Review ribbon bar is present
        """
        pass

    def test_002_tap_on_super_button(self):
        """
        DESCRIPTION: Tap on 'Super' button
        EXPECTED: - 'Account in Review' overlay is displayed
        EXPECTED: - User is NOT redirected to external/internal urls
        """
        pass

    def test_003_close_account_in_review_overlay(self):
        """
        DESCRIPTION: Close 'Account in Review' overlay
        EXPECTED: 'Account in Review' overlay is closed
        """
        pass
