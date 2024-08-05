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
class Test_C3020316_Verify_successful_login_for_in_shop_MC_user(Common):
    """
    TR_ID: C3020316
    NAME: Verify successful login for in-shop/MC user
    DESCRIPTION: This test case verifies successful login by in-shop user
    DESCRIPTION: Note: cannot automate, test case requires manual steps in IMS.
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed( links to be provided)
    PRECONDITIONS: * User taps/clicks 'log in' button on landing page
    PRECONDITIONS: * SB login pop-up is displayed
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: Expected urls for upgrade journey:
    PRECONDITIONS: login: https://coral-url?targetPage=login&referrerPage=whatever-url
    PRECONDITIONS: signup: https://coral-url?targetPage=signup&referrerPage=whatever-url
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001_log_in_with_in_shop_user_with_their_card_number_and_pin(self):
        """
        DESCRIPTION: 'Log in' with in-shop user with their card number and PIN
        EXPECTED: * All on login pop-ups are hidden (IMS or SalesForce)
        EXPECTED: * Upgrade pop-up is not displayed
        EXPECTED: * Relevant GDPR banner is displayed (WS "Get Player Tags" request 35547)
        EXPECTED: * User is automatically navigated to the upgrade page
        """
        pass

    def test_002_upgrade_in_shop_to_multi_channel_user(self):
        """
        DESCRIPTION: Upgrade in-shop to Multi-channel user
        EXPECTED: User is upgraded
        """
        pass

    def test_003_change_user_password_in_ims(self):
        """
        DESCRIPTION: Change user password in IMS
        EXPECTED: Password is updated
        """
        pass

    def test_004_log_in_with_an_online_or_multi_channel_user_using_the_card_number_and_pin(self):
        """
        DESCRIPTION: 'Log in' with an online or Multi-channel user using the card number and PIN
        EXPECTED: * The default error handing on the login pop-up is displayed
        EXPECTED: * User is able to login with username/password
        """
        pass

    def test_005_log_in_with_multi_channel_user_using_username_and_password(self):
        """
        DESCRIPTION: 'Log in' with Multi-channel user using username and password
        EXPECTED: * All on login pop-ups are hidden (IMS or SalesForce)
        EXPECTED: * User is automatically navigated to the shop tab
        """
        pass
