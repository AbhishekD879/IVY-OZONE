import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C62175406_Verify_display_of_Not_Logged_In_overlay_in_Bet_Pack_promotion_page(Common):
    """
    TR_ID: C62175406
    NAME: Verify display of Not Logged In overlay in Bet Pack promotion page
    DESCRIPTION: This test case verifies display of Not Logged In overlay in Bet Pack promotion page when user tries to buy the bet pack without logging in
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 3: User should be in Promotions page
    PRECONDITIONS: 4: User should be logged out from the application
    """
    keep_browser_open = True

    def test_001_navigate_to_configured_promotion_with_bet_pack_by_clicking_see_more_cta(self):
        """
        DESCRIPTION: Navigate to configured Promotion with Bet Pack by clicking 'See More' CTA
        EXPECTED: Bet Pack Promotion page is opened and Buy Button should be displayed
        """
        pass

    def test_002_click_on_buy_button(self):
        """
        DESCRIPTION: Click on Buy Button
        EXPECTED: It should display with below fields
        EXPECTED: * Overlay Header (Bet Pack)- Hard coded
        EXPECTED: * Description Content (It should be as per CMS config from Text field)
        EXPECTED: * Info message: Message should be displayed from not logged In field from CMS
        EXPECTED: * Exit CTA - Hard coded
        EXPECTED: * LOGIN CTA - Hard coded
        EXPECTED: ![](index.php?/attachments/get/161758819)
        """
        pass

    def test_003_click_on_login_button(self):
        """
        DESCRIPTION: Click on Login button
        EXPECTED: User should be redirected to login page
        """
        pass

    def test_004_enter_valid_credentials(self):
        """
        DESCRIPTION: Enter valid credentials
        EXPECTED: User should be able to Login to the appilication
        """
        pass

    def test_005_repeat_steps_1_2_and_click_on_exit_button(self):
        """
        DESCRIPTION: Repeat steps 1-2 and click on Exit Button
        EXPECTED: Bet Pack overlay should be closed and user should be in Bet Pack promotion page
        """
        pass
