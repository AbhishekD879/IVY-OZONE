import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9240620_Races_displaying_forecast_tricast_dividends_on_resulted_event_details_page_based_on_forecast_tricast_check_boxes_state_in_OB(Common):
    """
    TR_ID: C9240620
    NAME: <Races>: displaying forecast/tricast dividends on resulted event details page based on forecast/tricast check boxes state in OB
    DESCRIPTION: This test case verifies displaying of forecast/tricast dividends based on forecast/tricast check boxed in OB
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 3 resulted <Race> events:
    PRECONDITIONS: 1) With enabled Forecast and Tricast, with configured Forecast and Tricast in ascending and descending order (e.g Tricast 1-2-3 and 3-2-1), winning runners should be in ascending order
    PRECONDITIONS: 2) With enabled Forecast and Tricast, with configured Forecast and Tricast in ascending and descending order (e.g Tricast 1-2-3 and 3-2-1), winning runners should be in descending order
    PRECONDITIONS: 3) With disabled Forecast and Tricast
    PRECONDITIONS: - You should be on a <Race> details page with enabled forecast/tricast with winning runners in ascending order
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_forecast(self):
        """
        DESCRIPTION: Verify displaying of forecast
        EXPECTED: For Horse Racing and Greyhounds:
        EXPECTED: "DIVIDEND" section is displayed
        EXPECTED: UI elements:
        EXPECTED: - Section name is 'DIVIDEND' with 2 columns 'RESULT' and 'DIVIDEND'
        EXPECTED: - Forecast and Tricast are displayed under the 'DIVIDENDS' column and only those that have exact order of winning runners
        EXPECTED: - Section name and dividends types are displayed in bold
        EXPECTED: - Winners numbers are placed under the 'RESULT' column against respective dividend type
        EXPECTED: - Amounts of dividends are placed under the 'DIVIDEND' column against respective dividend type
        """
        pass

    def test_002_go_to_race_event_with_configured_forecast_and_tricast_and_winning_runners_in_descending_order(self):
        """
        DESCRIPTION: Go to <Race> event with configured Forecast and Tricast and winning runners in descending order
        EXPECTED: For Horse Racing and Greyhounds:
        EXPECTED: "DIVIDEND" section is displayed
        EXPECTED: UI elements:
        EXPECTED: - Section name is 'DIVIDEND' with 2 columns 'RESULT' and 'DIVIDEND'
        EXPECTED: - Forecast and Tricast are displayed under the 'DIVIDENDS' column and only those that have exact order of winning runners
        EXPECTED: - Section name and dividends types are displayed in bold
        EXPECTED: - Winners numbers are placed under the 'RESULT' column against respective dividend type
        EXPECTED: - Amounts of dividends are placed under the 'DIVIDEND' column against respective dividend type
        """
        pass

    def test_003_go_to_race_details_page_with_disabled_forecasttricast_and_verify_dividend_section_displaying(self):
        """
        DESCRIPTION: Go to <Race> details page with disabled forecast/tricast and verify 'DIVIDEND' section displaying
        EXPECTED: For Horse Racing and Greyhounds:
        EXPECTED: 'DIVIDEND' section with forecast and tricast respectively is not displayed
        """
        pass
