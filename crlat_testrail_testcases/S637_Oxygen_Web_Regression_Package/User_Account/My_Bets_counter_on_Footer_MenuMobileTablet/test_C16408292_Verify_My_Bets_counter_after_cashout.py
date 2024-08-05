import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C16408292_Verify_My_Bets_counter_after_cashout(Common):
    """
    TR_ID: C16408292
    NAME: Verify My Bets counter after cashout
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after successful cash-out
    DESCRIPTION: AUTOTEST [C29855321]
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure user has open (unsettled) bets with cash out available
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - Should be tested for Sports/Races singles and multiple bets
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_002_make_a_full_cashout_for_a_bet(self):
        """
        DESCRIPTION: Make a full cashout for a bet
        EXPECTED: Bet is cashed out
        """
        pass

    def test_003_verify_my_bets_counter_displaying_on_the_footer(self):
        """
        DESCRIPTION: Verify My Bets counter displaying on the Footer
        EXPECTED: My Bets counter is decreased by one
        """
        pass

    def test_004_make_a_partial_cashout_for_another_bet(self):
        """
        DESCRIPTION: Make a partial cashout for another bet
        EXPECTED: Bet is partially cashed out
        """
        pass

    def test_005_verify_my_bets_counter_displaying_on_the_footer(self):
        """
        DESCRIPTION: Verify My Bets counter displaying on the Footer
        EXPECTED: My Bets counter remains the same
        """
        pass

    def test_006_make_a_full_cash_out_for_a_bet_from_step_4(self):
        """
        DESCRIPTION: Make a full cash out for a bet from step #4
        EXPECTED: Bet is cashed out
        """
        pass

    def test_007_verify_my_bets_counter_displaying_on_the_footer(self):
        """
        DESCRIPTION: Verify My Bets counter displaying on the Footer
        EXPECTED: My Bets counter is decreased by one
        """
        pass
