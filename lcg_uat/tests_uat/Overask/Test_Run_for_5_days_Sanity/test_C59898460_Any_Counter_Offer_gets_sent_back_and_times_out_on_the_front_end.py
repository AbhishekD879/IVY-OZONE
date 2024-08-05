import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.trader_timeout
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898460_Any_Counter_Offer_gets_sent_back_and_times_out_on_the_front_end(BaseBetSlipTest):
    """
    TR_ID: C59898460
    NAME: Any Counter Offer gets sent back and times out on the front end
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.2
    suggested_max_bet = 0.25
    prices = {0: '1/12', 1: '1/11', 2: '1/9'}

    def test_000_precondition(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created test event
        """
        self.__class__.username = tests.settings.betplacement_user
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet, default_market_name='|Draw No Bet|')
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login(self.username)
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        wait_for_result(lambda: self.get_betslip_sections().Singles, timeout=10)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_offer_by_stakeprice(self):
        """
        DESCRIPTION: Counter Offer by Stake/Price
        EXPECTED: Counter offer gets sent back
        """
        try:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, offer_timeout=10)
            account_id, bet_id, betslip_id = \
                self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
            self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                           betslip_id=betslip_id, max_bet=self.suggested_max_bet)
            self.site.wait_content_state_changed()
            overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=15)
            self.assertFalse(overask, msg='Overask is not closed')
            overask_message = self.get_betslip_content().wait_for_overask_message_to_change(timeout=15)
            self.assertTrue(overask_message, msg='Overask Offer timeout message is not triggered for the User')
            self.site.wait_content_state_changed()
            overask_offer_timeout_message = self.get_betslip_content().overask_warning
            self.assertEqual(overask_offer_timeout_message, vec.betslip.OVERASK_MESSAGES.customer_action_time_expired,
                             msg=f'Actual message "{overask_offer_timeout_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.customer_action_time_expired}"')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_003_time_out_on_the_front_end(self):
        """
        DESCRIPTION: Time out on the front end
        EXPECTED: After the Counter Offer has expired, the customer will see the bet slip with the message that the offer has Expired and we should not see a bet in My Bets and Account History.
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
