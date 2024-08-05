import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C874356_Horse_Racing_Bet_Filter(Common):
    """
    TR_ID: C874356
    NAME: Horse Racing Bet Filter
    DESCRIPTION: 
    PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
    PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
    PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
    PRECONDITIONS: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=739471&group_order=asc
    """
    keep_browser_open = True

    def test_001_load_oxygen_app___go_to_horse_racing(self):
        """
        DESCRIPTION: Load Oxygen App -> Go to Horse racing
        EXPECTED: * Horse landing page is opened
        EXPECTED: * 'Bet Filter' link on the Horse Racing header in the right
        """
        pass

    def test_002_tap_bet_filter_link(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link
        EXPECTED: Bet finder page contains:
        EXPECTED: * Text 'BET FILTER ...'
        EXPECTED: * Following Filters groups:
        EXPECTED: * Meetings
        EXPECTED: * Odds
        EXPECTED: * Form
        EXPECTED: * Going (Ground Type)
        EXPECTED: * Digital Tipster Filters
        EXPECTED: * Select Star Rating
        EXPECTED: * --------------------
        EXPECTED: * 'Save selection' button
        EXPECTED: * 'Find bets' button
        """
        pass

    def test_003_verify_meetings_filter(self):
        """
        DESCRIPTION: Verify Meetings filter
        EXPECTED: * 'All meetings' value selected by default
        EXPECTED: * Select any value -> Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"course": "combobox_value"} param
        """
        pass

    def test_004_verify_odds_filter(self):
        """
        DESCRIPTION: Verify Odds filter
        EXPECTED: * Filter contains options:
        EXPECTED: -Odds On
        EXPECTED: -Evens - 7/2
        EXPECTED: -4/1 - 15/2
        EXPECTED: -8/1 - 14/1
        EXPECTED: -16/1 - 28/1
        EXPECTED: -33/1 or Bigger
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"odds": "between selected values"} param
        """
        pass

    def test_005_verify_form_filter(self):
        """
        DESCRIPTION: Verify Form filter
        EXPECTED: * Filter contains options:
        EXPECTED: -Course and Distance Winner (long button, as compared to the rest Form buttons that are 1/2 of this)
        EXPECTED: -Course Winner
        EXPECTED: -Winner Last Time
        EXPECTED: -Placed Last Time
        EXPECTED: -Distance Winner
        EXPECTED: -Winner Within Last 3
        EXPECTED: -Placed Within Last 3
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"filters option (from above)": "Y"} param
        """
        pass

    def test_006_verify_going_ground_type_filter(self):
        """
        DESCRIPTION: Verify Going (Ground Type) filter
        EXPECTED: * Filter contains option: Proven
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"provenGoing": "Y"} param / {"provenGoing": "N"} param
        """
        pass

    def test_007_verify_digital_tipster_filters_filter(self):
        """
        DESCRIPTION: Verify Digital Tipster Filters filter
        EXPECTED: * Filter contains options:
        EXPECTED: -Selection
        EXPECTED: -Alternative
        EXPECTED: -Each-Way
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "S"} param / {"supercomputerSelection": "A"} param / {"supercomputerSelection": "E"} param
        """
        pass

    def test_008_verify_select_star_rating_filter(self):
        """
        DESCRIPTION: Verify Select Star Rating filter
        EXPECTED: * Filter contains options:
        EXPECTED: - 5 starts (unselected by default)
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"starRating": "number of selected stars"} param
        """
        pass

    def test_009__select_any_options_from_several_filters_groups_and_tapclick__save_selection_button_refresh_page(self):
        """
        DESCRIPTION: * Select any options from several filters groups and tap/click  'Save selection' button
        DESCRIPTION: * Refresh page
        EXPECTED: All selected options are saved
        """
        pass

    def test_010_tapclick_find_bets_button_and_verify_results_page(self):
        """
        DESCRIPTION: Tap/click 'Find bets' button and verify results page
        EXPECTED: * Displayed selections match the filters parameters
        EXPECTED: * The following details are provided:
        EXPECTED: -Jockey
        EXPECTED: -Trainer
        EXPECTED: -Form
        EXPECTED: -Price
        EXPECTED: -Silks
        EXPECTED: -Time selection is running
        EXPECTED: -Runner Number
        EXPECTED: -Draw
        EXPECTED: * Filter 'Sort by TIME/ODDS' on the header (sorted 'by time' by default) sorts displayed selection either by time or odds
        """
        pass
