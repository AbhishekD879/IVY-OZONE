import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60063761_Verfiy_Tote_Bet_Placement_for_international(Common):
    """
    TR_ID: C60063761
    NAME: Verfiy Tote Bet Placement for international
    DESCRIPTION: 
    PRECONDITIONS: International Tote events are available on the front end
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladrokescom(self):
        """
        DESCRIPTION: Open https://msports.ladrokes.com
        EXPECTED: Ladbrokes application launched
        """
        pass

    def test_002_click_on_hr(self):
        """
        DESCRIPTION: Click on HR
        EXPECTED: User navigated to HR LP
        """
        pass

    def test_003_select_a_international_tote_meeting_which_contains_tote_markets_availableeg_quadpotplacepotjackpottricastexca_etc(self):
        """
        DESCRIPTION: Select a International Tote meeting which contains Tote markets available
        DESCRIPTION: (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        EXPECTED: User has selected International Tote meeting (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        """
        pass

    def test_004_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Bet placed successfully
        """
        pass

    def test_005_verify_minimum_bets_for_eg_quadpotplacepotjackpottricastexca_etc(self):
        """
        DESCRIPTION: Verify Minimum bets for (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        EXPECTED: User is prompted with minimum bet value for (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc) when attempting to place bet below this amount.
        """
        pass

    def test_006_verify_only_1_tote_bet_can_be_placed_at_a_time_in_the_betslip(self):
        """
        DESCRIPTION: Verify only 1 tote bet can be placed at a time in the betslip
        EXPECTED: User displayed with only 1 tote bet in betslip and can only place 1 tote bet a time.
        """
        pass
