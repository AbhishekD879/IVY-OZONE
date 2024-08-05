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
class Test_C9243967_Races_sections_ordering_on_resulted_event_details_page(Common):
    """
    TR_ID: C9243967
    NAME: <Races>: sections ordering on resulted event details page
    DESCRIPTION: This test case verifies ordering of sections on <Race> result details page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have Horse Race and Greyhounds events with enabled Forecast and Tricast on market level, with enabled "Each-way" on market level, with some non runners, with Rule 4 deduction configured
    PRECONDITIONS: - You should have created different forecasts and tricasts with dividends for the events above
    PRECONDITIONS: - Events should be resulted with winning runners from one of the configured forecast and tricast
    PRECONDITIONS: - You should be on a <Race> result details page
    PRECONDITIONS: NOTE: Horse Races and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_order_of_sections(self):
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
