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
class Test_C60075496_Verify_Market_Selector_dropdown_list_on_Ice_Hockey_Competition_page(Common):
    """
    TR_ID: C60075496
    NAME: Verify 'Market Selector' dropdown list on Ice Hockey Competition page
    DESCRIPTION: This testcase verifies  the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|60 Minute betting|,|Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|Money Line (WW)|- Money Line
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- 60 Minute Betting
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
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

    def test_002_verify_the_competition_page(self):
        """
        DESCRIPTION: Verify the Competition page
        EXPECTED: One of the below market will be selected by default according to which events will be displayed with odds value.
        EXPECTED: • Puck Line
        EXPECTED: • 60 Minute Betting
        EXPECTED: • Total Goals 2-way
        EXPECTED: >If a market is only for Preplay event then only Preplay events will be displayed with odds
        EXPECTED: >If a market is only for Preplay event then only Preplay events will be displayed with odds
        EXPECTED: > If a market is having both Preplay and Inplay event then both inplay and Preplay events will be displayed with odds
        """
        pass

    def test_003_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets:
        EXPECTED: . Money Line
        EXPECTED: • Puck Line
        EXPECTED: • 60 Minute Betting
        EXPECTED: • Total Goals 2-way
        """
        pass

    def test_004_select_money_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Money Line' in the 'Market Selector' dropdown list
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Money Line (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        pass

    def test_005_repeat_step_3_for_the_following_markets_puck_line_preplay_and_inplay_market_60_minute_betting_preplay_and_inplay_market_total_goals_2_way_preplay_and_inplay_market(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Puck Line (Preplay and Inplay market)
        DESCRIPTION: • 60 Minute Betting (Preplay and Inplay market)
        DESCRIPTION: • Total Goals 2-way (Preplay and Inplay market)
        EXPECTED: 
        """
        pass
