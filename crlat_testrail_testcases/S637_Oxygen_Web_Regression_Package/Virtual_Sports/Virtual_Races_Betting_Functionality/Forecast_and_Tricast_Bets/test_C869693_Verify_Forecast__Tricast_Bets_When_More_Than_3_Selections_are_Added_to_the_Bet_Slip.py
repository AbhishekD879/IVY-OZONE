import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869693_Verify_Forecast__Tricast_Bets_When_More_Than_3_Selections_are_Added_to_the_Bet_Slip(Common):
    """
    TR_ID: C869693
    NAME: Verify 'Forecast / Tricast' Bets When More Than 3 Selections are Added to the Bet Slip
    DESCRIPTION: This test case verifies 'Combination Tricast' and 'Combination Forecast' fields which appear when more than 3 selections are added to the Bet Slip for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_virtual_racing_event_details_page(self):
        """
        DESCRIPTION: Go to the <Virtual Racing> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_more_than_3_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add more than 3 selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open 'Bet Slip'
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_verify_forecast__tricast_section(self):
        """
        DESCRIPTION: Verify 'Forecast / Tricast' section
        EXPECTED: 'Forecast / Tricast ' section is shown
        EXPECTED: Section header is 'Forecast / Tricast (n)'
        EXPECTED: Section consists of fields:
        EXPECTED: *   **'Combination Tricast (k)'**
        EXPECTED: *   '**Combination Forecast (k)**'
        """
        pass

    def test_006_verify_combination_tricast_k_field(self):
        """
        DESCRIPTION: Verify **'Combination Tricast (k)'** field
        EXPECTED: 'Combination Tricast (k)' section is shown
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: The counter (k) is calculated by formula:
        EXPECTED: k=n(n-1)(n-2)
        EXPECTED: where, n - the number of added selections which are used for forecast/tricast bets
        """
        pass

    def test_007_verify_combination_forecast_k_filed(self):
        """
        DESCRIPTION: Verify** 'Combination Forecast (k)'** filed
        EXPECTED: 'Combination Forecast (k)' section is shown
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: The counter (k) is calculated by the formula :
        EXPECTED: k=n(n-1)
        EXPECTED: where, n = the number of added selections which are used for forecast/tricast bets
        """
        pass
