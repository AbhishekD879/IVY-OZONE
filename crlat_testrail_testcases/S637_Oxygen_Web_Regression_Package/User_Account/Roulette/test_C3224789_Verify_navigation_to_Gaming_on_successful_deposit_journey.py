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
class Test_C3224789_Verify_navigation_to_Gaming_on_successful_deposit_journey(Common):
    """
    TR_ID: C3224789
    NAME: Verify navigation to Gaming on successful deposit journey
    DESCRIPTION: This test case verifies navigation to Gaming on successful deposit journey
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked / timeToRedirect = 2 sec
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * CMS 'timeToRedirect' is 2 sec by default
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed( links to be provided)
    PRECONDITIONS: * C3019617 is completed
    PRECONDITIONS: * User is on Deposit page, My payments tab
    PRECONDITIONS: * Credit card is successfully added
    PRECONDITIONS: * Relevant GDPR policy banner is displayed (WS "Get Player Tags" request 35547)
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: Expected urls for upgrade journey:
    PRECONDITIONS: login: https://coral-url?targetPage=login&referrerPage=whatever-url
    PRECONDITIONS: signup: https://coral-url?targetPage=signup&referrerPage=whatever-url
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001__enter_valid_amount_enter_cvvcv2_tap_deposit(self):
        """
        DESCRIPTION: * Enter valid amount
        DESCRIPTION: * Enter CVV/CV2
        DESCRIPTION: * Tap deposit
        EXPECTED: * Deposit button is disabled before the end of depositing operation
        EXPECTED: * 'Protection of Funds' pop-up is displayed for initial deposit (WS response 33014)
        """
        pass

    def test_002__tap_accept_on_protection_of_funds_pop_up(self):
        """
        DESCRIPTION: * Tap 'Accept' on 'Protection of Funds' pop-up
        EXPECTED: * Success deposit pop-up is displayed (WS response 31133)
        """
        pass

    def test_003__close_the_success_deposit_pop_up_verify_navigation_to_gaming_on_successful_deposit(self):
        """
        DESCRIPTION: * Close the Success deposit pop-up
        DESCRIPTION: * Verify navigation to Gaming on successful deposit
        EXPECTED: * Successful message: **"Your deposit of <currency symbol> XX.XX was successful is shown for 2sec
        EXPECTED: * User balance is updated accordingly
        EXPECTED: * **User is redirected to the shop tab within Gaming**
        """
        pass

    def test_004_change_the_cms_config_for_timetoredirect_to_10sec(self):
        """
        DESCRIPTION: Change the CMS config for 'timeToRedirect' to 10sec
        EXPECTED: Config is successfully changed
        """
        pass

    def test_005_repeat_steps_1_3(self):
        """
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: * Successful message: **"Your deposit of <currency symbol> XX.XX was successful is shown for 10sec
        EXPECTED: * **User is redirected to the shop tab within Gaming**
        """
        pass
