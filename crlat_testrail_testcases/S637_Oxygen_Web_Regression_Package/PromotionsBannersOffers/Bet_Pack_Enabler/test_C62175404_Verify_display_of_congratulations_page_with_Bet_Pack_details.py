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
class Test_C62175404_Verify_display_of_congratulations_page_with_Bet_Pack_details(Common):
    """
    TR_ID: C62175404
    NAME: Verify  display of congratulations page  with 'Bet Pack' details.
    DESCRIPTION: This test case verifies display of congratulations page with 'Bet Pack' details as per the CMS, when user clicks on confirm button with sufficient balance
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS
    PRECONDITIONS: 2: Make sure Congrats message is configured in Bet Pack promotion page in CMS
    PRECONDITIONS: 3: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 4: User should be Logged in with sufficient balance to buy Bet Pack and should be in Promotions page
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
        EXPECTED: Congrats message should be displayed to the user
        """
        pass

    def test_004_verify_the_content_in_congratulations_page(self):
        """
        DESCRIPTION: Verify the content in Congratulations page
        EXPECTED: Content displayed in Congratulations page with Bet Pack details should be as per the configurations in CMS
        """
        pass
