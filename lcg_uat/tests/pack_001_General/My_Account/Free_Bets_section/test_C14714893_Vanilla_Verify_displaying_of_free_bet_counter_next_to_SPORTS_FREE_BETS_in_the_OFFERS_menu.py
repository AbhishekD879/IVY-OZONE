import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod Can't grant freebets
# @pytest.mark.hl Can't grant freebets
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C14714893_Vanilla_Verify_displaying_of_free_bet_counter_next_to_SPORTS_FREE_BETS_in_the_OFFERS_menu(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C14714893
    NAME: [Vanilla] Verify displaying of free bet counter next to 'SPORTS FREE BETS' in the 'OFFERS' menu
    DESCRIPTION: This test case verifies that users are able to see free bet counter next to 'SPORTS FREE BETS' options
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: - User is logged in with only 1 FreeBet available
        DESCRIPTION: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 3088)
        DESCRIPTION: - FreeBets menu item exists if available in CMS (Right Menu) no matter if FreeBets are available to user or not
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.team1 = event_params.team1
        self.__class__.team2 = event_params.team2
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount, card_number=tests.settings.visa_card)
        self.site.login(username=self.username, async_close_dialogs=False)

        avatar = self.site.header.user_panel.my_account_button
        if not avatar.has_freebet_icon():
            self.site.logout()
            self.ob_config.grant_freebet(username=self.username)
            self.site.login(username=self.username)

    def test_001_log_in_with_user_from_preconditions(self):
        """
        DESCRIPTION: Log in with user from preconditions
        EXPECTED: User is logged in
        """
        self.assertTrue(self.site.wait_logged_in(timeout=5), msg='User is not logged in')

    def test_002_open_main_page_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Open main page and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS' option
        """
        self.site.wait_content_state('Homepage')
        avatar = self.site.header.user_panel.my_account_button
        self.assertTrue(avatar.is_displayed(),
                        msg='User avatar is not displayed.')

        avatar.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Account menu is not opened.')

        menu_items = self.site.right_menu.items_as_ordered_dict

        self.assertTrue(menu_items, msg='Right menu items not found')
        self.__class__.offers = self.site.window_client_config.offers_menu_title
        self.__class__.sports_freebets = self.site.window_client_config.sports_freebets_menu_title
        self.assertIn(self.offers, menu_items.keys(),
                      msg=f'"{self.offers}" not present in the Right column')

    def test_003_click_on_the_offers_options(self):
        """
        DESCRIPTION: Click on the 'OFFERS' options
        EXPECTED: Free Bet counter is shown next to 'SPORT FREE BETS' with the number of available free bets (1)
        """
        self.site.right_menu.click_item(item_name=self.offers)
        result = wait_for_result(lambda: self.site.right_menu.header.title == self.offers,
                                 name='Wait for header title to change')

        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{self.offers}"')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu has no items available.')

        self.assertIn(self.sports_freebets, menu_items.keys(),
                      msg=f'"{self.sports_freebets}" not present in the Right column')
        sports_freebets_menu_item = menu_items.get(self.sports_freebets)
        self.assertTrue(sports_freebets_menu_item, msg='Sports Freebets menu item not found.')
        freebet_counter_value = sports_freebets_menu_item.badge_text
        expected_freebet_counter_value = '1' if self.brand == 'bma' else 'FB'

        self.assertEqual(freebet_counter_value, expected_freebet_counter_value,
                         msg=f'Freebet counter value does not equal "{expected_freebet_counter_value}" and equals "{freebet_counter_value}" instead')

    def test_004_use_free_bet_available_for_the_user_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Use free bet available for the user and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS' option
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        avatar = self.site.header.user_panel.my_account_button
        avatar.click()

        self.assertTrue(self.site.is_right_menu_opened(), msg='Account menu is not opened.')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        self.assertIn(self.offers, menu_items.keys(),
                      msg=f'"{self.offers}" not present in the Right column')

    def test_005_click_on_the_offers_option(self):
        """
        DESCRIPTION: Click on the 'OFFERS' option
        EXPECTED: Free Bet counter is not shown next to 'SPORT FREE BETS'
        """
        self.site.right_menu.click_item(item_name=self.offers)
        result = wait_for_result(lambda: self.site.right_menu.header.title == self.offers,
                                 name='Wait for header title to change')

        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{self.offers}"')

        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu has no items available.')

        self.assertIn(self.sports_freebets, menu_items.keys(),
                      msg=f'{self.sports_freebets} not present in the Right column')
        sports_freebets_menu_item = self.site.right_menu.items_as_ordered_dict.get(self.sports_freebets)
        self.assertTrue(sports_freebets_menu_item, msg='Sports Freebets menu item not found.')
        freebet_counter_value = sports_freebets_menu_item.badge_text
        expected_freebet_counter_value = ''

        self.assertEqual(freebet_counter_value, expected_freebet_counter_value,
                         msg=f'Freebet counter value is not empty and equals "{freebet_counter_value}" instead')

    def test_006_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        if self.device_type == 'desktop':
            self.site.right_menu.header.back_button.click()
            self.site.right_menu.log_out_button.click()
        else:
            self.site.right_menu.close_icon.click()
            self.site.logout()
            self.assertTrue(self.site.wait_logged_out(timeout=5), msg='User is not logged out.')

    def test_007_login_to_the_account_with_multiple_more_than_two_freebets_available_and_click_on_the_avatar_in_the_header(
            self):
        """
        DESCRIPTION: Login to the account with multiple (more than two)
        FreeBets available and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS' option
        """
        for _ in range(3):
            self.ob_config.grant_freebet(username=self.username)
        self.site.login(self.username)
        avatar = self.site.header.user_panel.my_account_button
        avatar.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Account menu is not opened.')

        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu has no items available.')
        self.assertIn(self.offers, menu_items.keys(),
                      msg=f'"{self.offers}" not present in the Right column')

    def test_008_click_on_the_offers_options(self):
        """
        DESCRIPTION: Click on the 'OFFERS' options
        EXPECTED: Free Bet counter is shown next to 'SPORT FREE BETS' with the number of available free bets
        """
        self.site.right_menu.click_item(item_name=self.offers)
        result = wait_for_result(lambda: self.site.right_menu.header.title == self.offers,
                                 name='Wait for header title to change')

        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{self.offers}"')
        sports_freebets_menu_item = self.site.right_menu.items_as_ordered_dict.get(self.sports_freebets)
        self.assertTrue(sports_freebets_menu_item, msg='Sports Freebets menu item not found.')
        freebet_counter_value = sports_freebets_menu_item.badge_text
        expected_freebet_counter_value = '3' if self.brand == 'bma' else 'FB'

        self.assertEqual(freebet_counter_value, expected_freebet_counter_value,
                         msg=f'Freebet counter value does not equal "{expected_freebet_counter_value}" and equals "{freebet_counter_value}" instead')

    def test_009_use_one_of_the_free_bet_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Use one of the free bet and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS' options
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team2])
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

        avatar = self.site.header.user_panel.my_account_button
        avatar.click()

        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu has no items available.')

        self.assertTrue(menu_items, msg='Right menu items not found')
        self.assertIn(self.offers, menu_items.keys(),
                      msg=f'"{self.offers}" not present in the Right column')

    def test_010_click_on_the_offers_option(self):
        """
        DESCRIPTION: Click on the 'OFFERS' option
        EXPECTED: Free Bet counter is shown next to ’SPORT FREE BETS’ with the updated number of available free bets
        """
        self.site.right_menu.click_item(item_name=self.offers)
        self.site.wait_content_state_changed(timeout=4)
        sports_freebets_menu_item = self.site.right_menu.items_as_ordered_dict.get(self.sports_freebets)
        self.assertTrue(sports_freebets_menu_item, msg='Sports Freebets menu item not found.')
        freebet_counter_value = sports_freebets_menu_item.badge_text
        expected_freebet_counter_value = '2' if self.brand == 'bma' else 'FB'

        self.assertEqual(freebet_counter_value, expected_freebet_counter_value,
                         msg=f'Freebet counter value does not equal "{expected_freebet_counter_value}" and equals "{freebet_counter_value}" instead')
