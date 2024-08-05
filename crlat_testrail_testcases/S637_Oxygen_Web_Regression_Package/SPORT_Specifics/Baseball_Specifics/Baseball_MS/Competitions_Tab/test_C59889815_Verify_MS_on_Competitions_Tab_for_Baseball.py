import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C59889815_Verify_MS_on_Competitions_Tab_for_Baseball(Common):
    """
    TR_ID: C59889815
    NAME: Verify MS on Competitions Tab for Baseball
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Baseball Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|Run Line|,|Total Runs|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Baseball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line| - "Money Line"
    PRECONDITIONS: * |Run Line (Handicap)| - "Run Line"
    PRECONDITIONS: * |Total Runs (Over/Under)| - "Total Runs"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Money Line
        EXPECTED: • Run Line
        EXPECTED: • Total Runs
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        pass

    def test_003_select_money_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Money Line' in the 'Market Selector' dropdown list
        EXPECTED: • Events will be displayed as per the below conditions
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_004_repeat_step_3_for_the_following_markets_run_line_total_runs(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Run Line
        DESCRIPTION: • Total Runs
        EXPECTED: 
        """
        pass

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_money_line_run_line_total_runs(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Run Line
        DESCRIPTION: • Total Runs
        EXPECTED: Bet should be placed successfully
        """
        pass
