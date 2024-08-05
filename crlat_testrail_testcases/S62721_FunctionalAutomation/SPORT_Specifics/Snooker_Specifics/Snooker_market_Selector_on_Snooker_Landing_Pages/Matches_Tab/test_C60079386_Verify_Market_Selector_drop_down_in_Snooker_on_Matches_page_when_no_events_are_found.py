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
class Test_C60079386_Verify_Market_Selector_drop_down_in_Snooker_on_Matches_page_when_no_events_are_found(Common):
    """
    TR_ID: C60079386
    NAME: Verify 'Market Selector' drop down in Snooker on Matches page when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in Snooker on Matches page when no events are found
    PRECONDITIONS: No Live events are configured for Snooker on Matches Tab
    """
    keep_browser_open = True

    def test_001_navigate_to_snooker_and_click_on_matches(self):
        """
        DESCRIPTION: Navigate to Snooker and click on Matches
        EXPECTED: Matches Today page is loaded
        """
        pass

    def test_002_verify_displaying_of_market_selector(self):
        """
        DESCRIPTION: Verify displaying of Market Selector
        EXPECTED: • Market Selector dropdown should not be displayed with Arrow pointing downwards
        EXPECTED: • 'No events found' message should be displayed
        """
        pass

    def test_003_repeat_step2_for_tomorrow_and_future_tab(self):
        """
        DESCRIPTION: Repeat Step2 for Tomorrow and Future Tab
        EXPECTED: 
        """
        pass
