import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.issue('https://jira.openbet.com/browse/LCRCORE-16654')  # Issue in ladbrokes only. todo : Need to remove this marker after given epic was closed
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.trader_timeout
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898514_Verify_Free_Bet_token_is_NOT_used_up_if_trader_declines_times_out_or_user_cancels_times_out(BaseBetSlipTest):
    """
    TR_ID: C59898514
    NAME: Verify Free Bet  token is NOT used up if trader declines/times out or user cancels/times out.
    PRECONDITIONS: Free Bet tokens should be assigned.
    """
    keep_browser_open = True
    max_bet = 0.2
    suggested_max_bet = 0.25
    prices = {0: '1/2', 1: '1/11', 2: '1/9'}
    new_price = '1/10'

    def verifying_free_bet(self):
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id_1)
        wait_for_result(lambda: self.get_betslip_sections().Singles, timeout=15)
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(self.stake.has_use_free_bet_link(), msg=f'"Has Use Free Bet" link was not found for "{stake_name}" ')

    def test_000_precondition(self):
        """
        PRECONDITIONS: User needs to have free bet tokens assigned.
        """
        self.__class__.username_1 = tests.settings.betplacement_user
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet,
                                                                                 default_market_name='|Draw No Bet|')
        self.__class__.eventID_1, selection_ids_1 = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id_1 = list(selection_ids_1.values())[0]
        self.ob_config.grant_freebet(username=self.username_1)

    def test_001_add_any_selection_use_free_bet_and_trigger_oa(self):
        """
        DESCRIPTION: Add any selection, use free bet and trigger OA.
        EXPECTED: Trader should see the bet in OB.
        """
        self.site.login(self.username_1)
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        try:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=10)
            self.verifying_free_bet()
            self.stake.use_free_bet_link.click()
            self.select_free_bet()
            self.__class__.bet_amount = self.max_bet + 0.1
            self.place_single_bet(number_of_stakes=1)
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
            account_id, bet_id, betslip_id = \
                self.bet_intercept.find_bet_for_review(username=self.username_1, event_id=self.eventID_1)
            self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                           betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_002_trader_times_out_the_bet(self):
        """
        DESCRIPTION: Trader times out the bet
        EXPECTED: User should see the message and able to use free bet token for same or other bet.
        EXPECTED: Note:  If user or trader times out the bet then FB appears back in 10 mins.
        """
        self.site.wait_content_state_changed()
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='"Overask" is not closed')
        self.site.wait_content_state_changed(timeout=15)
        overask_warning_message = self.get_betslip_content().overask_warning
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.some_bets_with_freebet,
                         msg=f'Actual message "{overask_warning_message}" does not match '
                             f'expected "{vec.betslip.OVERASK_MESSAGES.some_bets_with_freebet}"')
        self.navigate_to_page('homepage')
        self.verifying_free_bet()
        self.clear_betslip()
        self.site.wait_content_state(state_name='homepage')

    def test_003_repeat_step_1__2_but_trader_declining_bet_this_time(self):
        """
        DESCRIPTION: Repeat step 1 & 2 but trader declining bet this time.
        EXPECTED: User should see the message and able to use free bet token for same or other bet.
        """
        self.verifying_free_bet()
        self.stake.use_free_bet_link.click()
        self.select_free_bet()
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username_1,
                                                                                event_id=self.eventID_1)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.decline_bet(event_id=self.eventID_1, bet_id=bet_id, betslip_id=betslip_id)
        self.site.wait_content_state_changed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
        self.device.refresh_page()
        self.verifying_free_bet()
        self.clear_betslip()
        self.site.wait_content_state(state_name='homepage')

    def test_004_add_any_selection_use_free_bet_and_trigger_oa(self):
        """
        DESCRIPTION: Add any selection, use free bet and trigger OA.
        EXPECTED: Trader should see the bet in OB.
        """
        try:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, offer_timeout=10)
            self.verifying_free_bet()
            self.stake.use_free_bet_link.click()
            freebet_stake = self.select_free_bet()
            self.place_single_bet(number_of_stakes=1)
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
            account_id, bet_id, betslip_id = \
                self.bet_intercept.find_bet_for_review(username=self.username_1, event_id=self.eventID_1)
            self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                     betslip_id=betslip_id, price_1=self.new_price,
                                                     max_bet=self.bet_amount + float(freebet_stake))
            self.site.wait_splash_to_hide(timeout=5)
            overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=5)
            self.assertFalse(overask, msg='Overask is not closed')
            overask_message = self.get_betslip_content().wait_for_overask_message_to_change(timeout=10)
            self.assertTrue(overask_message, msg='Overask Offer timeout message is not triggered for the User')
            self.site.wait_splash_to_hide(timeout=5)
            overask_offer_timeout_message = self.get_betslip_content().overask_warning
            self.assertEqual(overask_offer_timeout_message, vec.betslip.OVERASK_MESSAGES.customer_action_time_expired,
                             msg=f'Actual message "{overask_offer_timeout_message}" is not same as'
                                 f'Expected message "{vec.betslip.OVERASK_MESSAGES.customer_action_time_expired}"')
            self.verifying_free_bet()
            self.clear_betslip()
            self.site.wait_content_state(state_name='homepage')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_005_trader_offers_price(self):
        """
        DESCRIPTION: Trader offers price
        EXPECTED: User should see the offer.
        """
        # This step is coverd in step4

    def test_006_user_times_out_the_offer(self):
        """
        DESCRIPTION: User times out the offer
        EXPECTED: User should see the message and able to use free bet token for same or other bet.
        EXPECTED: Note:  If user or trader times out the bet then FB appears back in 10 mins.
        """
        # This step is coverd in step4

    def test_007_repeat_steps_4_and_5(self):
        """
        DESCRIPTION: Repeat steps 4 and 5
        """
        self.site.wait_content_state_changed()
        self.verifying_free_bet()
        self.stake.use_free_bet_link.click()
        freebet_stake = self.select_free_bet()
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username_1, event_id=self.eventID_1)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price,
                                                 max_bet=self.bet_amount + float(freebet_stake))
        self.site.wait_splash_to_hide(timeout=5)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=15)
        self.assertFalse(overask, msg='Overask is not closed')

    def test_008_user_cancels_the_offer(self):
        """
        DESCRIPTION: User cancels the offer
        EXPECTED: User should see the message and able to use free bet token for same or other bet.
        """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=5),
                             msg='Betslip widget was not closed')
        self.device.refresh_page()
        self.verifying_free_bet()
