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
class Test_C60075414_Verify_Market_Selector_drop_down_in_Basketball_on_in_Play_page_when_no_events_are_found(Common):
    """
    TR_ID: C60075414
    NAME: Verify 'Market Selector' drop down in Basketball on in-Play page when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in Basketball on in-Play page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No Live events are configured for BasketBall on Inplay Tab
    """
    keep_browser_open = True

    def test_001_navigate_to_basketball_and_click_on_inplay(self):
        """
        DESCRIPTION: Navigate to Basketball and click on Inplay
        EXPECTED: Inplay page is loaded
        """
        pass

    def test_002_verify_displaying_of_market_selector(self):
        """
        DESCRIPTION: Verify displaying of Market Selector
        EXPECTED: • Market Selector dropdown should not be displayed with Arrow pointing downwards
        EXPECTED: • 'There are currently no Live events available' message should be displayed
        """
        pass
