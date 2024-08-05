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
class Test_C3020336_Verify_upgrade_from_in_shop_to_MC_user(Common):
    """
    TR_ID: C3020336
    NAME: Verify upgrade from in-shop to MC user
    DESCRIPTION: This test case verifies upgrade from in-shop to MC user
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed( links to be provided)
    PRECONDITIONS: * User taps/clicks 'log in' button
    PRECONDITIONS: * SB login pop-up is displayed
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: Expected urls for upgrade journey:
    PRECONDITIONS: login: https://coral-url?targetPage=login&referrerPage=whatever-url
    PRECONDITIONS: signup: https://coral-url?targetPage=signup&referrerPage=whatever-url
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001_log_in_with_in_shop_user_with_their_card_number_and_pin(self):
        """
        DESCRIPTION: 'Log in' with in-shop user with their card number and PIN
        EXPECTED: * All on login pop-ups are hidden (IMS or SalesForce)
        EXPECTED: * Upgrade pop-up is not displayed
        EXPECTED: * User is automatically navigated to the upgrade page
        """
        pass

    def test_002_verify_successful_upgrade_journey(self):
        """
        DESCRIPTION: Verify successful upgrade journey
        EXPECTED: * Auto re-login is performed
        EXPECTED: * Success upgrade pop-up is displayed
        """
        pass

    def test_003_close_success_upgrade_pop_up(self):
        """
        DESCRIPTION: Close success upgrade pop-up
        EXPECTED: User is navigated to deposit page within SB
        """
        pass

    def test_004_add_credit_card(self):
        """
        DESCRIPTION: Add Credit Card
        EXPECTED: Credit card is successfully added
        """
        pass

    def test_005__enter_valid_amount_tap_deposit_verify_user_balance(self):
        """
        DESCRIPTION: * Enter valid amount
        DESCRIPTION: * Tap deposit
        DESCRIPTION: * Verify user Balance
        EXPECTED: * Deposit button is disabled before the end of depositing operation
        EXPECTED: * Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: * User Balance is increased
        EXPECTED: * **User is redirected to the shop tab within Gaming**
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_007_navigate_to_roulette_landing_page(self):
        """
        DESCRIPTION: Navigate to Roulette landing page
        EXPECTED: Roulette landing page is opened
        """
        pass

    def test_008_repeat_steps_1_3_with_another_in_shop_user(self):
        """
        DESCRIPTION: Repeat steps 1-3 with another in-shop user
        EXPECTED: 
        """
        pass

    def test_009_verify_deposit_via_other_payment_methods_paypal_paypalviasafecharge_neteller_skrill_paysafecard(self):
        """
        DESCRIPTION: Verify deposit via other payment methods:
        DESCRIPTION: * PayPal
        DESCRIPTION: * PayPalviaSafeCharge
        DESCRIPTION: * Neteller
        DESCRIPTION: * Skrill
        DESCRIPTION: * Paysafecard
        EXPECTED: * Deposit button is disabled before the end of depositing operation
        EXPECTED: * Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: * User Balance is increased
        EXPECTED: * **User is redirected to the shop tab within Gaming**
        """
        pass

    def test_010_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_011_navigate_to_roulette_landing_page(self):
        """
        DESCRIPTION: Navigate to Roulette landing page
        EXPECTED: Roulette landing page is opened
        """
        pass

    def test_012_repeat_steps_1(self):
        """
        DESCRIPTION: Repeat steps 1
        EXPECTED: 
        """
        pass

    def test_013_exit_upgrade_page_by_clicking_on_the_header_logo_bottom_menu_or_back(self):
        """
        DESCRIPTION: Exit upgrade page by:
        DESCRIPTION: * clicking on the header logo
        DESCRIPTION: * bottom menu or back
        EXPECTED: * User is navigated to previous page
        EXPECTED: * The card/PIN screen is not displayed
        """
        pass
