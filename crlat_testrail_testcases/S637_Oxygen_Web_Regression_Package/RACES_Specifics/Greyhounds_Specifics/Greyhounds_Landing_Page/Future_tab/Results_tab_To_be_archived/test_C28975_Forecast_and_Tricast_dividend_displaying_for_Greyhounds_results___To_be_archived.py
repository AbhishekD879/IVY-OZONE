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
class Test_C28975_Forecast_and_Tricast_dividend_displaying_for_Greyhounds_results___To_be_archived(Common):
    """
    TR_ID: C28975
    NAME: Forecast and Tricast dividend displaying for Greyhounds results  -  To be archived
    DESCRIPTION: This test case verifies Forecast and Tricast dividend displaying for Greyhounds results
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-12167 Greyhounds - Include dividend payouts to results
    PRECONDITIONS: Data about Forecast/Tricast dividends for event can be viewed via https://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.20/RacingResultsForEvent/*Event_ID*
    PRECONDITIONS: *Example:*
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.20/RacingResultsForEvent/4240829
    PRECONDITIONS: <ncastDividend id="517362" marketId="63787471" siteChannels="P,Q,C,I,M," type="FC" dividend="6.0000" runnerNumbers="1,2,"/>
    PRECONDITIONS: <ncastDividend id="517363" marketId="63787471" siteChannels="P,Q,C,I,M," type="TC" dividend="7.0000" runnerNumbers="1,2,4,"/>
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_greyhounds___resutls_section(self):
        """
        DESCRIPTION: Go to Greyhounds -> Resutls section
        EXPECTED: *   'Results' tab is opened
        EXPECTED: *   **'By Latest Results' **sorting type is selected by default
        EXPECTED: *   Results are displayed ONLY for today's events (see '**startTime'** attribute)
        """
        pass

    def test_003_verify_forecasttricast_dividend_displaying_for_event_results(self):
        """
        DESCRIPTION: Verify Forecast/Tricast dividend displaying for event results
        EXPECTED: Forecast/Tricast dividend are displayed for the event if available
        """
        pass

    def test_004_verify_format_of_text_and_data_displaying_for_forecttricast_dividends(self):
        """
        DESCRIPTION: Verify format of text and data displaying for Forect/Tricast dividends
        EXPECTED: *   'Straight Forecast:' text is displayed in bold
        EXPECTED: *   'Tricast:' text is displayed in bold beneath the text 'Straight Forecast'
        EXPECTED: *   Both lines of text are positioned beneath the Each Way Terms
        EXPECTED: *   Value of Straight Forecast is displayed next to the text in format £00.00
        EXPECTED: *   Value of Tricast is displayed next to the text in format £00.00
        """
        pass

    def test_005_verify_data_displaying_for_straight_forecast_parameter(self):
        """
        DESCRIPTION: Verify data displaying for Straight Forecast parameter
        EXPECTED: Data received from OpenBet for selected event are displayed
        """
        pass

    def test_006_verify_data_displaying_for_tricast_parameter(self):
        """
        DESCRIPTION: Verify data displaying for Tricast parameter
        EXPECTED: Data received from OpenBet for selected event are displayed
        """
        pass
