import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C874349_CORAL_ONLY_Football_Pre_Match_Statistic__SportsRadar(Common):
    """
    TR_ID: C874349
    NAME: [CORAL ONLY] Football Pre-Match Statistic - SportsRadar
    DESCRIPTION: This test case verifies pre-match statistic slides
    PRECONDITIONS: Make sure you have pre-match Football event with available pre-match statistics
    PRECONDITIONS: Availability of Pre-Match statistic can checked using the following link:
    PRECONDITIONS: https://vis-tst2-coral.symphony-solutions.eu/is-stats/<OpenBet_event_ID>
    PRECONDITIONS: Site Serve Events Mapping to Sport Radar
    PRECONDITIONS: https://spark-br.symphony-solutions.eu/mapper/#/site-serve-to-sport-radar
    PRECONDITIONS: How to map pre-match statistic: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Football+Pre-match+Statistics
    PRECONDITIONS: Pre-match statistic can also be mapped in Mapper tool>Football>SportRadar events
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_with_available_pre_match_statistics(self):
        """
        DESCRIPTION: Navigate to Event Details page of event with available pre-match statistics
        EXPECTED: * Football widget with pre-match statistics is shown
        EXPECTED: * Head to Head  slide is opened by default
        EXPECTED: Notes:
        EXPECTED: * if event has less than three Head to Head stats results then slide with Over/Under statistic is displayed by default
        EXPECTED: * if statistic for the whole slide is absent then slide is not shown at all
        """
        pass

    def test_002_verify_pre_match_header(self):
        """
        DESCRIPTION: Verify Pre-match Header
        EXPECTED: Pre-match Header contains data in the following order:
        EXPECTED: * Home Team Name
        EXPECTED: * Away Team Name
        """
        pass

    def test_003_verify_the_view_of_line_ups_if_available(self):
        """
        DESCRIPTION: Verify the view of Line Ups (if available)
        EXPECTED: * List of Home team players' numbers and names are displayed from the left side under Home team name
        EXPECTED: * List of Away team players' numbers and names are displayed from the right side under Away team name
        EXPECTED: * Vertical white divider is displayed in the middle of slide
        """
        pass

    def test_004_verify_the_view_of_head_to_head_results(self):
        """
        DESCRIPTION: Verify the view of Head to Head results
        EXPECTED: * **HEAD TO HEAD - CURRENT COMPETITION** text is displayed
        EXPECTED: * At least 1 and maximum 5 results of last Head to Head meeting are dislayed, divided by vertical line
        """
        pass

    def test_005_navigate_to_slide_with_overunder_statistic(self):
        """
        DESCRIPTION: Navigate to slide with **Over/Under statistic**
        EXPECTED: Slide with Over/Under statistic is displayed
        """
        pass

    def test_006_verify_content_of_slide_with_overunder_statistic(self):
        """
        DESCRIPTION: Verify content of slide with Over/Under statistic
        EXPECTED: * Over/Under statistic top bar selector
        EXPECTED: * **OVER/UNDERS - CURRENT COMPETITION** label
        EXPECTED: * Under/Over information graphs for both teams
        """
        pass

    def test_007_verify_overunder_statistic_top_bar_selector(self):
        """
        DESCRIPTION: Verify Over/Under statistic top bar selector
        EXPECTED: * On the top of the slide the following selections **0.5**, **1.5**, **2.5**, **3.5** are displayed
        EXPECTED: * **Goals** label is displayed next to each selection
        EXPECTED: * White indicator is displayed beneath **2.5** selection by default
        """
        pass

    def test_008_verify_general_overunder_graphs_displaying(self):
        """
        DESCRIPTION: Verify general Over/Under graphs displaying
        EXPECTED: * Bars that consist of blue and red parts are shown for both teams
        EXPECTED: * Blue part corresponds to percentage of Over matches, red part - to Under
        EXPECTED: * Percentage of Over matches is shown on the blue part of the bar for corresponding team, number of matches is shown below the bar
        EXPECTED: * Percentage of Under matches is shown on the red part of the bar for corresponding team, number of matches is shown below the bar
        """
        pass

    def test_009_switch_between_selectors(self):
        """
        DESCRIPTION: Switch between selectors
        EXPECTED: * White indicator is displayed under selected option
        EXPECTED: * Text of selected option gets focus, all other selections become grayed out
        EXPECTED: * Over/Under graphs are shown for selected option for both teams
        """
        pass

    def test_010_verify_the_view_of_latest_form(self):
        """
        DESCRIPTION: Verify the view of Latest Form
        EXPECTED: * **LATEST FORM - ALL COMPETITIONS** title is shown
        EXPECTED: * History of latest results (max value - 6 for each team) is shown in boxes
        """
        pass
