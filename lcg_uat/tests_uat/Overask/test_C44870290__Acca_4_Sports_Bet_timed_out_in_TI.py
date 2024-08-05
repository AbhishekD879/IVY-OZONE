import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.open_bets
@pytest.mark.uat
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.overask
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870290__Acca_4_Sports_Bet_timed_out_in_TI(BaseBetSlipTest):
    """
    TR_ID: C44870290
    NAME: - Acca 4 Sports Bet timed out in TI
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.2
    suggested_max_bet = 0.94
    prices = {0: '1/12'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        for i in range(4):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp=self.prices, max_bet=self.max_bet)
            selection_ids = event_params.selection_ids
            self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login()
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)

    def test_001_add_four_selections_from_any_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add four selections from any sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        try:
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.__class__.bet_amount = self.max_bet + 0.1
            self.place_single_bet(number_of_stakes=1)
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_002_time_out_in_ti(self):
        """
        DESCRIPTION: Time out in TI
        EXPECTED: After the Counter Offer has expired in TI, the customer will see the bet slip with the message that "this bet has not been accepted by traders!" and we should not see a bet in My Bets and Account History.
        """
        self.device.driver.implicitly_wait(5)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
