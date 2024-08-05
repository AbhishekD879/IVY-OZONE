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
class Test_C3019574_Verify_Login_exit_scenarios(Common):
    """
    TR_ID: C3019574
    NAME: Verify Login exit scenarios
    DESCRIPTION: This test case verifies Login pop-up for the user came from Roulette landing page
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001__tap_login_button_go_to_the_local_storage_and_check_attribute_for_roulette_users__oxroulettejourney(self):
        """
        DESCRIPTION: * Tap 'Login' button
        DESCRIPTION: * Go to the Local storage and check attribute for Roulette users = 'OX.rouletteJourney'
        EXPECTED: * Sportsbook login pop-up is displayed
        EXPECTED: * On the background the user is automatically navigated to the Sportsbook home page
        EXPECTED: * Any first install tutorial is not displayed
        EXPECTED: * LocalStorage attribute = 'OX.rouletteJourney' is available
        """
        pass

    def test_002_tap_on_the_space_outside_of_the_pop_up(self):
        """
        DESCRIPTION: Tap on the space outside of the pop-up
        EXPECTED: * The space outside of the pop-up is unresponsive
        EXPECTED: * Pop-up isn't close
        """
        pass

    def test_003_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: The In-shop user is redirected back to the landing page
        EXPECTED: (http://promotions.coral.co.uk/lp/shop-games/)
        EXPECTED: Any page can be setup in referrerPage=whatever-url attribute
        """
        pass

    def test_004_repeat_step_1(self):
        """
        DESCRIPTION: Repeat Step 1
        EXPECTED: 
        """
        pass

    def test_005__tap_forgot_passwordusername_go_to_the_local_storage_and_check_attribute_for_roulette_users__oxroulettejourney(self):
        """
        DESCRIPTION: * Tap 'Forgot password/username'
        DESCRIPTION: * Go to the Local storage and check attribute for Roulette users = 'OX.rouletteJourney'
        EXPECTED: * Forgot password/username links navigate to appropriate pages in Sportsbook
        EXPECTED: * Attribute is absent
        """
        pass

    def test_006__tap_sb_login_button_tap_x_button(self):
        """
        DESCRIPTION: * Tap SB 'Login' button
        DESCRIPTION: * Tap 'X' button
        EXPECTED: * Sportsbook login pop-up is displayed
        EXPECTED: * Sportsbook login pop-up is closed
        EXPECTED: * User remains on 'Forgot password/username' page
        """
        pass

    def test_007_repeat_step_5_for_live_chat_join_us_here(self):
        """
        DESCRIPTION: Repeat Step 5 for
        DESCRIPTION: * Live Chat
        DESCRIPTION: * 'Join us here'
        EXPECTED: * Links navigate to appropriate pages in Sportsbook
        EXPECTED: * 'OX.rouletteJourney' attribute is absent
        """
        pass
