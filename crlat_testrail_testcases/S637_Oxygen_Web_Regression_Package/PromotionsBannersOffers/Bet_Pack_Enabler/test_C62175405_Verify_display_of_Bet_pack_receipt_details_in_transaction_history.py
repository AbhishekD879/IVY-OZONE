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
class Test_C62175405_Verify_display_of_Bet_pack_receipt_details_in_transaction_history(Common):
    """
    TR_ID: C62175405
    NAME: Verify display of Bet pack receipt details in transaction history
    DESCRIPTION: This test case verifies display of Bet pack receipt details in transaction history
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 3: User should be Logged in with sufficient balance to buy Bet Pack and should be in Promotions page
    PRECONDITIONS: 4: User should not have purchase history of a Bet Pack in last 24 hrs.
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
        EXPECTED: Congrats messages should be displayed to the user
        """
        pass

    def test_004_click_on_avataruser_account(self):
        """
        DESCRIPTION: Click on Avatar/User account
        EXPECTED: User/Right menu should be opened
        """
        pass

    def test_005_click_on_history__gt_transactions_history(self):
        """
        DESCRIPTION: Click on History -&gt; Transactions History
        EXPECTED: User should be navigated to Transactions History page
        """
        pass

    def test_006_verify_the_bet_pack_purchase_details(self):
        """
        DESCRIPTION: Verify the Bet Pack purchase details
        EXPECTED: User should be displayed with the Bet Pack purchase details in the transactions history page
        """
        pass
