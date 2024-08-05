import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C18640313_Verify_Surface_Bet_module_displaying_when_live_event_has_market_bet_in_runN(Common):
    """
    TR_ID: C18640313
    NAME: Verify Surface Bet module displaying when live event has market bet_in_run: "N"
    DESCRIPTION: This test case verifies behaviour of Surface Bet module when live event is used and its market bet_in_run: "N"
    PRECONDITIONS: 1. There are at least 2 Surface Bets added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Surface Bets contain selections from live events
    PRECONDITIONS: 3. Market bet_in_run: "Y" (in TI checkbox 'Bet In Running' is ticked on market level)
    PRECONDITIONS: Load Home page
    PRECONDITIONS: Open Network > ws > wss://featured-sports
    """
    keep_browser_open = True

    def test_001___in_ti_set_bet_in_runn_to_all_markets_of_any_surface_bet_and_save_changes__in_app_observe_featured_ws_and_fe_behaviour(self):
        """
        DESCRIPTION: - In TI set bet_in_run: "N" to all markets of any Surface Bet and save changes
        DESCRIPTION: - In app observe featured ws and FE behaviour
        EXPECTED: In featured ws:
        EXPECTED: - Event update with market bet_in_run: "N" is received
        EXPECTED: - Surface bet module update is received NOT containing Surface Bet with market bet_in_run: "N"
        EXPECTED: On FE:
        EXPECTED: Surface Bet with market bet_in_run: "N" is removed automatically
        """
        pass

    def test_002___in_ti_set_bet_in_runn_to_all_markets_of_the_last_surface_bet_and_save_changes__in_app_observe_featured_ws_and_fe_behaviour(self):
        """
        DESCRIPTION: - In TI set bet_in_run: "N" to all markets of the last Surface Bet and save changes
        DESCRIPTION: - In app observe featured ws and FE behaviour
        EXPECTED: In featured ws:
        EXPECTED: - Event update with market bet_in_run: "N" is received
        EXPECTED: - “FEATURED_STRUCTURE_CHANGED" is received NOT containing SB module at all
        EXPECTED: On FE:
        EXPECTED: Surface Bet with market bet_in_run: "N" is removed automatically
        """
        pass

    def test_003_repeat_steps_1_2_on_sport_landing_page(self):
        """
        DESCRIPTION: Repeat steps 1-2 on Sport Landing page
        EXPECTED: 
        """
        pass
