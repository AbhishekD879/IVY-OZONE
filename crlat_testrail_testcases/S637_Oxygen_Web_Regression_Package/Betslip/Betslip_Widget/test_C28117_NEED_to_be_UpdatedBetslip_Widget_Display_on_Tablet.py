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
class Test_C28117_NEED_to_be_UpdatedBetslip_Widget_Display_on_Tablet(Common):
    """
    TR_ID: C28117
    NAME: [NEED to be Updated]Betslip Widget Display on Tablet
    DESCRIPTION: This test case verifies view of BetSlip widget displaying with no added selections on Tablet
    PRECONDITIONS: Tablet device
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_tablet_device(self):
        """
        DESCRIPTION: Load Oxygen app on tablet device
        EXPECTED: 1. Homepage is opened
        EXPECTED: 2. Bet Slip widget is located at the top of right column
        EXPECTED: 3. Bet Slip widget is expanded by default and contains:
        EXPECTED: * <collapse/expand> button ("-")
        EXPECTED: * 'BET SLIP' label
        EXPECTED: * Tabs: 'BET SLIP' (selected by default); 'CASH OUT'; 'OPEN BETS'; 'BET HISTORY';
        EXPECTED: * Message "You have no selections in the slip." displayed within Betslip content area
        EXPECTED: **FROM OX100**
        EXPECTED: 1. Homepage is opened
        EXPECTED: 2.  Bet Slip widget is located at the top of the last column
        EXPECTED: 3.  Bet Slip widget contains:
        EXPECTED: * 'BETSLIP' header
        EXPECTED: * Tabs: 'BETSLIP' (selected by default); 'MY BETS'
        EXPECTED: * Message "Your betslip is empty" at the top and for CORAL message below "Please add one or more selections to place a bet" displayed within Betslip content area
        EXPECTED: *Ladbrokes Only*
        EXPECTED: * Button with name "GO BETTING"
        """
        pass

    def test_002_tap_my_bets_tab(self):
        """
        DESCRIPTION: Tap 'MY BETS' tab
        EXPECTED: New tabs are visible:
        EXPECTED: * 'CASH OUT' (selected by default);
        EXPECTED: * 'OPEN BETS';
        EXPECTED: * 'SETTLED BETS';
        EXPECTED: * 'SHOP BETS';
        """
        pass

    def test_003_tap_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'CASH OUT' tab
        EXPECTED: 1. 'CASH OUT' tab is displayed
        EXPECTED: 2. "Please log in to see your Cash Out bets." message is displayed
        EXPECTED: 3. 'Log In' button is displayed under the message
        """
        pass

    def test_004_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'OPEN BETS' tab
        EXPECTED: 1. 'OPEN BETS' tab is displayed
        EXPECTED: 2."Please log in to see your Open Bets." message is displayed
        EXPECTED: 3. 'Log In' button is displayed under the message
        """
        pass

    def test_005_tap_settled_bets_tab(self):
        """
        DESCRIPTION: Tap 'SETTLED BETS' tab
        EXPECTED: 1. 'SETTLED BETS' tab is displayed
        EXPECTED: 2."Please log in to see your settled bets." message is displayed
        EXPECTED: 3. 'Log In' button is displayed under the message
        """
        pass

    def test_006_click_collapseexpand_button__(self):
        """
        DESCRIPTION: Click <collapse/expand> button ("-")
        EXPECTED: **Before OX100**
        EXPECTED: 1. Bet Slip widget is collapsed (only section header is present)
        EXPECTED: 2. <collapse/expand> button ("-") changed to "+"
        """
        pass

    def test_007_click_collapseexpand_button_plus(self):
        """
        DESCRIPTION: Click <collapse/expand> button ("+")
        EXPECTED: **Before OX100**
        EXPECTED: 1. Bet Slip widget is expanded and has the same content
        EXPECTED: 2. <collapse/expand> button ("+") changed to "-"
        """
        pass
