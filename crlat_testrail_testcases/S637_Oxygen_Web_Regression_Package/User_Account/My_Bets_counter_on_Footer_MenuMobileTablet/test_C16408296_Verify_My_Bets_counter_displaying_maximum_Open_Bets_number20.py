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
class Test_C16408296_Verify_My_Bets_counter_displaying_maximum_Open_Bets_number20(Common):
    """
    TR_ID: C16408296
    NAME: Verify My Bets counter displaying maximum Open Bets number(20+)
    DESCRIPTION: This test case verifies displaying more than 20 open bets on My Bets Badge Icon
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Login with user who has 21 open (unsettled) bets
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_verify_my_bets_on_footer_menu(self):
        """
        DESCRIPTION: Verify 'My bets' on Footer Menu
        EXPECTED: My bets counter icon is displayed with '20+' in top right corner
        """
        pass

    def test_002_go_to_cashout_pagetab_and_make_a_full_cashout_of_one_bet(self):
        """
        DESCRIPTION: Go to Cashout page/tab and make a full cashout of one bet
        EXPECTED: Bet is cashed out successfully
        """
        pass

    def test_003_verify_my_bets_on_footer_menu(self):
        """
        DESCRIPTION: Verify 'My bets' on Footer Menu
        EXPECTED: My bets counter icon is displayed with '20' in top right corner
        """
        pass

    def test_004_add_selection_to_betslipquickbet_and_place_bet(self):
        """
        DESCRIPTION: Add selection to Betslip/QuickBet and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_005_verify_my_bets_on_footer_menu(self):
        """
        DESCRIPTION: Verify 'My bets' on Footer Menu
        EXPECTED: My bets counter icon is displayed with '20+' in top right corner
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: My Bets Footer menu is displayed without counter
        """
        pass
