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
class Test_C2594008_Verify_logic_of_displaying_the_Oxygen_Header_and_Opta_Header(Common):
    """
    TR_ID: C2594008
    NAME: Verify logic of displaying the Oxygen Header and Opta Header
    DESCRIPTION: This test case verifies logic of displaying the Oxygen Header and Opta Header
    PRECONDITIONS: To map Opta Scoreboard to an OB event:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Opta+Scoreboard+mapping+to+an+OB+event
    PRECONDITIONS: To map Visualization to an OB event:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Football+User+Guide
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Navigate to Football Landing page
    """
    keep_browser_open = True

    def test_001_navigate_to_in_play_football_edp_with_mapped_opta_scoreboard(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP with mapped Opta Scoreboard
        EXPECTED: * Event details page is opened
        EXPECTED: * In-Play Opta Scoreboard is available and visible
        EXPECTED: * Opta Header is displayed
        """
        pass

    def test_002_navigate_to_in_play_football_edp_with_mapped_visualization(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP with mapped Visualization
        EXPECTED: * Event details page is opened
        EXPECTED: * Visualization is available and visible
        EXPECTED: * Oxygen header is displayed above Visualization
        """
        pass

    def test_003_navigate_to_in_play_football_edp_with_mapped_grand_parade_scoreboard(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP with mapped Grand Parade Scoreboard
        EXPECTED: * Event details page is opened
        EXPECTED: * Grand Parade Scoreboard is available and visible
        EXPECTED: * Oxygen header is displayed above Grand Parade Scoreboard
        """
        pass

    def test_004_navigate_to_in_play_football_edp_without_any_mapped_scoreboard_or_visualization(self):
        """
        DESCRIPTION: Navigate to In-Play Football EDP without any mapped scoreboard or visualization
        EXPECTED: * Event details page is opened
        EXPECTED: * Oxygen header is displayed
        """
        pass

    def test_005_navigate_to_pre_match_football_edp_with_mapped_opta_scoreboard(self):
        """
        DESCRIPTION: Navigate to Pre-match Football EDP with mapped Opta Scoreboard
        EXPECTED: * Event details page is opened
        EXPECTED: * Pre-Match Opta Scoreboard is available and visible
        EXPECTED: * Opta Header is displayed
        """
        pass

    def test_006_navigate_to_pre_match_football_edp_with_mapped_pre_match_statistic(self):
        """
        DESCRIPTION: Navigate to Pre-match Football EDP with mapped Pre-Match Statistic
        EXPECTED: * Event details page is opened
        EXPECTED: * Pre-Match Statistic is available and visible
        EXPECTED: * Oxygen header is displayed above Pre-Match Statistic
        """
        pass

    def test_007_navigate_to_pre_match_football_edp_without_any_mapped_scoreboard_or_statistic(self):
        """
        DESCRIPTION: Navigate to Pre-match Football EDP without any mapped scoreboard or statistic
        EXPECTED: * Event details page is opened
        EXPECTED: * Oxygen header is displayed
        """
        pass
