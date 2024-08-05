import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.uat
@pytest.mark.open_bets
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870288__Single_Sports_Bet_timed_out_in_TI(BaseBetSlipTest):
    """
    TR_ID: C44870288
    NAME: - Single Sports Bet timed out in TI
    """
    keep_browser_open = True
    max_bet = 1.2
    prices = {0: '1/12', 1: '1/11', 2: '1/9'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_UK_racing_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.runner_name = list(event_params.selection_ids.keys())[0]
        selection_ids = event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login()
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)

    def test_001_place_a_single_oa_bet_on_any_sport(self):
        """
        DESCRIPTION: Place a single OA bet on any sport
        EXPECTED: The bet should have gone to the OA flow
        """
        try:
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.__class__.bet_amount = self.max_bet + 0.1
            self.place_single_bet(number_of_stakes=1)
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_002_in_the_traders_interface_allow_the_bet_to_time_out(self):
        """
        DESCRIPTION: In the Trader's Interface, allow the bet to time out
        EXPECTED: The bet should have timed out
        """
        # this step is covered in preconditions

    def test_003_check_that_on_the_front_end_you_see_the_message_saying_that_the_bet_has_not_been_accepted_by_the_trader(self):
        """
        DESCRIPTION: Check that on the front end, you see the message saying that the bet has not been accepted by the Trader
        EXPECTED: You should see the message
        """
        self.site.wait_splash_to_hide(5)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

    def test_004_check_my_bets_open_bets_to_confirm_that_the_bet_has_not_been_placed(self):
        """
        DESCRIPTION: Check My Bets->Open Bets to confirm that the bet has not been placed
        EXPECTED: The bet should not have been placed
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        try:
            open_bets = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.runner_name)
            self.assertFalse(open_bets, msg='Cancelled bet is present in "Open bets" tab')
        except Exception as e:
            self._logger.info(e)
