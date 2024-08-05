import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870293__Any_Counter_Offer_gets_sent_back_kill_the_app_browser_and_reload_the_app_browser(BaseBetSlipTest):
    """
    TR_ID: C44870293
    NAME: - Any Counter Offer gets sent back kill the app/browser and reload the app/browser
    DESCRIPTION: The desktop equivalent to this is log out and close the tab. Open a new tab in the same browser and check that the bet is still there and you can place the bet.
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    bet_username = tests.settings.betplacement_user
    max_bet = 0.2
    max_mult_bet = 0.3
    suggested_max_bet = 0.25
    prices = {0: '1/12', 1: '1/2', 2: '1/3'}

    def verify_overask_message(self):
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=5)
        self.assertFalse(overask, msg='Overask is not closed')
        overask_trader_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=5)
        cms_overask_trader_message = wait_for_result(lambda: self.get_overask_trader_offer(), timeout=5)
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=5)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

    def go_to_bethistory_openbets(self):
        self.navigate_to_page("Homepage")
        self.site.header.right_menu_button.click()
        self.device.driver.implicitly_wait(5)
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right-Menu')
        self.site.right_menu.click_item('HISTORY')
        self.site.wait_splash_to_hide(3)
        self.site.right_menu.click_item(item_name='BETTING HISTORY')
        self.site.wait_content_state(state_name='BetHistory')
        self.site.close_all_dialogs()
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()

    def verify_bet_in_openbets(self):
        open_bets = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())
        self.assertTrue(self.event_name in open_bets[0], msg=f'${self.event_name} bet not found in the account history')

    def verify_bet_not_in_openbets(self):
        try:
            open_bets = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name)
            self.assertFalse(open_bets, msg='Cancelled bet is present in "Open bets" tab')
        except Exception as e:
            self._logger.info(e)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet, max_mult_bet=self.max_mult_bet, default_market_name='|Draw No Bet|')
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login(username=self.bet_username)
        self.__class__.previous_balance = self.site.header.user_balance

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_offer_by_stakeprice(self):
        """
        DESCRIPTION: Counter Offer by Stake/Price
        EXPECTED: Counter offer gets sent back
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.bet_username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        self.verify_overask_message()

    def test_003_kill_the_appbrowser_and_reload_the_appbrowser(self):
        """
        DESCRIPTION: Kill the app/browser and reload the app/browser
        EXPECTED: Should still see the running counter offer, with the time still counting down and the accept and decline buttons
        """
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
        self.site.open_betslip()
        self.verify_overask_message()

    def test_004_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.site.wait_splash_to_hide()
        self.check_bet_receipt_is_displayed()
        actual_stake = self.site.bet_receipt.footer.total_stake
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_stake, str(self.suggested_max_bet),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.suggested_max_bet)}"')
        self.verify_estimated_returns(bet_amount=self.suggested_max_bet, odds=self.prices[0],
                                      est_returns=actual_est_returns)
        self.site.bet_receipt.close_button.click()
        self.navigate_to_page('Homepage')
        self.assertEqual(self.previous_balance, self.site.header.user_balance + self.suggested_max_bet, msg="balance isnt updated")

    def test_005_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        self.site.open_my_bets_open_bets()
        self.site.wait_splash_to_hide()
        self.verify_bet_in_openbets()
        self.go_to_bethistory_openbets()
        self.verify_bet_in_openbets()
        self.navigate_to_page("Homepage")
        self.site.logout()

    def test_006_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.test_000_preconditions()
        self.test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_counter_offer_by_stakeprice()
        self.test_003_kill_the_appbrowser_and_reload_the_appbrowser()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_not_in_openbets()
        self.go_to_bethistory_openbets()
        self.verify_bet_not_in_openbets()
