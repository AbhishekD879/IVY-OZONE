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
class Test_C64256393_Verify_betslip_by_adding_Horse_Racing_tote_pools_bets(Common):
    """
    TR_ID: C64256393
    NAME: Verify betslip by adding Horse Racing tote pools bets.
    DESCRIPTION: Verify betslip by adding Horse Racing tote pools bets.
    PRECONDITIONS: * HR tote pool bets available in front end
    PRECONDITIONS: * Initially any selection is added to betslip
    """
    keep_browser_open = True

    def test_001_load_the_application__navigate_to_horse_racing__page(self):
        """
        DESCRIPTION: Load the application & navigate to Horse Racing  page
        EXPECTED: * Front End application is loaded.
        EXPECTED: * HR landing page is displayed.
        """
        pass

    def test_002_navigate_to_edp_page__gt_tote_pool_tab(self):
        """
        DESCRIPTION: Navigate to EDP page -&gt; tote pool tab
        EXPECTED: * Totepool tab contains win, place, exacta, trifecta, quadpot, placepot, Jackpot bets
        """
        pass

    def test_003_try_to_add_any_tote_pool_bet__eg_placepot_to_enhanced_betslip(self):
        """
        DESCRIPTION: Try to add any tote pool bet  e.g., placepot to enhanced betslip
        EXPECTED: * Unable to add tote pool bet to the betslip
        EXPECTED: * User will get popup with the following message: 'You already have one or more selections in the betslip that can't be combined, please remove those selections to add any new selection'
        """
        pass

    def test_004_remove_all_selections_from_betslip(self):
        """
        DESCRIPTION: Remove all selections from betslip
        EXPECTED: * Betslip becomes empty
        """
        pass

    def test_005_add_only_tote_pool_bet__eg_placepot_to_enhanced_betslip(self):
        """
        DESCRIPTION: Add only tote pool bet  e.g., placepot to enhanced betslip
        EXPECTED: * Totepool bet is added to the betslip
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy totepool selection names.
        """
        pass

    def test_006_repeat_step_5_for_totepool_tab_that_contains_win_place_exacta_trifecta_quadpot_jackpot_bets(self):
        """
        DESCRIPTION: Repeat step-5 for Totepool tab that contains win, place, exacta, trifecta, quadpot, Jackpot bets
        EXPECTED: 
        """
        pass
