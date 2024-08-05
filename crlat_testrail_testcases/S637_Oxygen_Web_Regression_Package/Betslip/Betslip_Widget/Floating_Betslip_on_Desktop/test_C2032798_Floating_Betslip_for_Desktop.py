import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2032798_Floating_Betslip_for_Desktop(Common):
    """
    TR_ID: C2032798
    NAME: Floating Betslip for Desktop
    DESCRIPTION: This test case verifies 2 states of Desktop Betslip: fixed(anchored) and floating.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_verify_the_location_of_betslip_widget(self):
        """
        DESCRIPTION: Verify the location of Betslip widget
        EXPECTED: * Bet Slip widget is located at the top of the last column
        EXPECTED: * Bet Slip widget is expanded by default  (CMS configurable: Widgets->Betslip->'Show Expanded' checkbox)
        """
        pass

    def test_002_verify_bet_slip_widget_view(self):
        """
        DESCRIPTION: Verify Bet Slip widget view
        EXPECTED: Bet Slip widget contains:
        EXPECTED: * 'Bet slip' label
        EXPECTED: * 'Bet slip unlocked' icon next to up/down arrows
        EXPECTED: * up/down facing accordion arrows
        EXPECTED: * tabs: Bet Slip (selected by default); Cash Out; Open Bets; Bet History;
        """
        pass

    def test_003_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Bet Slip widget is NOT anchored to the top of the page
        EXPECTED: * Bet Slip widget becomes hidden when scrolling
        """
        pass

    def test_004_navigate_to_any_other_page_within_an_application(self):
        """
        DESCRIPTION: Navigate to any other page within an application
        EXPECTED: 'Bet slip unlocked' icon remains displayed
        """
        pass

    def test_005_click_on_bet_slip_unlocked_icon(self):
        """
        DESCRIPTION: Click on 'Bet slip unlocked' icon
        EXPECTED: 'Bet slip unlocked' icon changes to 'Bet slip locked' icon
        """
        pass

    def test_006_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Bet Slip widget is anchored to the top of the page
        EXPECTED: * Bet Slip widget remains visible while scrolling
        EXPECTED: * Bet Slip widget overlays 'Favorites' and 'Offer' widgets if available
        EXPECTED: * Bet Slip widget stops before footer area
        """
        pass

    def test_007_navigate_to_any_other_page_within_an_application(self):
        """
        DESCRIPTION: Navigate to any other page within an application
        EXPECTED: 'Bet slip locked' icon remains displayed
        """
        pass

    def test_008_click_on_bet_slip_locked_icon(self):
        """
        DESCRIPTION: Click on 'Bet slip locked' icon
        EXPECTED: * 'Bet slip locked' icon changes to 'Bet slip unlocked' icon
        EXPECTED: * Bet Slip widget appears at the top of the last column above any other available modules
        """
        pass

    def test_009_collapse_bet_slip_widget(self):
        """
        DESCRIPTION: Collapse Bet Slip widget
        EXPECTED: Collapsed Bet Slip widget contains:
        EXPECTED: * 'Bet slip' label
        EXPECTED: * 'Bet slip unlocked/locked' icon next to up/down arrows
        EXPECTED: * down facing accordion arrows
        """
        pass

    def test_010_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps 3-8
        EXPECTED: 
        """
        pass
