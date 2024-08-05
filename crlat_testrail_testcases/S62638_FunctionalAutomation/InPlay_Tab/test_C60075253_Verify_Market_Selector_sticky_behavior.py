import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C60075253_Verify_Market_Selector_sticky_behavior(Common):
    """
    TR_ID: C60075253
    NAME: Verify 'Market Selector'  sticky behavior
    DESCRIPTION: This test case verifies the sticky behavior of 'Market Selector'
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Choose the 'Basketball' tab
    PRECONDITIONS: 3. Navigate to the 'In-Play' page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that the Market selector becomes unsticky when the user reaches the Upcoming section
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB using the following market Templates:
    PRECONDITIONS: |Money Line (WW)| - "Money Line"
    PRECONDITIONS: |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: |Half Total Points (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Mobile/Tablet:
        EXPECTED: • Market selector remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        pass

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: • Market selector remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        pass
