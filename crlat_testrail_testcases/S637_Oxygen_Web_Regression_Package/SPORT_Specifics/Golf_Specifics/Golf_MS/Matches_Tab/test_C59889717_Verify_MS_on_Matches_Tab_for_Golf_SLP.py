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
class Test_C59889717_Verify_MS_on_Matches_Tab_for_Golf_SLP(Common):
    """
    TR_ID: C59889717
    NAME: Verify MS on Matches Tab for Golf SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Golf landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
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
        EXPECTED: • '2 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '2 Ball Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '2 Ball Betting' in 'Market selector' **Coral**
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 2 Ball Betting
        EXPECTED: • 3 Ball Betting
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

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_and_tablet___coral_and_lads__lads__desktop(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (Applicable for mobile and tablet - Coral and Lads & Lads- Desktop)
        EXPECTED: SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        pass

    def test_005_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition page where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Primary market displayed by default in Market switcher dropdown
        """
        pass

    def test_006_repeat_steps_3_5_for_the_following_markets_2_ball_betting(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the following markets:
        DESCRIPTION: • 2 Ball Betting
        EXPECTED: 
        """
        pass

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_2_ball_betting_3_ball_betting(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • 2 Ball Betting
        DESCRIPTION: • 3 Ball Betting
        EXPECTED: Bet should be placed successfully
        """
        pass
