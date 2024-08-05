import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28546_Verify_Sticky_Header_for_Scorecast_Market(Common):
    """
    TR_ID: C28546
    NAME: Verify Sticky Header for Scorecast Market
    DESCRIPTION: This test case verifies sticky header for Scorecast according the story **BMA-4501** Implement sticky headers on Event View and Market View
    DESCRIPTION: NOTE: Story is not yet implemented (30/11/2019), so make sure that it is necessary to test this functionality.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_003_select_football_event_with_handicap_markets_available(self):
        """
        DESCRIPTION: Select Football event with Handicap Markets available
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_tap_on_all_markets_tab(self):
        """
        DESCRIPTION: Tap on 'All markets' tab
        EXPECTED: All available markets are shown
        """
        pass

    def test_005_find_scorecast_section_and_expand_it_if_it_is_not_expanded_by_default(self):
        """
        DESCRIPTION: Find 'Scorecast' section and expand it (if it is not expanded by default)
        EXPECTED: The section is expanded
        """
        pass

    def test_006_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: 
        """
        pass

    def test_007_verify_market_header(self):
        """
        DESCRIPTION: Verify market header
        EXPECTED: The market header is always stuck on the top of the page until the next header reaches the top and sticks instead
        """
        pass
