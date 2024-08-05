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
class Test_C1317509_CORALLogic_of_Tennis_Scoreboard_Visualization_displaying(Common):
    """
    TR_ID: C1317509
    NAME: [CORAL]Logic of Tennis Scoreboard/Visualization displaying
    DESCRIPTION: This test case verifies logic of Tennis Scoreboard or Visualization displaying based on available mapped data
    PRECONDITIONS: Application is loaded
    PRECONDITIONS: Make sure you have LIVE Tennis events with:
    PRECONDITIONS: * first - available Scoreboard (BWIN(OPTA)) but unmapped Visualizations (IMG)
    PRECONDITIONS: * second - available Scoreboard (BWIN(OPTA)), ​with mapped Visualization(IMG) but without data to visualize
    PRECONDITIONS: * third - available Scoreboard (BWIN(OPTA)) and mapped Visualizations(IMG)
    PRECONDITIONS: * forth - not available Scoreboard (BWIN(OPTA)) and mapped Visualizations(IMG)
    PRECONDITIONS: * fifth - available all kinds of Scoreboards: Visualizations(IMG), BWIN(OPTA), Fall Backs, Grand Parade
    PRECONDITIONS: **RULE**: The sequence of scoreboards to display to user ( only one is displayed):
    PRECONDITIONS: 1. **Visualizations (IMG)** - 'coral-vis-tennis' request in XHR
    PRECONDITIONS: https://coral-vis-rtc-stg2.symphony-solutions.eu/#/sports/tennis/provider/img/tournaments/all/events?_k=0773mz
    PRECONDITIONS: credentials:mapperstg2/mapperstage
    PRECONDITIONS: 2. **BWIN(OPTA)** - 'datafabric' request in XHR  (NOT AVAILABLE ON PROD), can be mapped by Final Space team
    PRECONDITIONS: 3. **Fall Backs** scoreboards (Not Implemented yet for Tennis)
    PRECONDITIONS: 4. **Grand Parade** - (set in CMS(System config>VisualisationConfig) and displayed only when others scoreboards are missing)
    PRECONDITIONS: **Examples of scoreboards are attached to the test case**
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_first_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of first event
        EXPECTED: Event Details Page is opened
        EXPECTED: Tennis Scoreboard is shown
        """
        pass

    def test_002_navigate_to_event_details_page_of_second_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of second event
        EXPECTED: Event Details Page is opened
        EXPECTED: Tennis Scoreboard is shown
        """
        pass

    def test_003_navigate_to_event_details_page_of_third_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of third event
        EXPECTED: Event Details Page is opened
        EXPECTED: Scoreboard is NOT shown
        EXPECTED: Visualization iframe with 'Match Live' (default) and 'Match Statistics' tabs is shown
        """
        pass

    def test_004_navigate_to_event_details_page_of_forth_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of forth event
        EXPECTED: Event Details Page is opened
        EXPECTED: Visualization iframe with 'Match Live' (default) and 'Match Statistics' tabs is shown
        """
        pass

    def test_005_navigate_to_event_details_page_of_fifth_event(self):
        """
        DESCRIPTION: Navigate to Event Details Page of fifth event
        EXPECTED: Event Details Page is opened
        EXPECTED: Visualization iframe with 'Match Live' (default) and 'Match Statistics' tabs is shown
        """
        pass
