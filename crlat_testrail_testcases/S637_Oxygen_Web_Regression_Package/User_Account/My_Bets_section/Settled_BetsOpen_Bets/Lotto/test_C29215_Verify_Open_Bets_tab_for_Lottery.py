import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29215_Verify_Open_Bets_tab_for_Lottery(Common):
    """
    TR_ID: C29215
    NAME: Verify 'Open Bets' tab for 'Lottery'
    DESCRIPTION: This Test Case verifies 'Lottery' tab when user Logged In
    DESCRIPTION: **JIRA Ticket :**
    DESCRIPTION: BMA-5879 'Lottery - View open lottery bets'
    DESCRIPTION: BMA-17176 Re-naming of Cash Out section, associated tabs and moving Bet History
    DESCRIPTION: BMA-17175 Moving and changing navigation logic of Cash Out section (tablet/desktop)
    DESCRIPTION: BMA-27822 Open Bets : Lotto Redesign
    DESCRIPTION: AUTOTEST [C2000011]
    DESCRIPTION: AUTOTEST [C2000009]
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have 'Pending' bets on Lottery
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Navigate to 'My Bets' item on Top Menu
        EXPECTED: *   'My Bets' page/'Bet Slip' widget is opened
        EXPECTED: *   'Open Bets' tab is shown next to 'Cash Out' tab
        """
        pass

    def test_002_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: *   'Regular', 'Player Bets', 'Lotto' and 'Pools' sort filters are shown
        EXPECTED: *   'Regular' sort filter is selected by default
        """
        pass

    def test_003_navigate_to_lotto_filter_and_check_content_within_it(self):
        """
        DESCRIPTION: Navigate to 'Lotto' filter and check content within it
        EXPECTED: 1.All '**Pending bets**' sections are displayed chronologically (**'settled=N'** attribute is set for all displayed bets (from response select 'Network' tab-> 'All' filter -> choose the last request that appears after bet line expanding ->'Preview' tab))
        EXPECTED: 2. All sections are expanded
        EXPECTED: 3. All sections are not collapsible
        EXPECTED: 3. If there are more than 20 events, they should be loaded after scrolling by portions (20 event by portion)
        """
        pass

    def test_004_verify_information_in_bet_section_header(self):
        """
        DESCRIPTION: Verify information in bet section header
        EXPECTED: Following information is displayed in bet section header:
        EXPECTED: *   Lottery name
        """
        pass

    def test_005_verify_bet_details_and_check_if_bet_details_are_same_as_in_openbetsystem(self):
        """
        DESCRIPTION: Verify bet details and check if bet details are same as in **OpenBet **system
        EXPECTED: Bet details are shown:
        EXPECTED: **User's pick**s : X, x, x, x, x
        EXPECTED: **Draw Type** : e.g. Monday Draw
        EXPECTED: **Draw Date** : date of draw
        EXPECTED: **Stake**: stake value
        EXPECTED: **Bet Receipt #**
        EXPECTED: **Bet placed at** : date of lotto bet placement
        EXPECTED: **Returns Details** : returns value* (available only for settled bets)
        """
        pass
