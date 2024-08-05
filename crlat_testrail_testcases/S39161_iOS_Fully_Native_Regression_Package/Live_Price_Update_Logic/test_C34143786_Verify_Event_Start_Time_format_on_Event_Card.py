import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C34143786_Verify_Event_Start_Time_format_on_Event_Card(Common):
    """
    TR_ID: C34143786
    NAME: Verify Event Start Time format on Event Card
    DESCRIPTION: This test case verifies Start time format for Event Cards with Start time.
    PRECONDITIONS: * App is installed and launched
    PRECONDITIONS: * Event Card in opened
    PRECONDITIONS: * Event Card has a start time
    PRECONDITIONS: Scope:
    PRECONDITIONS: * All Live Prices on Application, for all modules & sports
    """
    keep_browser_open = True

    def test_001__for_nearby_events_start_date_in_today_or_tomorrow(self):
        """
        DESCRIPTION: * For nearby Events (start date in today or tomorrow)
        EXPECTED: * Start Time format: 'hh:mm', 'Today/Tomorrow'
        """
        pass

    def test_002__for_event_starts_later_than_tomorrow(self):
        """
        DESCRIPTION: * For Event starts later than tomorrow
        EXPECTED: * Start Time format: 'hh:mm', 'dd', 'Month'  (Month should be abbreviated to the first 3 letters, E.G December should be displayed as Dec)
        """
        pass
