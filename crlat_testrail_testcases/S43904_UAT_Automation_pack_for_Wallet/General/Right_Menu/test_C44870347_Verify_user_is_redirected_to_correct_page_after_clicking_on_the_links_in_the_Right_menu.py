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
class Test_C44870347_Verify_user_is_redirected_to_correct_page_after_clicking_on_the_links_in_the_Right_menu(Common):
    """
    TR_ID: C44870347
    NAME: Verify user is redirected to correct page after clicking on the links in the Right menu.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_click_on_the_avatar_and_click_on_deposit_button_verify(self):
        """
        DESCRIPTION: Click on the Avatar and click on Deposit button. Verify.
        EXPECTED: User is navigated to the deposit page.
        """
        pass

    def test_002_click_on_all_of_the_below_links_and_verify_1_banking_consisting_of_my_balance_deposit_withdraw2_offers__free_bets_consisting_of_sports_free_bets_sports_promotions_gaming_promotios_voucher_codes3_history_consisting_of_betting_history_transaction_history__payment_history4_messages5_connect_consisting_of_shop_exclusive_promos_shop_bet_tracker_football_bet_filter__shop_locator6_settings_consisting_of_my_account_details_change_password_marketing_preferences__betting_settings7_gambling_controls_consisting_of_spending_controls_time_management__account_closurereopening8_help__contact9_log_out(self):
        """
        DESCRIPTION: Click on all of the below links and verify:-
        DESCRIPTION: 1. Banking consisting of My Balance, Deposit, Withdraw
        DESCRIPTION: 2. Offers & Free bets consisting of Sports free bets, Sports promotions, Gaming promotios, Voucher codes
        DESCRIPTION: 3. History consisting of Betting History, Transaction History & Payment History.
        DESCRIPTION: 4. Messages
        DESCRIPTION: 5. Connect consisting of Shop exclusive promos, shop bet tracker, football bet filter & shop locator
        DESCRIPTION: 6. Settings consisting of My account details, change password, marketing preferences & betting settings.
        DESCRIPTION: 7. Gambling controls consisting of Spending Controls, Time management & Account closure/reopening.
        DESCRIPTION: 8. Help & Contact.
        DESCRIPTION: 9. Log out.
        EXPECTED: User is navigated to the corresponding pages.
        """
        pass
