import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C15389149_LadbrokesLogic_of_Tennis_Scoreboard_Visualization_displaying(Common):
    """
    TR_ID: C15389149
    NAME: [Ladbrokes]Logic of Tennis Scoreboard/Visualization displaying
    DESCRIPTION: This test case verifies logic of Tennis Scoreboard or Visualization displaying based on available mapped data on Ladbrokes
    PRECONDITIONS: Application is loaded
    PRECONDITIONS: Make sure you have LIVE Tennis events with:
    PRECONDITIONS: * first - available Scoreboard (BWIN(OPTA)) with mapped Fall Backs
    PRECONDITIONS: * second - available Scoreboard (BWIN(OPTA)), ​with no mapped Fall Backs
    PRECONDITIONS: * third - no available Scoreboard (BWIN(OPTA)) and mapped Fall Backs
    PRECONDITIONS: **RULE**: The sequence of scoreboards to display to user ( only one is displayed):
    PRECONDITIONS: 1. **BWIN(OPTA)** - 'datafabric' request in XHR  (NOT AVAILABLE ON PROD), can be mapped by Final Space team
    PRECONDITIONS: 2. **Fall Backs** scoreboards (Not Implemented yet for Tennis)
    PRECONDITIONS: NOTE: **Visualizations (IMG)** and **Grand Parade** are not available for Ladbrokes
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_first_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of first event
        EXPECTED: Event Details Page is opened
        EXPECTED: Tennis BWIN(OPTA) Scoreboard is shown
        """
        pass

    def test_002_navigate_to_event_details_page_of_second_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of second event
        EXPECTED: Event Details Page is opened
        EXPECTED: Tennis BWIN(OPTA) Scoreboard is shown
        """
        pass

    def test_003_navigate_to_event_details_page_of_third_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of third event
        EXPECTED: Event Details Page is opened
        EXPECTED: Fall Backs Scoreboard is shown
        """
        pass
