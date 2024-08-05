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
class Test_C3020330_Verify_TnC_pop_up_for_the_in_shop_user(Common):
    """
    TR_ID: C3020330
    NAME: Verify TnC pop-up for the in-shop user
    DESCRIPTION: This test case verifies TnC pop-up for the in-shop user
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed( links to be provided)
    PRECONDITIONS: * TnC is not accepted by the user on registration journey
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: Expected urls for upgrade journey:
    PRECONDITIONS: login: https://coral-url?targetPage=login&referrerPage=whatever-url
    PRECONDITIONS: signup: https://coral-url?targetPage=signup&referrerPage=whatever-url
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

    def test_002_log_in_with_in_shop_user_with_their_card_number_and_pin(self):
        """
        DESCRIPTION: 'Log in' with in-shop user with their card number and PIN
        EXPECTED: * TnC pop-up is displayed
        EXPECTED: * Login pop-up is closed
        EXPECTED: * Upgrade pop-up is not displayed
        """
        pass

    def test_003_decline_the_tnc(self):
        """
        DESCRIPTION: Decline the TnC
        EXPECTED: * Login pop-up is displayed again remaining in SB
        EXPECTED: * User is not logged in
        """
        pass

    def test_004_log_in_with_in_shop_user_with_their_card_number_and_pin(self):
        """
        DESCRIPTION: 'Log in' with in-shop user with their card number and PIN
        EXPECTED: * TnC pop-up is displayed
        """
        pass

    def test_005_accepts_the_tnc(self):
        """
        DESCRIPTION: Accepts the TnC
        EXPECTED: * User is logged in
        EXPECTED: * User is automatically navigated to the upgrade page
        """
        pass
