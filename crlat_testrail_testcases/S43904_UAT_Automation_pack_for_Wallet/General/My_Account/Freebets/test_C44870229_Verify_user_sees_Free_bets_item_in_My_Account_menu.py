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
class Test_C44870229_Verify_user_sees_Free_bets_item_in_My_Account_menu(Common):
    """
    TR_ID: C44870229
    NAME: "Verify user sees  Free bets item in My Account menu"
    DESCRIPTION: "Verify user sees  Free bets item in My Account menu as below
    DESCRIPTION: - Total amount in £ of Free Bets is displayed next to the menu item
    DESCRIPTION: - When item is tapped, customer can see all available tokens listed with Token Name, Token Value, Expiry Date,
    DESCRIPTION: RedemptionValues Tokens are listed in Expiry date order (if the same, prioritise higher value tokens)
    DESCRIPTION: - User can tap on the token to take them to the relative page (use Odds Boost page logic)
    DESCRIPTION: - User can tap on information icon that initiates pop-up that explains what user can use the free bet on
    DESCRIPTION: - Verify user is shown expiry message when free bet expiring within 24 hours,when they log into the app
    DESCRIPTION: Verify user  sees free bets messae on betslip
    DESCRIPTION: "
    PRECONDITIONS: UserName: goldenbuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_launch_beta_application(self):
        """
        DESCRIPTION: Launch BETA application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_login_with_freebets_available_user(self):
        """
        DESCRIPTION: Login with freebets available user
        EXPECTED: user is logged in
        """
        pass

    def test_003_verify_user_sees__total_free_bets_amount_in_my_account(self):
        """
        DESCRIPTION: Verify user sees  total Free bets amount in My Account
        EXPECTED: Freebet xx.xx is displayed on My Account
        """
        pass

    def test_004_tap_on_my_account_and_verify_user_sees_free_bets_item_in_my_account_menu(self):
        """
        DESCRIPTION: Tap on My Account and Verify user sees Free bets item in My Account menu
        EXPECTED: My Account menu is opened and free bet item is displayed
        """
        pass

    def test_005_verify_total_amount_in__of_free_bets_is_displayed_next_to_the_menu_item(self):
        """
        DESCRIPTION: Verify Total amount in £ of Free Bets is displayed next to the menu item
        EXPECTED: Total Amount is displayed
        EXPECTED: ![](index.php?/attachments/get/49920193)
        """
        pass

    def test_006_verify_when_item_is_tapped_customer_can_see_all_available_tokens_listed_with_token_name_token_value_expiry_date_redemption_values_tokens_are_listed_in_expiry_date_order_if_the_same_prioritise_higher_value_tokens(self):
        """
        DESCRIPTION: Verify When item is tapped, customer can see all available tokens listed with Token Name, Token Value, Expiry Date, Redemption Values Tokens are listed in Expiry date order (if the same, prioritise higher value tokens)
        EXPECTED: Free bets details are displayed
        """
        pass

    def test_007_verify__user_can_tap_on_the_token_to_take_them_to_the_relative_page_use_odds_boost_page_logic(self):
        """
        DESCRIPTION: Verify  User can tap on the token to take them to the relative page (use Odds Boost page logic)
        EXPECTED: Odds boost page opened
        """
        pass

    def test_008_verify__user_can_tap_on_information_icon_that_initiates_pop_up_that_explains_what_user_can_use_the_free_bet_on(self):
        """
        DESCRIPTION: verify  User can tap on information icon that initiates pop-up that explains what user can use the free bet on
        EXPECTED: Information pop up is displayed
        """
        pass

    def test_009_verify_user_sees_free_bets_message_on_betslip(self):
        """
        DESCRIPTION: Verify user sees free bets message on betslip
        EXPECTED: Free bet available message is displayed
        """
        pass

    def test_010_verify_user_is_shown_expiry_message_when_free_bet_expiring_within_24_hourswhen_they_log_into_the_app(self):
        """
        DESCRIPTION: Verify user is shown expiry message when free bet expiring within 24 hours,when they log into the app
        EXPECTED: Message appear on top of the HomePage
        """
        pass
