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
class Test_C60075267_Verify_Market_Selector_drop_down_in_American_Football_on_Competitions_page_when_no_events_are_found(Common):
    """
    TR_ID: C60075267
    NAME: Verify 'Market Selector' drop down in American Football on Competitions page when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in American Football on Competitions page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No Live events are configured for amercian Football on competition page
    """
    keep_browser_open = True

    def test_001_navigate_to_american_football_and_click_on_competition_page(self):
        """
        DESCRIPTION: Navigate to American Football and click on Competition Page
        EXPECTED: Competition page is loaded
        """
        pass

    def test_002_verify_displaying_of_market_selector(self):
        """
        DESCRIPTION: Verify displaying of Market Selector
        EXPECTED: • Market Selector dropdown should not be displayed with Arrow pointing downwards
        EXPECTED: • 'No events found' message should be displayed
        """
        pass
