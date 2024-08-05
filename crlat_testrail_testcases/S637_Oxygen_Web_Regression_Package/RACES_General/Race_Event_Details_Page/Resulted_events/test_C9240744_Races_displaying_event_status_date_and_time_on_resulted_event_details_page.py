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
class Test_C9240744_Races_displaying_event_status_date_and_time_on_resulted_event_details_page(Common):
    """
    TR_ID: C9240744
    NAME: <Races>: displaying event status, date and time on resulted event details page
    DESCRIPTION: This test case verifies status, date and time displaying on <Race> result details page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 <Race> events:
    PRECONDITIONS: 1) Resulted, but not settled (In TI tool you should click "Set Results" and "Confirm Results", event should have attribute isResulted="true')
    PRECONDITIONS: 2) Settled (In TI tool you should click "Set Results", "Confirm Results" and "Settle", event should have attributes isResulted="true', isFinished="true")
    PRECONDITIONS: - You should be on <Race> result details page of resulted not settled event
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_events_time_and_status_section(self):
        """
        DESCRIPTION: Verify event's time and status section
        EXPECTED: For Horse racing and Greyhounds:
        EXPECTED: - Section has no title
        EXPECTED: - Event start time and name (e.g. "2:45 Newcastle"), name is displayed in bold
        EXPECTED: - Red colored circle and "Unconfirmed Result" status displayed in bold
        EXPECTED: - Event's start date and time in next format: Full day name, day number, full month name and year (e.g. "Thursday 8th February 2018")
        """
        pass

    def test_002_go_to_the_settled_event_and_verify_time_and_status_section(self):
        """
        DESCRIPTION: Go to the settled event and verify time and status section
        EXPECTED: For Horse racing and Greyhounds:
        EXPECTED: - Section has no title
        EXPECTED: - Event start time and name (e.g. "2:45 Newcastle"), name is displayed in bold
        EXPECTED: - Green colored circle and "Settled Result" status displayed in bold
        EXPECTED: - Event's start date and time in next format: Full day name, day number, full month name and year (e.g. "Thursday 8th February 2018")
        """
        pass
