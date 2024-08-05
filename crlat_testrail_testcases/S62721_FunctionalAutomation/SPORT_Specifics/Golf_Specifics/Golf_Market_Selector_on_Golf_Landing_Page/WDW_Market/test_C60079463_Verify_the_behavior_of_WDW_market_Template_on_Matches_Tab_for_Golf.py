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
class Test_C60079463_Verify_the_behavior_of_WDW_market_Template_on_Matches_Tab_for_Golf(Common):
    """
    TR_ID: C60079463
    NAME: Verify the behavior of  ‘WDW market’ Template on Matches Tab for Golf
    DESCRIPTION: This test case verifies the behavior of  ‘WW market’ Template on Matches Tab for Golf
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |3 Ball Betting| - "3 Ball Betting"
    PRECONDITIONS: |2 Ball Betting| - "2 Ball Betting"
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 3 Ball Betting
        EXPECTED: • 2 Ball Betting
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

    def test_004_verify_text_of_the_labels_for_3_ball_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '3 Ball Betting'
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1','2','3' and corresponding Odds are present under Label 1 2 3
        """
        pass

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        pass

    def test_006_verify_ga_tracking_for_the_3_ball_betting(self):
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

    def test_007_repeat_steps_1_6_for_the_below_market_2_ball_bettingexcept_step_4(self):
        """
        DESCRIPTION: Repeat steps 1-6 for the below market:
        DESCRIPTION: • 2 Ball Betting(Except step 4)
        EXPECTED: 
        """
        pass

    def test_008_select_2_ball_betting_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select '2 Ball Betting' in the 'Market Selector' dropdown list
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1','Tie','2' and corresponding Odds are present under Label 1 Tie 2
        """
        pass
