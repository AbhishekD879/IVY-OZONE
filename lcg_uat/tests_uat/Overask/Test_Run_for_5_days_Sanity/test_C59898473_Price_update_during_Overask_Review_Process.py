import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898473_Price_update_during_Overask_Review_Process(BaseBetSlipTest):
    """
    TR_ID: C59898473
    NAME: Price update during Overask Review Process
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = {0: '1/20'}
    change_price = '1/15'
    new_price = '1/10'

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp_prices=self.prices, max_bet=self.max_bet,
                                                                                 max_mult_bet=self.max_mult_bet)
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
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        self.__class__.bet_slip_odds_value = stake.odds
        self.assertTrue(self.bet_slip_odds_value, msg='bet slip odd value is empty')
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_update_the_price_in_ob_during_overask_review_process(self):
        """
        DESCRIPTION: Update the price in OB during Overask Review Process
        EXPECTED: Updated price should not be shown in betslip
        EXPECTED: If counter offer is made in TI  then the bet should appear in the state sent back from TI
        EXPECTED: No error messaging regarding price change should be shown
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.change_price)
        self.assertNotEqual(self.bet_slip_odds_value, self.change_price,
                            msg=f'price is changed from "{self.bet_slip_odds_value}" to "{self.change_price}"')
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, max_bet=self.bet_amount)
        sections = self.get_betslip_sections().Singles
        stake_odd_value = sections.overask_trader_offer.stake_content.odd_value.value
        odd_value = stake_odd_value.strip(' x')
        self.assertEqual(odd_value, self.new_price,
                         msg=f'Actual price :{odd_value} is not same as'
                             f'Expected price :{self.new_price}')
