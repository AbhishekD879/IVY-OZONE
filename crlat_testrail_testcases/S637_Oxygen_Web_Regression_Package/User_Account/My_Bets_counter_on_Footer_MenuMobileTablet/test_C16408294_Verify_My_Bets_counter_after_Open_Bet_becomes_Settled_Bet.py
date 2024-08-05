import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C16408294_Verify_My_Bets_counter_after_Open_Bet_becomes_Settled_Bet(Common):
    """
    TR_ID: C16408294
    NAME: Verify My Bets counter after Open Bet becomes Settled Bet
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Open Bet becomes Settled Bet
    DESCRIPTION: AUTOTEST [C58695430] TST ONLY
    PRECONDITIONS: - Make sure My bets counter config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - OB TI tool:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_load_oxygenroxanne_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen/Roxanne Application and login
        EXPECTED: 
        """
        pass

    def test_002_place_a_bet_for_sportsracing_event(self):
        """
        DESCRIPTION: Place a bet for sports/racing event
        EXPECTED: * Bet is placed
        EXPECTED: * Bet counter on 'My Bets' Footer menu is increased by one
        """
        pass

    def test_003_in_ob_ti_settle_event(self):
        """
        DESCRIPTION: In OB TI settle event
        EXPECTED: Event is settled
        """
        pass

    def test_004_check_my_bets_counter_on_footer(self):
        """
        DESCRIPTION: Check My bets counter on Footer
        EXPECTED: My bets counter on Footer Menu remains the same
        """
        pass

    def test_005_refresh_the_page_and_check_my_bets_counter_on_footer(self):
        """
        DESCRIPTION: Refresh the page and check My bets counter on Footer
        EXPECTED: My bets counter is decreased by one on 'My Bets' Footer menu
        EXPECTED: NOTE: If there are 0 open bets, My Bets counter is NOT displayed, only My bets Footer Menu without counter
        """
        pass

    def test_006__repeat_steps_2_4_navigate_to_my_bets_page_on_mobile_and_cash_outmy_bets_tab_on_tablet(self):
        """
        DESCRIPTION: * Repeat steps #2-4
        DESCRIPTION: * Navigate to My Bets page on Mobile and Cash out/My Bets tab on Tablet
        EXPECTED: My bets counter is decreased by one
        """
        pass
