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
class Test_C11899310_Verify_that_Recently_Played_Games_are_restricted_for_users_with_accounts_in_review(Common):
    """
    TR_ID: C11899310
    NAME: Verify that Recently Played Games are restricted for users with accounts in review
    DESCRIPTION: This test case verifies restricting a user, whose account is in review, from playing Recently Played Games in Sports app.
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. Oxygen app is loaded
    PRECONDITIONS: 3. User is registered
    PRECONDITIONS: 4. In IMS:
    PRECONDITIONS: - 'Age verification result' is set to 'Active Grace Period' (in 'General Player Information' section) for a user
    PRECONDITIONS: - Next Player Tags added "AGP_Success_Upload < 5 & "Verification_Review" for a user
    PRECONDITIONS: 5. Recently Played Games module is active and configured in CMS: Sports Pages > Homepage > Recently Played Games
    PRECONDITIONS: 6. User has has played games in Gaming lobby (https://gaming.coral.co.uk/) OR:
    PRECONDITIONS: 6.1. in order to simulate that user have played games you may enter following script into browser's console:
    PRECONDITIONS: window.xbcAPI.imsAPI.webSocket.send(JSON.stringify({'ID':89603,'description':'Add game to recent','responses':[89604],'game':{'code':'ro_g'},'deviceType':'other','osName':'macintosh','osVersion’:’x’,’deliveryPlatform':'html5','deviceBrowser':'chrome','clientType':'casino','correlationId': Date.now()}));
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - Playtech IMS Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_login_with_a_user_from_preconditions_steps_4__5(self):
        """
        DESCRIPTION: Login with a user from Preconditions steps 4 & 5
        EXPECTED: - User is logged in
        EXPECTED: - Review ribbon bar is present
        """
        pass

    def test_002_tap_on_some_game_thumbnail_in_recently_played_games(self):
        """
        DESCRIPTION: Tap on some game thumbnail in Recently Played Games
        EXPECTED: 'Account in Review' overlay is displayed
        """
        pass
