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
class Test_C9472158_Races_displaying_canceled_event_on_resulted_event_details_page(Common):
    """
    TR_ID: C9472158
    NAME: <Races>: displaying canceled event on resulted event details page
    DESCRIPTION: This test case verifies results page displaying when event was canceled
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have resulted <Race> event where all the runners/greyhounds have been resulted as 'void'
    PRECONDITIONS: - You should be on result details page of the event above
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_results_page_displaying(self):
        """
        DESCRIPTION: Verify results page displaying
        EXPECTED: Horse Races and greyhounds:
        EXPECTED: - Time/status/date section is displayed
        EXPECTED: - All runners from the race are displayed as non runners in "Non Runners" section respectively
        EXPECTED: - 'V' icons under ODDS column are displayed next to the each non runner
        """
        pass
