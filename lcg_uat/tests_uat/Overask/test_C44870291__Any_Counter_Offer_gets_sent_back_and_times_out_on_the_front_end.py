import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.uat
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870291__Any_Counter_Offer_gets_sent_back_and_times_out_on_the_front_end(BaseBetSlipTest):
    """
    TR_ID: C44870291
    NAME: - Any Counter Offer gets sent back and times out on the front end
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    suggested_max_bet = 0.25
    prices = {0: '1/12', 1: '1/11', 2: '1/9'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet, default_market_name='|Draw No Bet|')
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=2)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_offer_by_stakeprice(self):
        """
        DESCRIPTION: Counter Offer by Stake/Price
        EXPECTED: Counter offer gets sent back
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        self.device.driver.implicitly_wait(3)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=5)
        self.assertFalse(overask, msg='Overask is not closed')
        overask_message = self.get_betslip_content().wait_for_overask_message_to_change(timeout=10)
        self.assertTrue(overask_message, msg='Overask Offer timeout message is not triggered for the User')
        self.device.driver.implicitly_wait(3)
        overask_offer_timeout_message = self.get_betslip_content().overask_warning
        self.assertEqual(overask_offer_timeout_message, vec.betslip.OVERASK_MESSAGES.customer_action_time_expired,
                         msg=f'Actual message "{overask_offer_timeout_message}" is not same as'
                         f'Expected message "{vec.betslip.OVERASK_MESSAGES.customer_action_time_expired}"')

    def test_003_time_out_on_the_front_end(self):
        """
        DESCRIPTION: Time out on the front end
        EXPECTED: After the Counter Offer has expired, the customer will see the bet slip with the message that the offer has Expired and we should not see a bet in My Bets and Account History.
        """
        # This steps is covered in step 2
