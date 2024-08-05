import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from datetime import timedelta
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod : as Freebets cannot be created in prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870229_Verify_user_sees_Free_bets_item_in_My_Account_menu(BaseBetSlipTest):
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
    username = tests.settings.betplacement_user

    def test_001_launch_beta_application(self):
        """
        DESCRIPTION: Launch BETA application
        EXPECTED: HomePage is opened
        """
        self.site.wait_content_state(state_name='homepage')

    def test_002_login_with_freebets_available_user(self):
        """
        DESCRIPTION: Login with freebets available user
        EXPECTED: user is logged in
        """
        self.__class__.selection_ids = self.ob_config.add_football_event_to_england_premier_league().selection_ids
        exp_date = datetime.now() + timedelta(hours=24)
        self.ob_config.grant_freebet(username=self.username, level='event',
                                     id=self.ob_config.add_football_event_to_england_premier_league().event_id,
                                     expiration_date=exp_date)
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, async_close_dialogs=False)
        self.site.wait_content_state('Home Page')

    def test_003_verify_user_sees__total_free_bets_amount_in_my_account(self):
        """
        DESCRIPTION: Verify user sees  total Free bets amount in My Account
        EXPECTED: Freebet xx.xx is displayed on My Account
        """
        if self.brand == 'bma':
            freebet_token_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION)
            self.assertTrue(freebet_token_dialog, msg='Freebet dialog is not shown')
            self.assertTrue(freebet_token_dialog.freebet_sum, msg='Freebet sum popup is not displayed')
            self.assertTrue(freebet_token_dialog.has_close_button(), msg='"Close" Button is not shown')
            self.assertTrue(freebet_token_dialog.ok_button.is_displayed(), msg='"OK" Button is not shown')
            freebet_token_dialog.click_ok()
            dialog_closed = freebet_token_dialog.wait_dialog_closed()
            self.assertTrue(dialog_closed, msg='Dialog is not closed after pressing OK button')
            self.site.close_all_dialogs(async_close=False)

    def test_004_tap_on_my_account_and_verify_user_sees_free_bets_item_in_my_account_menu(self):
        """
        DESCRIPTION: Tap on My Account and Verify user sees Free bets item in My Account menu
        EXPECTED: My Account menu is opened and free bet item is displayed
        """
        # Coral: OFFERS & FREE BETS, Ladbrokes: Promotions
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        actual_menu_items = list(self.site.right_menu.get_items().keys())
        if self.brand == 'bma':
            self.assertEqual(actual_menu_items, vec.bma.OFFERS_FREE_BETS_MENU_ITEMS,
                             msg=f'Actual offers & free bets items "{actual_menu_items}" is not as same as '
                                 f'Expected offers & free bets items "{vec.bma.OFFERS_FREE_BETS_MENU_ITEMS}"')
            freebet = vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[1]
        else:
            self.assertEqual(actual_menu_items, vec.bma.PROMOTIONS_MENU_ITEMS,
                             msg=f'Actual offers & free bets items "{actual_menu_items}" is not as same as '
                                 f'Expected offers & free bets items "{vec.bma.PROMOTIONS_MENU_ITEMS}"')
            freebet = vec.bma.PROMOTIONS_MENU_ITEMS[0]
        self.site.right_menu.click_item(item_name=freebet)
        self.site.close_all_dialogs(async_close=False)

    def test_005_verify_total_amount_in__of_free_bets_is_displayed_next_to_the_menu_item(self):
        """
        DESCRIPTION: Verify Total amount in £ of Free Bets is displayed next to the menu item
        EXPECTED: Total Amount is displayed
        EXPECTED: ![](index.php?/attachments/get/49920193)
        """
        self.site.wait_content_state('freebets')
        self.assertTrue(self.site.freebets.balance.total_balance, msg='the total balance is not displayed')

    def test_006_verify_when_item_is_tapped_customer_can_see_all_available_tokens_listed_with_token_name_token_value_expiry_date_redemption_values_tokens_are_listed_in_expiry_date_order_if_the_same_prioritise_higher_value_tokens(self):
        """
        DESCRIPTION: Verify When item is tapped, customer can see all available tokens listed with Token Name, Token Value, Expiry Date, Redemption Values Tokens are listed in Expiry date order (if the same, prioritise higher value tokens)
        EXPECTED: Free bets details are displayed
        """
        freebets = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebets, msg='No Free Bets found on page')
        freebet_item_name, freebet_item = list(freebets.items())[0]
        if self.brand == 'bma':
            freebet_item.click()
            sleep(2)
            self.assertTrue(self.site.freebet_details.title, msg='Freebet title is not displayed')
            self.assertTrue(self.site.freebet_details.has_expires(), msg='Freebet has no expires')
            self.assertTrue(self.site.freebet_details.expires, msg='Freebet expires is not displayed')
            self.assertTrue(self.site.freebet_details.value, msg='Freebet value is not displayed')
            self.assertTrue(self.site.freebet_details.bet_now, msg='Bet now button is not displayed')
        else:
            self.assertTrue(freebet_item.freebet_title, msg='Freebet title is not displayed')
            self.assertTrue(freebet_item.freebet_value, msg='Freebet value is not displayed')
            self.assertTrue(freebet_item.used_by, msg='Freebet has no expires')

    def test_007_verify__user_can_tap_on_the_token_to_take_them_to_the_relative_page_use_odds_boost_page_logic(self):
        """
        DESCRIPTION: Verify  User can tap on the token to take them to the relative page (use Odds Boost page logic)
        EXPECTED: Odds boost page opened
        """
        self.site.freebet_details.bet_now.click()
        self.site.wait_content_state_changed()
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])

    def test_008_verify__user_can_tap_on_information_icon_that_initiates_pop_up_that_explains_what_user_can_use_the_free_bet_on(self):
        """
        DESCRIPTION: verify  User can tap on information icon that initiates pop-up that explains what user can use the free bet on
        EXPECTED: Information pop up is displayed
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section.items()) == 1, msg='One stake should be found in betslip Singles section')
        stake_name, stake = list(singles_section.items())[0]
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        stake.amount_form.input.value = self.bet_amount
        self.assertTrue(stake.freebet_tooltip, msg='The free bet tooltip is not displayed')
        stake.freebet_tooltip.click()

    def test_009_verify_user_sees_free_bets_message_on_betslip(self):
        """
        DESCRIPTION: Verify user sees free bets message on betslip
        EXPECTED: Free bet available message is displayed
        """
        self.assertTrue(self.site.contents.free_bets_notification, msg='The freebet notification is not displayed')
        self.site.close_betslip()

    def test_010_verify_user_is_shown_expiry_message_when_free_bet_expiring_within_24_hourswhen_they_log_into_the_app(self):
        """
        DESCRIPTION: Verify user is shown expiry message when free bet expiring within 24 hours,when they log into the app
        EXPECTED: Message appear on top of the HomePage
        """
        # this is only applicable for mobile as the notification is unavailable in desktop
        if self.device_type == 'mobile':
            self.site.logout()
            self.site.login(username=self.username, async_close_dialogs=True)
            self.assertTrue(self.site.contents.free_bets_notification, msg='The freebet notification is not displayed')
