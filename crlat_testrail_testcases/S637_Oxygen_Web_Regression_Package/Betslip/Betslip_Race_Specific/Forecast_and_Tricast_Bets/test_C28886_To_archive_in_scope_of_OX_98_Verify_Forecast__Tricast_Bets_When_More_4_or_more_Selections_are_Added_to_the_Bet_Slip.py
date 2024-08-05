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
class Test_C28886_To_archive_in_scope_of_OX_98_Verify_Forecast__Tricast_Bets_When_More_4_or_more_Selections_are_Added_to_the_Bet_Slip(Common):
    """
    TR_ID: C28886
    NAME: [To archive in scope of OX 98] Verify 'Forecast / Tricast' Bets When More 4 or more Selections are Added to the Bet Slip
    DESCRIPTION: This test case verifies 'Combination Tricast' and 'Combination Forecast' fields which appear when 4 OR more selections are added to the Bet Slip.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_4_or_more_race_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 4 or more <Race> selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_002_open_bet_slip(self):
        """
        DESCRIPTION: Open 'Bet Slip'
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_003_verify_forecast__tricast_section(self):
        """
        DESCRIPTION: Verify 'Forecast / Tricast' section
        EXPECTED: 'Forecast / Tricast ' section is shown
        EXPECTED: Section header is 'FORECASTS/TRICASTS (n)'
        EXPECTED: Section consists of fields:
        EXPECTED: *   **'Combination Tricast (k)'**
        EXPECTED: *   **'Combination Forecast (k)'**
        """
        pass

    def test_004_verify_combination_tricast_k_field(self):
        """
        DESCRIPTION: Verify **'Combination Tricast (k)'** field
        EXPECTED: 'Combination Tricast (k)' section is shown
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: The counter (k) is calculated by formula:
        EXPECTED: k=n(n-1)(n-2)
        EXPECTED: where, n - the number of added selections which are used for forecast/tricast bets
        """
        pass

    def test_005_verify_combination_forecast_k_field(self):
        """
        DESCRIPTION: Verify **'Combination Forecast (k)'** field
        EXPECTED: 'Combination Forecast (k)' section is shown
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: The counter (k) is calculated by the formula :
        EXPECTED: k=n(n-1)
        EXPECTED: where, n = the number of added selections which are used for forecast/tricast bets
        """
        pass
