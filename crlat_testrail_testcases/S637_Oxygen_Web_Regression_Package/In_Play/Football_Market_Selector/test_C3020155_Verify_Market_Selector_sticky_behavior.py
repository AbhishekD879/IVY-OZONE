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
class Test_C3020155_Verify_Market_Selector_sticky_behavior(Common):
    """
    TR_ID: C3020155
    NAME: Verify 'Market Selector'  sticky behavior
    DESCRIPTION: This test case verifies the sticky behavior of 'Market Selector'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that the Market selector becomes unsticky when the user reaches the Upcoming section
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    """
    keep_browser_open = True

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: * Market selector remains at the top of the scrolling page
        EXPECTED: * Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        pass

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: * Market selector remains at the top of the scrolling page
        EXPECTED: * Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        pass

    def test_003_repeat_steps_1_2_on_football_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-2 on 'Football Landing Page' -> 'In-Play' tab
        EXPECTED: 
        """
        pass
