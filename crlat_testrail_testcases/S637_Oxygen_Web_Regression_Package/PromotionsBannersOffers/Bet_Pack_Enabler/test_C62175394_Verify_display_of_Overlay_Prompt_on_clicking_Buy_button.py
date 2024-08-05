import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.promotions_banners_offers
@vtest
class Test_C62175394_Verify_display_of_Overlay_Prompt_on_clicking_Buy_button(Common):
    """
    TR_ID: C62175394
    NAME: Verify display of Overlay/Prompt on clicking Buy button
    DESCRIPTION: This test case verifies display of Overlay/Prompt when user clicked on Buy Button on Bet Pack promotions page
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    """
    keep_browser_open = True

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to Application
        EXPECTED: User should be Logged in
        """
        pass

    def test_002_navigate_to_promotions_page_from_sports_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Ribbon' or 'Left Navigation' menu
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_003_navigate_to_configured_promotion_with_bet_pack_by_clicking_see_more_cta(self):
        """
        DESCRIPTION: Navigate to configured Promotion with Bet Pack by clicking 'See More' CTA
        EXPECTED: Bet Pack Promotion page is opened
        """
        pass

    def test_004_verify_bet_pack_details_and_buy_button_in_bet_pack_promotion_page(self):
        """
        DESCRIPTION: Verify Bet Pack details and 'Buy Button' in Bet Pack promotion page
        EXPECTED: Bet Pack details and 'Buy Button' should be displayed as per the CMS configurations
        EXPECTED: ![](index.php?/attachments/get/161454691)
        """
        pass

    def test_005_click_on_buy_button(self):
        """
        DESCRIPTION: Click on 'Buy Button'
        EXPECTED: Buy Button should be clickable and Buy Button overlay should be displayed
        """
        pass

    def test_006_verify_content_on_the_overlay(self):
        """
        DESCRIPTION: Verify content on the overlay
        EXPECTED: It should display with below fields
        EXPECTED: * Overlay Header (Bet Pack)- Hard coded
        EXPECTED: * Description Content (It should be as per CMS config from Text field)
        EXPECTED: * Exit CTA - Hard coded
        EXPECTED: * Confirm CTA - Hard coded
        EXPECTED: ![](index.php?/attachments/get/161454692)
        """
        pass
