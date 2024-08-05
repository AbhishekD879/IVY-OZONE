import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C28882_To_archive_in_scope_of_OX_98_Verify_Bet_Slip_where_Forecast_Tricast_are_available(Common):
    """
    TR_ID: C28882
    NAME: [To archive in scope of OX 98] Verify Bet Slip where 'Forecast'/'Tricast' are available
    DESCRIPTION: This test case verifies in what conditions forecast/tricast options will be available on the Bet Slip
    DESCRIPTION: AUTOTEST [C965108]
    PRECONDITIONS: 1. User is logged in
    """
    keep_browser_open = True

    def test_001_go_to_the_race_event_details_page(self):
        """
        DESCRIPTION: Go to the <Race> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_add_two_or_more_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_003_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_004_verify_forecasttricast_bets(self):
        """
        DESCRIPTION: Verify 'Forecast'/'Tricast' bets
        EXPECTED: * 'Forecast'/'Tricast' bets are shown in the section below the 'Singles' section
        EXPECTED: * 'Forecast'/'Tricast' bets are shown ONLY after 'Singles' section
        """
        pass

    def test_005_clear_the_betslip_and_add_two_or_more_selections_from_one_market_of_the_different_race_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more selections from one market of the different <Race> events to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_006_open_bet_slip_and_verify_forecasttricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: For each event it's own forecasts/tricasts betting options are build and shown as separate section
        """
        pass

    def test_007_clear_the_betslip_and_add_two_or_more_selections_from_each_different_markets_of_the_same_race_event_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more selections from each different markets of the same <Race> event to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_008_open_bet_slip_and_verify_forecasttricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: * 'Forecast'/'Tricast' bets are shown in the section below the 'Singles' section
        EXPECTED: * 'Forecast'/'Tricast' bets are shown ONLY after 'Singles' section
        """
        pass
