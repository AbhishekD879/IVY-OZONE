import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.promotions_banners_offers
@vtest
class Test_C62175401_Verify_the_network_call_is_triggered_to_Open_bet_when_user_clicks_on_confirm_button(Common):
    """
    TR_ID: C62175401
    NAME: Verify the network call is triggered to Open bet when user clicks on confirm button
    DESCRIPTION: This test case verifies network call is triggered to Open bet when user clicks on confirm button
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 3. User should be Logged in and should be in Promotions page
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
        DESCRIPTION: Click on 'Buy Button'
        EXPECTED: It should display with below fields
        EXPECTED: * Overlay Header (Bet Pack)- Hard coded
        EXPECTED: * Description Content (It should be as per CMS config from Text field)
        EXPECTED: * Exit CTA - Hard coded
        EXPECTED: * Confirm CTA - Hard coded
        EXPECTED: ![](index.php?/attachments/get/161454692)
        """
        pass

    def test_003_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on Confirm button
        EXPECTED: Confirm Button should be clickable
        """
        pass

    def test_004_verify_network_call_is_triggered_to_open_bet(self):
        """
        DESCRIPTION: Verify Network call is triggered to Open Bet
        EXPECTED: Below bpp call should be triggered to Open Bet in order to create Free bet tokens
        EXPECTED: ![](index.php?/attachments/get/2e5442dd-4ff0-4cd2-9cc6-b934e07734aa)
        """
        pass
