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
class Test_C2512945_Edited_for_OX98_Verify_Bet_Slip_where_Forecast_Tricast_bets_are_NOT_available(Common):
    """
    TR_ID: C2512945
    NAME: [Edited for OX98] Verify Bet Slip where 'Forecast'/'Tricast' bets are NOT available
    DESCRIPTION: This test case verifies in what conditions forecast/tricast options will not be available on the Bet Slip
    DESCRIPTION: AUTOTEST [C2605959]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_two_or_three_selections_from_the_same_race_but_each_from_different_market(self):
        """
        DESCRIPTION: Add two or three selections from the same <Race> but each from **different** market
        EXPECTED: Selections are added
        """
        pass

    def test_002_open_bet_slip_and_verify_forecasttricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: 'Forecast'/'Tricast' bets are NOT available if selections from different markets are added
        """
        pass

    def test_003_clear_the_betslip_and_add_two_or_more_selections_from_different_races_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more selections from **different** <Races> to the Bet Slip
        EXPECTED: Selections are added to the Bet Slip
        """
        pass

    def test_004_open_bet_slip_and_verify_forecasttricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: 'Forecast'/'Tricast' bets are NOT available if selections from different events are added
        """
        pass

    def test_005_clear_the_betslip_and_add_two_or_more_sport_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more <Sport> selections from the **same** market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_006_verify_forecasttricast_bets(self):
        """
        DESCRIPTION: Verify 'Forecast/Tricast' bets
        EXPECTED: 'Forecast/Tricast' bets are NOT available for <Sport> events
        """
        pass

    def test_007_add_two_or_three_selections_from_the_same_race__from_the_same_marketstep_not_valid_for_releases_earlier_than_ox98(self):
        """
        DESCRIPTION: Add two or three selections from the same <Race>  from the **same** market
        DESCRIPTION: **Step not valid for releases earlier than OX98**
        EXPECTED: Selections are added
        """
        pass

    def test_008_open_bet_slip_and_verify_forecasttricast_betsstep_not_valid_for_releases_earlier_than_ox98(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        DESCRIPTION: **Step not valid for releases earlier than OX98**
        EXPECTED: 'Forecast'/'Tricast' bets are NOT available if selections from same markets are added
        """
        pass
