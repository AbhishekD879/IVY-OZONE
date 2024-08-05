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
class Test_C62175386_Verify_display_of_Bet_Pack_details_and_Buy_Button_as_per_configuration_set_in_CMS(Common):
    """
    TR_ID: C62175386
    NAME: Verify display of Bet Pack details and Buy Button as per configuration set in CMS
    DESCRIPTION: This test case verifies display of Bet Pack details and Buy Button as per configuration in promotions page in CMS
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

    def test_003_check_promotions_in_landing_page(self):
        """
        DESCRIPTION: Check 'Promotions' in landing page
        EXPECTED: Bet Pack Enabler button is NOT displayed on 'Promotions' landing page
        """
        pass

    def test_004_navigate_to_configured_promotion_with_bet_pack_by_clicking_see_more_cta(self):
        """
        DESCRIPTION: Navigate to configured Promotion with 'Bet Pack' by clicking 'See More' CTA
        EXPECTED: Bet Pack Enabler Promotion page is opened
        """
        pass

    def test_005_verify_bet_pack_details_and_buy_button(self):
        """
        DESCRIPTION: Verify Bet Pack details and 'Buy Button'
        EXPECTED: Bet Pack details and 'Buy Button' should be displayed as per the CMS configurations
        EXPECTED: ![](index.php?/attachments/get/161454691)
        """
        pass

    def test_006_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User should be Logged out
        """
        pass

    def test_007_repeat_steps_2_5_with_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps 2-5 with Logged out user
        EXPECTED: 
        """
        pass
