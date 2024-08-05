import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1901954_Tracking_of_all_sub_accordions_Shots_Shots_on_Goal_Tackles_Assist_To_Get_a_Card(Common):
    """
    TR_ID: C1901954
    NAME: Tracking of all sub-accordions: Shots, Shots on Goal, Tackles, Assist & To Get a Card
    DESCRIPTION: This Test Case verifies tracking in the Google Analytics data Layer of all sub-accordions: Shots, Shots on Goal, Tackles, Assist & To Get a Card.
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Featured tab is opened
        """
        pass

    def test_002_navigate_to_inplay_and_select_event_with_configured_player_markets(self):
        """
        DESCRIPTION: Navigate to InPlay and select Event with configured Player Markets
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_select_all_markets_tab(self):
        """
        DESCRIPTION: Select All Markets tab
        EXPECTED: - All Markets tab is opened
        EXPECTED: - '#YourCall Player Markets' section is displayed
        """
        pass

    def test_004_expandcollapse_sub_accordions_with_markets_names_shots_shots_on_goal_tackles_assist__to_get_a_card(self):
        """
        DESCRIPTION: Expand/Collapse sub-accordions with Markets names: Shots, Shots on Goal, Tackles, Assist & To Get a Card.
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'ds in play player stat',
        EXPECTED: 'eventLabel' : '<< ACTION >>' //e.g. expand accordion - shots, collapse accordion - shots, expand accordion - shots on goal, etc.
        EXPECTED: })
        """
        pass
