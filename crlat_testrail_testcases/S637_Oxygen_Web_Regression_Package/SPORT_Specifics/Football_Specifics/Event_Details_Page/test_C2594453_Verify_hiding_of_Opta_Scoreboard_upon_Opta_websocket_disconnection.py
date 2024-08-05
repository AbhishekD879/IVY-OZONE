import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2594453_Verify_hiding_of_Opta_Scoreboard_upon_Opta_websocket_disconnection(Common):
    """
    TR_ID: C2594453
    NAME: Verify hiding of Opta Scoreboard upon Opta websocket disconnection
    DESCRIPTION: to update: clear instruction on how to perform this test
    DESCRIPTION: This test case verifies receiving custom event from Opta scoreboard when Opta websocket has been disconnected for 30sec and displaying Oxygen header instead alongside with visualization/Grand Parade scoreboard (whatever is mapped to event, if anything).
    DESCRIPTION: Note: Cannot be automated as manual assistance needed to complete all steps
    PRECONDITIONS: Several Football events should be configured in the following way:
    PRECONDITIONS: 1) in-play event with Opta Scoreboard and Oxygen Visualization mapped
    PRECONDITIONS: 2) in-play event with Opta Scoreboard and Grand Parade scoreboard mapped
    PRECONDITIONS: 3) in-play event with Opta Scoreboard mapped
    PRECONDITIONS: To map Opta Scoreboard to an OB event:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Opta+Scoreboard+mapping+to+an+OB+event
    PRECONDITIONS: To map Visualization to an OB event:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Football+User+Guide
    PRECONDITIONS: **NOTE! To trigger Opta websocket disconnection contact FinalSpace team.**
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Navigate to Football Landing page
    """
    keep_browser_open = True

    def test_001_navigate_to_in_play_football_edp_with_mapped_opta_scoreboard_and_oxygen_visualization(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP with mapped Opta Scoreboard and Oxygen Visualization
        EXPECTED: Event details page is opened with In-Play Opta Scoreboard displayed
        """
        pass

    def test_002_trigger_opta_websocket_disconnection_and_wait_30_sec(self):
        """
        DESCRIPTION: Trigger Opta websocket disconnection and wait 30 sec
        EXPECTED: * Custom event **hideScoreboardComponent** is received in console
        EXPECTED: * Opta Scoreboard is hidden
        EXPECTED: * Oxygen header is shown together with Oxygen Visualization
        """
        pass

    def test_003_navigate_to_in_play_football_edp_with_mapped_opta_scoreboard_and_grand_parade_scoreboard(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP with mapped Opta Scoreboard and Grand Parade scoreboard
        EXPECTED: Event details page is opened with In-Play Opta Scoreboard displayed
        """
        pass

    def test_004_trigger_opta_websocket_disconnection_and_wait_30_sec(self):
        """
        DESCRIPTION: Trigger Opta websocket disconnection and wait 30 sec
        EXPECTED: * Custom event **hideScoreboardComponent** is received in console
        EXPECTED: * Opta Scoreboard is hidden
        EXPECTED: * Oxygen header is shown together with Grand Parade scoreboard
        """
        pass

    def test_005_navigate_to_in_play_football_edp_with_mapped_opta_scoreboard(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP with mapped Opta Scoreboard
        EXPECTED: Event details page is opened with In-Play Opta Scoreboard displayed
        """
        pass

    def test_006_trigger_opta_websocket_disconnection_and_wait_30_sec(self):
        """
        DESCRIPTION: Trigger Opta websocket disconnection and wait 30 sec
        EXPECTED: * Custom event **hideScoreboardComponent** is received in console
        EXPECTED: * Opta Scoreboard is hidden
        EXPECTED: * Oxygen header is shown
        """
        pass
