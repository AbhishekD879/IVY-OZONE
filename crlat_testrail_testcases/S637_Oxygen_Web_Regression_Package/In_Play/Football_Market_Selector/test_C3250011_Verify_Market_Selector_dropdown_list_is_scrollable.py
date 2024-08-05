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
class Test_C3250011_Verify_Market_Selector_dropdown_list_is_scrollable(Common):
    """
    TR_ID: C3250011
    NAME: Verify 'Market Selector' dropdown list is scrollable
    DESCRIPTION: This test case verifies the content of 'Market Selector' dropdown list is scrollable
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    PRECONDITIONS: 4. Be aware that several markets are available in the 'Market Selector' dropdown list
    """
    keep_browser_open = True

    def test_001_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: - 'Market Selector' dropdown list opens
        EXPECTED: - The list of markets is displayed
        EXPECTED: - The chevron near 'Change' button is pointed downwards
        """
        pass

    def test_002_verify_the_scroll_appears_inside_the_dropdown_list_if_the_list_of_markets_exceeds_the_dropdown_height(self):
        """
        DESCRIPTION: Verify the scroll appears inside the dropdown list if the list of markets exceeds the dropdown height
        EXPECTED: - Content of 'Market Selector' dropdown list becomes scrollable
        EXPECTED: - Sidebar is displayed
        """
        pass

    def test_003_scroll_till_the_end_of_markets_list_inside_dropdown(self):
        """
        DESCRIPTION: Scroll till the end of markets list inside dropdown
        EXPECTED: - Content is scrolled till the last drop down option
        EXPECTED: - The whole page becomes scrollable afterwards
        """
        pass

    def test_004_scroll_the_content_up(self):
        """
        DESCRIPTION: Scroll the content up
        EXPECTED: Content is scrollable
        """
        pass

    def test_005_select_any_option_from_dropdown(self):
        """
        DESCRIPTION: Select any option from dropdown
        EXPECTED: Option is selected
        """
        pass

    def test_006_tap_on_the_change_button_again_and_scroll_the_content(self):
        """
        DESCRIPTION: Tap on the 'Change' button again and scroll the content
        EXPECTED: - 'Market Selector' dropdown list opens
        EXPECTED: - Content is scrollable
        EXPECTED: - The chevron near 'Change' button is pointed downwards
        """
        pass

    def test_007_repeat_steps_1_6_on_football_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-6 on 'Football Landing Page' -> 'In-Play' tab
        EXPECTED: 
        """
        pass
