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
class Test_C59898513_Verify_Odds_Boost_token_is_NOT_used_up_if_trader_declines_times_out_or_user_cancels_times_out(BaseBetSlipTest):
    """
    TR_ID: C59898513
    NAME: Verify Odds Boost token is NOT used up if trader declines/times out or user cancels/times out.
    PRECONDITIONS: User needs to have odds boost tokens assigned.
    """
    keep_browser_open = True
    max_bet = 0.2
    suggested_max_bet = 0.25
    prices = {0: '1/12', 1: '1/11', 2: '1/9'}

    def verify_odds_boost(self):
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        wait_for_result(lambda: self.get_betslip_sections().Singles, timeout=10)
        self.assertTrue(self.site.betslip.odds_boost_header.boost_button.is_displayed(),
                        msg='"Odds boost button" is not displayed')

    def placing_bet_verify_overask(self):
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def find_bet_for_review__and_add_offer_stake(self):
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        self.site.wait_splash_to_hide(timeout=5)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')

    def test_000_precondition(self):
        """
        PRECONDITIONS: User needs to have odds boost tokens assigned.
        """
        self.__class__.username = tests.settings.odds_boost_user
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet, default_market_name='|Draw No Bet|')
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]

    def test_001_add_any_selection_click_on_odds_boost_and_trigger_oa(self):
        """
        DESCRIPTION: Add any selection, click on odds boost and trigger OA.
        EXPECTED: Trader should see the bet in OB.
        """
        self.site.login(self.username)
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        try:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)
            self.verify_odds_boost()
            self.__class__.bet_amount = self.max_bet + 0.1
            self.placing_bet_verify_overask()
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_002_trader_times_out_the_bet(self):
        """
        DESCRIPTION: Trader times out the bet
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        self.site.wait_splash_to_hide(5)
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        single_section = self.get_betslip_sections().Singles
        stake = single_section.overask_trader_offer.stake_content.stake_value.value.strip('£')
        self.assertEqual(float(stake), self.max_bet,
                         msg=f'Actual Stake: "{stake}" is not same as '
                             f'Expected stake: "{self.max_bet}"')
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=5),
                             msg='Betslip widget was not closed')
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.verify_odds_boost()
        self.navigate_to_page('homepage')
        self.site.wait_content_state(state_name='homepage')

    def test_003_repeat_step_1__2_but_trader_declining_bet_this_time(self):
        """
        DESCRIPTION: Repeat step 1 & 2 but trader declining bet this time.
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.device.refresh_page()
        self.verify_odds_boost()
        self.site.betslip.odds_boost_header.boost_button.click()
        self.placing_bet_verify_overask()
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.site.wait_content_state_changed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
        self.device.refresh_page()
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.verify_odds_boost()
        self.clear_betslip()
        self.site.wait_content_state(state_name='homepage')

    def test_004_add_any_selection_click_on_odds_boost_and_trigger_oa(self):
        """
        DESCRIPTION: Add any selection, click on odds boost and trigger OA.
        EXPECTED: Trader should see the bet in OB.
        """
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        try:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, offer_timeout=10)
            self.verify_odds_boost()
            self.site.betslip.odds_boost_header.boost_button.click()
            self.placing_bet_verify_overask()
            self.find_bet_for_review__and_add_offer_stake()
            overask_message = self.get_betslip_content().wait_for_overask_message_to_change(timeout=15)
            self.assertTrue(overask_message, msg='Overask Offer timeout message is not triggered for the User')
            self.site.wait_splash_to_hide(timeout=5)
            overask_offer_timeout_message = self.get_betslip_content().overask_warning
            self.assertEqual(overask_offer_timeout_message, vec.betslip.OVERASK_MESSAGES.customer_action_time_expired,
                             msg=f'Actual message "{overask_offer_timeout_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.customer_action_time_expired}"')
            self.site.wait_content_state(state_name='homepage')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_005_trader_offers_price_or_stake(self):
        """
        DESCRIPTION: Trader offers price or stake
        EXPECTED: User should see the offer.
        """
        # This step is coverd in step 4

    def test_006_user_times_out_the_offer(self):
        """
        DESCRIPTION: User times out the offer
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.verify_odds_boost()
        self.clear_betslip()
        self.site.wait_content_state(state_name='homepage')

    def test_007_repeat_steps_4_and_5(self):
        """
        DESCRIPTION: Repeat steps 4 and 5
        """
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.verify_odds_boost()
        self.site.betslip.odds_boost_header.boost_button.click()
        self.placing_bet_verify_overask()
        self.find_bet_for_review__and_add_offer_stake()

    def test_008_user_cancels_the_offer(self):
        """
        DESCRIPTION: User cancels the offer
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=5),
                             msg='Betslip widget was not closed')
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.verify_odds_boost()
