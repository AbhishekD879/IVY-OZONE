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
class Test_C44870287__Single_Sports_Bet_Accepted(Common):
    """
    TR_ID: C44870287
    NAME: - Single Sports Bet Accepted
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_single_oa_bet_on_any_sport_except_hr_and_gh(self):
        """
        DESCRIPTION: Place a single OA bet on any sport except HR and GH
        EXPECTED: The bet should go through to the OA flow
        """
        pass

    def test_002_in_the_traders_interface_accept_the_bet(self):
        """
        DESCRIPTION: In the Trader's Interface, accept the bet
        EXPECTED: On the Front End, you should see the bet receipt
        """
        pass

    def test_003_check_that_the_bet_shows_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Check that the bet shows in My Bets->Open Bets
        EXPECTED: The bet should show in My Bets->Open Bets
        """
        pass
