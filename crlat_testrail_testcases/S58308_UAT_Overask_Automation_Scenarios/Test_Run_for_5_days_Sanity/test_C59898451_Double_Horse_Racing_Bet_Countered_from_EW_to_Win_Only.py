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
class Test_C59898451_Double_Horse_Racing_Bet_Countered_from_EW_to_Win_Only(Common):
    """
    TR_ID: C59898451
    NAME: Double Horse Racing Bet Countered from EW to Win Only
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_selections_from_hr_to_betsliptrigger_overask_select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selections from HR to Betslip
        DESCRIPTION: Trigger Overask (Select E/W checkbox and try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_the_double_bet_from_ew_to_win_only_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter the Double bet from EW to Win Only in OB TI tool
        EXPECTED: Counter offer with the Win Only is displayed and updated potential returns shown to the customer
        """
        pass

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated correctly
        """
        pass

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History
        """
        pass

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass
