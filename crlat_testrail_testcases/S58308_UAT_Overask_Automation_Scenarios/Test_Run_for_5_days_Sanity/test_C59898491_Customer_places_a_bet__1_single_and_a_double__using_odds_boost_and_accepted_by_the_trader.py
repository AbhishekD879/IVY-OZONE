import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59898491_Customer_places_a_bet__1_single_and_a_double__using_odds_boost_and_accepted_by_the_trader(Common):
    """
    TR_ID: C59898491
    NAME: Customer places a bet - 1 single and a double - using odds boost and accepted by the trader
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_hr_selections_or_any_sport_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stakemake_sure_bet_is_boosted__click_on_odds_boosted_(self):
        """
        DESCRIPTION: Add HR selections OR ANY sport SELECTIONS to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        DESCRIPTION: Make sure Bet is boosted ( Click on Odds Boosted )
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_accept_the_bet_in_ti(self):
        """
        DESCRIPTION: Accept the bet in TI
        EXPECTED: User is  taken to the bet receipt with bet as placed
        EXPECTED: Correct potential return should be shown to user
        EXPECTED: The balance should be updated correctly and bet receipt shown to the customer with odds boost signposting
        """
        pass

    def test_003_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History. and user should see signposted in My Bets section
        """
        pass
