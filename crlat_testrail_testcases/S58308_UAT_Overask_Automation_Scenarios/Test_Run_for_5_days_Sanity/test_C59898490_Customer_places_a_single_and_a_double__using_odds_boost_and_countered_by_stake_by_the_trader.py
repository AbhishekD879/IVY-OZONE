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
class Test_C59898490_Customer_places_a_single_and_a_double__using_odds_boost_and_countered_by_stake_by_the_trader(Common):
    """
    TR_ID: C59898490
    NAME: Customer places a single and a double - using odds boost and countered by stake by the trader
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_single_hr_selections_or_any_sport_selection_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_(self):
        """
        DESCRIPTION: Add single HR selections OR ANY sport SELECTION to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        DESCRIPTION: Make sure Bet is boosted ( Click on Odds Boosted )
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_by_stake_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: Counter is seen a offer with the new stake highlighted and updated potential returns shown to the customeron FE
        """
        pass

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: The balance should be updated correctly and bet receipt shown to the customer with odds boost signposting
        """
        pass

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History. and  user should see signposted in My Bets section
        """
        pass

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass

    def test_006_repeat_the_same_steps_by_adding_a_double_selection_from_hr_or_any_other_sports(self):
        """
        DESCRIPTION: Repeat the same steps by adding a double selection from HR or any other sports.
        EXPECTED: 
        """
        pass
