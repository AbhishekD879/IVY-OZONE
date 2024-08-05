import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60079464_Verify_previously_selected_WDW_Market_Template_is_saved_when_user_is_switching_between_Today_Tomorrow_Future_on_Golf_Landing_Page(Common):
    """
    TR_ID: C60079464
    NAME: Verify previously selected ‘WDW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Golf Landing Page
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Golf Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • '2 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' **Coral**
        """
        pass

    def test_002_verify_text_of_the_labels_for_3_ball_betting_in_matches_tab_today(self):
        """
        DESCRIPTION: Verify text of the labels for '3 Ball Betting' in Matches Tab (Today)
        EXPECTED: • The events for the 3 Ball Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3.
        """
        pass

    def test_003_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: 3 Ball Betting)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3.
        EXPECTED: Note:
        EXPECTED: If events are not present for 3 Ball Betting market and if events are present for 2 Ball Betting market then 2 Ball Betting will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_34_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4 for the 'Future' tab
        EXPECTED: 
        """
        pass

    def test_006_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3
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

    def test_008_repeat_steps_1_7_for_the_below_markets_2_ball_betting_expect_step_2(self):
        """
        DESCRIPTION: Repeat steps 1-7 for the below markets
        DESCRIPTION: • 2 Ball Betting (expect step 2)
        EXPECTED: 
        """
        pass

    def test_009_verify_text_of_the_labels_for_2_ball_betting_in_matches_tab_today(self):
        """
        DESCRIPTION: Verify text of the labels for '2 Ball Betting' in Matches Tab (Today)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        """
        pass
