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
class Test_C62184308_Verify_Bet_Pack_amount_is_debited_from_user_balance_when_Bet_Pack_is_created_successfully(Common):
    """
    TR_ID: C62184308
    NAME: Verify Bet Pack amount is debited from user balance when Bet Pack is created successfully
    DESCRIPTION: This test case verifies the Bet Pack amount is debited from user balance when Bet Pack is created successfully
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 3: User should be Logged in with sufficient balance to buy Bet Pack and should be in Promotions page
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

    def test_004_verify_bet_pack_amount_is_debited_in_user_balance(self):
        """
        DESCRIPTION: Verify Bet Pack amount is debited in user balance
        EXPECTED: Bet Pack amount should be debited from the user balance
        """
        pass
