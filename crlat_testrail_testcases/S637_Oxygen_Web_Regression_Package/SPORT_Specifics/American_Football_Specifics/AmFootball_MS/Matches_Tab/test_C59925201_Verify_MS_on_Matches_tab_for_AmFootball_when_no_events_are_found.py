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
class Test_C59925201_Verify_MS_on_Matches_tab_for_AmFootball_when_no_events_are_found(Common):
    """
    TR_ID: C59925201
    NAME: Verify MS on Matches tab for Am.Football when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in American Football on Matches page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No events are configured for Am football on Matches Tab
    """
    keep_browser_open = True

    def test_001_navigate_to_american_football(self):
        """
        DESCRIPTION: Navigate to American Football
        EXPECTED: Matches Tab is displayed by default
        """
        pass

    def test_002_verify_displaying_of_market_selectortoday_tab(self):
        """
        DESCRIPTION: Verify displaying of Market Selector(Today Tab)
        EXPECTED: • Market Selector dropdown should not be displayed with Arrow pointing downwards
        EXPECTED: • 'No events found' message should be displayed
        """
        pass

    def test_003_repeat_step2_for_tomorrow_and_future_tab_steps_12_and_3_are_applicable_for_desktop(self):
        """
        DESCRIPTION: Repeat Step2 for Tomorrow and Future Tab (Steps 1,2 and 3 are applicable for desktop)
        EXPECTED: 
        """
        pass

    def test_004_verify_matches_tab_in_mobile(self):
        """
        DESCRIPTION: Verify Matches Tab in Mobile
        EXPECTED: Matches Tab should not display when there are no events
        """
        pass