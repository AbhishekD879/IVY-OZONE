import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C9240629_Horse_Racing_event_details_page_for_resulted_events(Common):
    """
    TR_ID: C9240629
    NAME: Horse Racing event details page for resulted events
    DESCRIPTION: This test case verifies UI elements on resulted Horse Race details page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have resulted Horse Race events with next configurations:
    PRECONDITIONS: - 1) Each-way enabled
    PRECONDITIONS: - 2) With enabled Forecast and Tricast on market level
    PRECONDITIONS: - 3) With different Forecasts and Tricasts configured
    PRECONDITIONS: - 4) With information received about trainer, age etc. (For Greyhounds we receive this information from TimeForm)
    PRECONDITIONS: - 5) With non runners (non runners has N/R in title, e.g. |Krocko N/R|)
    PRECONDITIONS: - 6) With Rule 4 deduction configured
    PRECONDITIONS: - You should be on a Horse Race details page
    """
    keep_browser_open = True

    def test_001_verify_events_time_and_status_section(self):
        """
        DESCRIPTION: Verify event's time and status section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section has no title
        EXPECTED: - Section include info about event start time and name, event status and full event date
        """
        pass

    def test_002_verify_each_way_section(self):
        """
        DESCRIPTION: Verify "Each Way" section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Each way with odds and places is displayed
        EXPECTED: - Promo icons, cash out icon (For Ladbrokes cash out icon shouldn't be displayed)
        """
        pass

    def test_003_verify_race_result_section(self):
        """
        DESCRIPTION: Verify Race Result section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section with "Race result" title is displayed
        EXPECTED: - Section include info about won runners:
        EXPECTED: 1) Place
        EXPECTED: 2) Silk
        EXPECTED: 3) Number and name
        EXPECTED: 4) Trainer and jokey
        EXPECTED: 5) ODDS (SP price)
        EXPECTED: 6) F/2F/JF/2JF labels
        EXPECTED: NOTE:
        EXPECTED: Ladbrokes:
        EXPECTED: - f/2f/jf/2jf labels are displayed next to the SP price in lower case
        EXPECTED: Coral:
        EXPECTED: - F/2F/JF/2JF labels are displayed next to the runner name in upper case
        """
        pass

    def test_004_verify_deduction_section(self):
        """
        DESCRIPTION: Verify "DEDUCTION" section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section with "DEDUCTION" title is displayed
        EXPECTED: - Section include 'Rule 4' raw and deduction value
        """
        pass

    def test_005_verify_dividend_section(self):
        """
        DESCRIPTION: Verify 'DIVIDEND' section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section with 'DIVIDEND' title and 2 columns 'RESULT' and 'DIVIDEND' is displayed
        EXPECTED: - Section include info about Forecast and Tricast according to the won runners with proper result and dividend value
        """
        pass

    def test_006_verify_non_runners_section(self):
        """
        DESCRIPTION: Verify 'NON RUNNERS' section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section with 'NON RUNNERS' title is displayed
        EXPECTED: - Section include only non runners
        EXPECTED: - Grey silk, runner number and name
        EXPECTED: - For Ladbrokes: trainer and jokey should be displayed for non runners
        """
        pass

    def test_007_verify_order_of_sections(self):
        """
        DESCRIPTION: Verify order of sections
        EXPECTED: 1) Event's time and status section
        EXPECTED: 2) "Each Way" section
        EXPECTED: 3) "RACE RESULT" section
        EXPECTED: 4) "DEDUCTION" section
        EXPECTED: 5) "DIVIDEND" section
        EXPECTED: 6) "NON RUNNERS" section
        """
        pass
