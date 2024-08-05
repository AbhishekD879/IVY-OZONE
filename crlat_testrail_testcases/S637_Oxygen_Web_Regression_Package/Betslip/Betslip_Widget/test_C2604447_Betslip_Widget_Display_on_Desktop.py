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
class Test_C2604447_Betslip_Widget_Display_on_Desktop(Common):
    """
    TR_ID: C2604447
    NAME: Betslip Widget Display on Desktop
    DESCRIPTION: This test case verifies view of BetSlip widget displaying with no added selections on Desktop version
    DESCRIPTION: BetSlip redesigns: BMA-36921, BMA-39081
    PRECONDITIONS: Desktop
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on desktop
        EXPECTED: 1. Homepage is opened
        EXPECTED: 2.  Bet Slip widget is located at the top of the last column
        EXPECTED: 3.  Bet Slip widget is expanded by default and contains:
        EXPECTED: * 'Bet slip unlocked' icon next to up/down arrows
        EXPECTED: * Up/down facing accordion arrows
        EXPECTED: * Tabs: 'BET SLIP' (selected by default); 'CASH OUT'; 'OPEN BETS'; 'BET HISTORY';
        EXPECTED: * Message "You have no selections in the slip." displayed within Betslip content area
        EXPECTED: **FROM OX100**
        EXPECTED: 1. Homepage is opened
        EXPECTED: 2.  Bet Slip widget is located at the top of the last column
        EXPECTED: 3.  Bet Slip widget contains:
        EXPECTED: * Tabs: 'BETSLIP' (selected by default); 'MY BETS'
        EXPECTED: * Message "Your betslip is empty" at the top and for CORAL message below "Please add one or more selections to place a bet" displayed within Betslip content area
        """
        pass

    def test_002_tap_my_bets_tab(self):
        """
        DESCRIPTION: Tap 'MY BETS' tab
        EXPECTED: New tabs are visible:
        EXPECTED: * 'CASH OUT' (selected by default);
        EXPECTED: * 'OPEN BETS';
        EXPECTED: * 'SETTLED BETS';
        EXPECTED: ** Coral only
        EXPECTED: * 'SHOP BETS';
        """
        pass

    def test_003_tap_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'CASH OUT' tab
        EXPECTED: 'CASH OUT' tab is displayed
        EXPECTED: **Coral**
        EXPECTED: "Please log in to see your cash out bets." message is displayed
        EXPECTED: 'Log In' button is displayed under the message
        EXPECTED: **Ladbrokes** (not available after OX102)
        EXPECTED: "Your cash out bets will appear here, Please login to view." message is displayed
        """
        pass

    def test_004_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'OPEN BETS' tab
        EXPECTED: 'OPEN BETS' tab is displayed
        EXPECTED: **Coral**
        EXPECTED: "Please log in to see your open bets." message is displayed
        EXPECTED: 'Log In' button is displayed under the message
        EXPECTED: **Ladbrokes**
        EXPECTED: "Your open bets will appear here, Please login to view." message is displayed
        """
        pass

    def test_005_tap_setted_bets_tab(self):
        """
        DESCRIPTION: Tap 'SETTED BETS' tab
        EXPECTED: 'SETTLED BETS' tab is displayed
        EXPECTED: **Coral**
        EXPECTED: "Please log in to see your settled bets." message is displayed
        EXPECTED: 'Log In' button is displayed under the message
        EXPECTED: **Ladbrokes**
        EXPECTED: "Your settled bets will appear here, Please login to view." message is displayed
        """
        pass

    def test_006_click_up_facing_arrow(self):
        """
        DESCRIPTION: Click up facing arrow
        EXPECTED: **Before OX100**
        EXPECTED: 1. Bet Slip widget is collapsed (only section header is present)
        EXPECTED: 2. Up facing arrow changes to down facing one
        """
        pass

    def test_007_click_down_facing_arrow(self):
        """
        DESCRIPTION: Click down facing arrow
        EXPECTED: **Before OX100**
        EXPECTED: 1. Bet Slip widget is expanded and has the same content
        EXPECTED: 2. Down facing arrow changes to up facing one
        """
        pass
