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
class Test_C59925200_Verify_MS_on_Inplay_tab_for_Basketball_when_no_events_are_found(Common):
    """
    TR_ID: C59925200
    NAME: Verify MS on Inplay tab for Basketball when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in Basketball on in-Play page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No Live events are configured for BasketBall on Inplay Tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
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
