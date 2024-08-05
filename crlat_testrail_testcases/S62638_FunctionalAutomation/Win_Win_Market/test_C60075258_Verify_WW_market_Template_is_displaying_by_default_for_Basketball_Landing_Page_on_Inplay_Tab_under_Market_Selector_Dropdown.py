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
class Test_C60075258_Verify_WW_market_Template_is_displaying_by_default_for_Basketball_Landing_Page_on_Inplay_Tab_under_Market_Selector_Dropdown(Common):
    """
    TR_ID: C60075258
    NAME: Verify ‘WW market’ Template is displaying by default for Basketball  Landing Page on Inplay Tab under Market Selector Dropdown
    DESCRIPTION: This test case verifies displaying of ‘WW market’ Template is displaying by default for Basketball Landing Page on Inplay Tab under Market Selector Dropdown
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball -> 'Click on Inplay Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money line(WW)| - "Money line"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: * The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: Desktop:
        EXPECTED: * The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change Market' button is placed next to 'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: * 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        pass

    def test_002_verify_text_of_the_labels_for_money_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Money Line'
        EXPECTED: • The events for the Money Line market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        pass

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        pass

    def test_004_verify_displaying_of_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Inplay events
        EXPECTED: Only Inplay events should be displayed
        """
        pass

    def test_005_verify_ga_tracking_for_the_money_line(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Money Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Money Line"
        EXPECTED: categoryID: "6"
        EXPECTED: })
        """
        pass
