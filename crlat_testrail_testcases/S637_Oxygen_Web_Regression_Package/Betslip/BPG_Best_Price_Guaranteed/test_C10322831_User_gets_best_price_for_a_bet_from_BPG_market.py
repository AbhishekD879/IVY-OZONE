import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C10322831_User_gets_best_price_for_a_bet_from_BPG_market(Common):
    """
    TR_ID: C10322831
    NAME: User gets best price for a bet from BPG market
    DESCRIPTION: 
    PRECONDITIONS: GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)
    PRECONDITIONS: Event has SP and LP prices available
    PRECONDITIONS: User has GP betting enabled (OB ti -> search for the customer -> Account Rules -> GP checkbox under NOT ALLOWED section should be unchecked)
    PRECONDITIONS: **NOTE: BPG replaced to BOG ( https://jira.egalacoral.com/browse/BMA-49331 ) from Coral 101.2 / Ladbrokes 100.4 versions**
    """
    keep_browser_open = True

    def test_001_add_lp_selection_eg_15_from_bpg_market_to_the_betslip_enter_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Add LP selection (e.g. 1/5) from BPG market to the Betslip, enter stake and place a bet.
        EXPECTED: Bet is placed
        EXPECTED: (note estimated returns)
        """
        pass

    def test_002_go_to_the_set_results_page_in_tiset_starting_price_for_your_selection_greater_than_lp_price_in_step_above_eg_11result_and_settle_event_so_the_selection_wins(self):
        """
        DESCRIPTION: Go to the 'Set Results' page in TI.
        DESCRIPTION: Set 'Starting Price' for your selection greater than LP price in step above (e.g. 1/1).
        DESCRIPTION: Result and settle event so the selection wins.
        EXPECTED: ![](index.php?/attachments/get/102113869)
        """
        pass

    def test_003_verify_that_balance_is_increased_on_more_than_potential_returns_value_in_step_1(self):
        """
        DESCRIPTION: Verify that balance is increased on more than Potential Returns value in step 1.
        EXPECTED: Balance is increased on amount calculated basing on SP price not LP price (SP (Starting Price) is the best price in this case)
        """
        pass
