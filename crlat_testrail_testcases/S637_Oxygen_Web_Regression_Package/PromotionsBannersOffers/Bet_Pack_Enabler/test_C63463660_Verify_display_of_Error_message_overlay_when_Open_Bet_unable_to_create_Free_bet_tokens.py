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
class Test_C63463660_Verify_display_of_Error_message_overlay_when_Open_Bet_unable_to_create_Free_bet_tokens(Common):
    """
    TR_ID: C63463660
    NAME: Verify display of Error message overlay when Open Bet unable to create Free bet tokens
    DESCRIPTION: This test case verifies display of Error message overlay in Bet Pack promotion page when Open Bet unable to create Free bet tokens
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 3: Make sure Invalid values is enter in Trigger ID or Values field
    PRECONDITIONS: 4: User should be Logged in and should be in Promotions page
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
        EXPECTED: * Message which is configured in Error message field in CMS should be displayed to the user
        EXPECTED: * User should remain in the Bet Pack Promotion page
        EXPECTED: * Congratulations message should not be displayed to the user
        """
        pass
