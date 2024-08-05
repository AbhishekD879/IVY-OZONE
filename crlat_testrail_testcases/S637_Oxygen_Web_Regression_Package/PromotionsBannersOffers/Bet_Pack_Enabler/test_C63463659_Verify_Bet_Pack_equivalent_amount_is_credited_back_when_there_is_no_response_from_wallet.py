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
class Test_C63463659_Verify_Bet_Pack_equivalent_amount_is_credited_back_when_there_is_no_response_from_wallet(Common):
    """
    TR_ID: C63463659
    NAME: Verify Bet Pack equivalent amount is credited back when there is no response from wallet
    DESCRIPTION: This test case verifies Bet Pack equivalent amount is credited back when there is no response from wallet
    PRECONDITIONS: 1: Make sure Bet Pack Promotion with Buy Button is configured within CMS.
    PRECONDITIONS: 2: Make sure Offer with Purchase(Bet Pack) Trigger and Reward as sportsbook Tokens should be created in OB
    PRECONDITIONS: 3: User should be Logged in with sufficient balance to buy Bet Pack
    PRECONDITIONS: Note:
    PRECONDITIONS: Below Time Out Scenarios needs to be tested with below users
    PRECONDITIONS: ![](index.php?/attachments/get/f74fcc90-3483-44e0-a4bf-4fdfb344f880)
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

    def test_003_click_on_confirm_buttonat_the_same_time_trigger_time_out_or_network_errors_from_wallet(self):
        """
        DESCRIPTION: Click on Confirm button
        DESCRIPTION: At the same time trigger Time out or Network Errors from wallet
        EXPECTED: * Message which is configured in Error message field in CMS should be displayed to the user
        EXPECTED: * User should remain in the Bet Pack Promotion page
        EXPECTED: * Congratulations message should not be displayed to the user
        EXPECTED: * Bet Pack amount should be debited from the user balance
        """
        pass

    def test_004_verify_credit_in_user_balance(self):
        """
        DESCRIPTION: Verify credit in user balance
        EXPECTED: Bet Pack amount should be credited back to the user balance
        """
        pass

    def test_005_click_on_history__gt_transactions_history(self):
        """
        DESCRIPTION: Click on History -&gt; Transactions History
        EXPECTED: User should be navigated to Transactions History page
        """
        pass

    def test_006_verify_the_transaction_details_of_unsuccessful_bet_pack(self):
        """
        DESCRIPTION: Verify the transaction details of unsuccessful Bet Pack
        EXPECTED: Transaction history page should be displayed with debited and credited Bet Pack amount details
        """
        pass
