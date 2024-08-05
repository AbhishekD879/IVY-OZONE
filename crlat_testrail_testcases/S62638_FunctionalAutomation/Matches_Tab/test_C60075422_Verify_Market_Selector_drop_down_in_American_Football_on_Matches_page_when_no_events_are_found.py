import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C60075422_Verify_Market_Selector_drop_down_in_American_Football_on_Matches_page_when_no_events_are_found(Common):
    """
    TR_ID: C60075422
    NAME: Verify 'Market Selector' drop down in American Football on Matches page when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in American Football on Matches page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No Live events are configured for Tennis on Matches Tab
    """
    keep_browser_open = True

    def test_001_navigate_to_american_football(self):
        """
        DESCRIPTION: Navigate to American Football
        EXPECTED: Matches Tab is displayed by default
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
