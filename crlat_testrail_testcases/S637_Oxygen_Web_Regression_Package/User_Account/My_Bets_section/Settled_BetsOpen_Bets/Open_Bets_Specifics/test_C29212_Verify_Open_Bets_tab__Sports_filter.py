import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29212_Verify_Open_Bets_tab__Sports_filter(Common):
    """
    TR_ID: C29212
    NAME: Verify 'Open Bets' tab - 'Sports' filter
    DESCRIPTION: This test case verifies 'Open Bets' tab when user Logged In for 'Regular' bets
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-5275 Add Each Way to bet receipt
    DESCRIPTION: *   BMA-7644 As a Customer, I want to navigate from my open bet leg straight to the event, So that it's easier to find the event details
    DESCRIPTION: *   BMA-9189 Bet History - Desktop, Tablet and Mobile
    DESCRIPTION: *   [BMA-12164 Bet History/My Bets - Display Unit Stake][1]
    DESCRIPTION: *   BMA-22657 #YourCall - My Bets - Open bets layout
    DESCRIPTION: * [BMA-24438 Open Bets: Redesign main areas] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-12164
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-24438
    DESCRIPTION: AUTOTEST [C1501571]
    DESCRIPTION: AUTOTEST [C9698293]
    DESCRIPTION: AUTOTEST [C527795]
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have open bets
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: *   'My Bets' page / 'Bet Slip' widget is opened
        EXPECTED: *   'Open Bets' tab is shown next to 'Cash Out' tab
        """
        pass

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: *   'Sports' sort filter is selected by default
        """
        pass

    def test_004_verify_bet_overview(self):
        """
        DESCRIPTION: Verify Bet overview
        EXPECTED: *   All sections are displayed chronologically (**'settled=N'** attribute is set for all displayed bets (from response select 'Network' tab-> 'All' filter -> choose last request that appears after bet line expanding ->'Preview' tab))
        EXPECTED: *   If there are more than 20 sections, they are loaded after scrolling by portions (20 sections by portion)
        """
        pass

    def test_005_verify_multiples_bets(self):
        """
        DESCRIPTION: Verify Multiples bets
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * Bet details of all bets, which are included in a multiple, are shown one under another
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake and Estimated Returns are shown at the bottom of the section
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet details of all bets, which are included in a multiple, are shown one under another
        EXPECTED: * Stake and Estimated Returns are shown at the bottom of the section
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_006_trigger_the_situation_of_winning_a_bet_and_verify_if_bet_disappears_from_open_bets(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify if bet disappears from 'Open Bets'
        EXPECTED: **For** **98** **Release**:
        EXPECTED: Bet with status 'Won' is not displayed in 'Open Bets' tab
        EXPECTED: **For** **99** **Release**:
        EXPECTED: Bet with 'green tick' icon is not displayed in 'Open Bets' tab
        """
        pass

    def test_007_trigger_the_situation_of_losing_a_bet_and_verify_if_betdisappears_from_open_bets(self):
        """
        DESCRIPTION: Trigger the situation of Losing a bet and verify if bet disappears from 'Open Bets'
        EXPECTED: **For** **98** **Release**:
        EXPECTED: Bet with status 'Lost' is not displayed in 'Open Bets' tab
        EXPECTED: **For** **99** **Release**:
        EXPECTED: Bet with 'red cross' icon is not displayed in 'Open Bets' tab
        """
        pass

    def test_008_trigger_the_situation_of_cancelling_a_bet_and_verify_if_bet_disappears_fromopen_bets(self):
        """
        DESCRIPTION: Trigger the situation of Cancelling a bet and verify if bet disappears from 'Open Bets'
        EXPECTED: **For** **98** **Release**:
        EXPECTED: Bet with status 'Void' is not displayed in 'Open Bets' tab
        EXPECTED: **For** **99** **Release**:
        EXPECTED: Bet with status 'Void' is not displayed in 'Open Bets' tab
        """
        pass
