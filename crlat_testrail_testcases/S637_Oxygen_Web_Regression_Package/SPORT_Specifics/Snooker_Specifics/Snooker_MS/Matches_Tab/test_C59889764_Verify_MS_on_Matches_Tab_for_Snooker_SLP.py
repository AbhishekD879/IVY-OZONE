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
class Test_C59889764_Verify_MS_on_Matches_Tab_for_Snooker_SLP(Common):
    """
    TR_ID: C59889764
    NAME: Verify MS on Matches Tab for Snooker SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown in Matches tab for Snooker landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|Handicap|,|Total Frames|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: |Match Handicap (Handicap)| - "Handicap"
    PRECONDITIONS: |Total Frames Over/Under (Over/Under)| - "Total Frames"
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
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Mach betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Handicap
        EXPECTED: • Total Frames
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        pass

    def test_003_select_handicap_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Handicap' in the 'Market Selector' dropdown list
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

    def test_006_repeat_steps_3_5_for_the_following_markets_handicap_total_frames(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the following markets:
        DESCRIPTION: • Handicap
        DESCRIPTION: • Total Frames
        EXPECTED: 
        """
        pass

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_handicap_total_frames(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Handicap
        DESCRIPTION: • Total Frames
        EXPECTED: Bet should be placed successfully
        """
        pass
