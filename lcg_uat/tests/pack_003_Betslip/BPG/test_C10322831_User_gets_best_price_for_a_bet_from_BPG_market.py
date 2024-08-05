import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # Can't result_selection on prod/hl
# @pytest.mark.prod
@pytest.mark.medium
@pytest.mark.bpg
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C10322831_User_gets_best_price_for_a_bet_from_BPG_market(BaseBetSlipTest):
    """
    TR_ID: C10322831
    NAME: User gets best price for a bet from BPG market
    PRECONDITIONS: GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)
    PRECONDITIONS: Event has SP and LP prices available
    PRECONDITIONS: User has GP betting enabled (OB ti -> search for the customer -> Account Rules -> GP checkbox under NOT ALLOWED section should be unchecked)
    """
    keep_browser_open = True
    bet_amount = 0.50
    new_odds = '4/1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and log in
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, gp=True, lp_prices=['1/5'])
        self.__class__.selection_id = list(event.selection_ids.values())[0]
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id
        self.site.login(username=tests.settings.user_with_allowed_gp_betting)

    def test_001_add_lp_selection_from_bpg_market_to_the_betslip_enter_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Add LP selection from BPG market to the Betslip, enter stake and place a bet
        EXPECTED: Bet is placed
        EXPECTED: (note estimated returns)
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_info = self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_002_result_and_settle_event_so_the_selection_wins_set_sp_price__lp_price(self):
        """
        DESCRIPTION: Result and settle event so the selection wins. Set SP price > LP price
        """
        self.ob_config.result_selection(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID, result='W', price=self.new_odds)
        self.ob_config.confirm_result(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID, result='W')
        self.ob_config.settle_result(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID, result='W')

    def test_003_verify_amount(self):
        """
        DESCRIPTION: Verify amount
        EXPECTED: Balance is increased on amount calculated basing on SP price not LP price (SP is the best price in this case)
        """
        old_est_returns = self.bet_info.get('total_estimate_returns')
        new_est_returns = self.calculate_estimated_returns(bet_amount=self.bet_amount, odds=[self.new_odds])
        self.assertNotEqual(old_est_returns, new_est_returns,
                            msg=f'Old est returns "{old_est_returns}" not changed to "{new_est_returns}"')
        self.verify_user_balance(expected_user_balance=(self.user_balance - self.bet_amount + old_est_returns),
                                 page='betreceipt',
                                 timeout=20)
