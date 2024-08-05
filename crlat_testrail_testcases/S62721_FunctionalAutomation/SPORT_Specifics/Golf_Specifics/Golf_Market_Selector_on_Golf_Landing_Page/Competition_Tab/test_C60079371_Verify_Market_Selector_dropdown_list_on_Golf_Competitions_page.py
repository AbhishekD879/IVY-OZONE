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
class Test_C60079371_Verify_Market_Selector_dropdown_list_on_Golf_Competitions_page(Common):
    """
    TR_ID: C60079371
    NAME: Verify 'Market Selector' dropdown list on Golf Competitions page
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Golf Competitions page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Competitions page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
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
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • '3 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' **Coral**
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 3 Ball Betting
        EXPECTED: • 2 Ball Betting
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        pass

    def test_003_select_3_ball_betting_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select '3 Ball Betting' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_004_repeat_step_3_for_the_following_markets_2_ball_betting(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • 2 Ball Betting
        EXPECTED: 
        """
        pass
