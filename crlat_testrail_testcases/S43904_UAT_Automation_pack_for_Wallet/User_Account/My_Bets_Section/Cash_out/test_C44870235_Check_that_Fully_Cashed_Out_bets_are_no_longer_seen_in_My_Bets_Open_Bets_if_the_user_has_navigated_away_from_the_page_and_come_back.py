import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870235_Check_that_Fully_Cashed_Out_bets_are_no_longer_seen_in_My_Bets_Open_Bets_if_the_user_has_navigated_away_from_the_page_and_come_back(Common):
    """
    TR_ID: C44870235
    NAME: Check that Fully Cashed Out bets are no longer seen in My Bets->Open Bets if the user has navigated away from the page and come back
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_a_bet_from_a_cash_out_market(self):
        """
        DESCRIPTION: Make a bet from a cash out market
        EXPECTED: You should have placed a bet from a cash out market
        """
        pass

    def test_002_go_to_my_bets_open_bets_and_fully_cash_out_this_bet(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and fully cash out this bet.
        EXPECTED: You should have fully cashed out this bet
        """
        pass

    def test_003_go_to_any_other_page_eg_my_bets_open_bets_or_click_on_menu_and_then_come_back_to_my_bets_open_bets_and_verify_that_your_cashed_out_bet_is_no_longer_seen_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Go to any other page e.g. My Bets->Open Bets or click on Menu and then come back to My Bets-Open Bets and verify that your cashed out bet is no longer seen in My Bets->Open Bets
        EXPECTED: Your bet should not be in My Bets-Open Bets
        """
        pass
