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
class Test_C59939754_Verify_WDW_MT_on_Competitions_Tab_for_Golf(Common):
    """
    TR_ID: C59939754
    NAME: Verify 'WDW’ MT on Competitions Tab for Golf
    DESCRIPTION: This test case verifies the behaviour of  ‘WW market’ Template on Competitions Tab for Golf
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf -> 'Click on Competition Tab'
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

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • '2 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '2 Ball Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '2 Ball Betting' in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 2 Ball Betting
        EXPECTED: • 3 Ball Betting
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

    def test_004_verify_displaying_of_preplay_and_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay and Inplay events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • 3 Ball Betting (Preplay and Inplay market)
        EXPECTED: • 2 Ball Betting (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        pass

    def test_005_verify_text_of_the_labels_for_3_ball_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '3 Ball Betting'
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3.
        """
        pass

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        pass

    def test_007_verify_ga_tracking_for_the_3_ball_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the '3 Ball Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "3 Ball Betting"
        EXPECTED: categoryID: "18"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        pass

    def test_008_repeat_3_7_steps_for_the_below_market2_ball_betting_expect_step_5(self):
        """
        DESCRIPTION: Repeat 3-7 steps for the below market
        DESCRIPTION: 2 Ball Betting (Expect Step 5)
        EXPECTED: 
        """
        pass

    def test_009_verify_text_of_the_labels_for_2_ball_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '2 Ball Betting'
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        """
        pass
