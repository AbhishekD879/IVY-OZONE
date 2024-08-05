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
class Test_C3009118_Verify_Login_pop_up_for_the_user_from_Roulette_LP(Common):
    """
    TR_ID: C3009118
    NAME: Verify Login pop-up for the user from Roulette LP
    DESCRIPTION: This test case verifies Login pop-up for the user came from Roulette landing page
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed( links to be provided)
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: Expected urls for upgrade journey:
    PRECONDITIONS: login: https://coral-url?targetPage=login&referrerPage=whatever-url
    PRECONDITIONS: signup: https://coral-url?targetPage=signup&referrerPage=whatever-url
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001_tap_login_button(self):
        """
        DESCRIPTION: Tap 'Login' button
        EXPECTED: * Sportsbook login pop-up is displayed
        EXPECTED: * On the background the user is automatically navigated to the Sportsbook home page
        EXPECTED: * Any first install tutorial is not displayed
        """
        pass

    def test_002_verify_forgot_passwordusername(self):
        """
        DESCRIPTION: Verify 'Forgot password/username'
        EXPECTED: * Forgot password/username links navigate to appropriate pages
        EXPECTED: * Roulette journey is interrupted
        """
        pass

    def test_003_verify_checkboxes(self):
        """
        DESCRIPTION: Verify Checkboxes
        EXPECTED: Checkboxes can be checked/unchecked
        """
        pass

    def test_004_verify_showhide_functionality(self):
        """
        DESCRIPTION: Verify 'Show/Hide' functionality
        EXPECTED: 'Show/Hide' functionality works properly
        """
        pass

    def test_005_verify_successful_logging(self):
        """
        DESCRIPTION: Verify successful logging
        EXPECTED: User is able to log in with valid credentials
        """
        pass

    def test_006_verify_unsuccessful_logging(self):
        """
        DESCRIPTION: Verify unsuccessful logging
        EXPECTED: Error handling is present for invalid credentials
        """
        pass

    def test_007_verify_join_button(self):
        """
        DESCRIPTION: Verify 'Join' button
        EXPECTED: * 'Join' button navigate to SB Registration page
        EXPECTED: * Roulette journey is preserved
        """
        pass

    def test_008_verify_live_chat(self):
        """
        DESCRIPTION: Verify Live Chat
        EXPECTED: * Chat link navigates to the live chat
        EXPECTED: * Roulette journey is interrupted
        """
        pass

    def test_009_verify_login_pop_up_closing(self):
        """
        DESCRIPTION: Verify login pop-up closing
        EXPECTED: * Pop-up is closed by 'Close' button
        EXPECTED: * User is navigated back to 'referrerPage' preconfigured within LP 'LOGIN' url
        """
        pass
