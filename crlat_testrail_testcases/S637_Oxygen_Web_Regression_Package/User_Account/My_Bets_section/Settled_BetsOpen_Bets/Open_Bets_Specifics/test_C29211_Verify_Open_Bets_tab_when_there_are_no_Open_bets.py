import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29211_Verify_Open_Bets_tab_when_there_are_no_Open_bets(Common):
    """
    TR_ID: C29211
    NAME: Verify 'Open Bets' tab when there are no Open bets
    DESCRIPTION: This test case verifies 'Open Bets' tab when no open bets are present.
    DESCRIPTION: **Jira tickets:** BMA-3145, BMA-17176, BMA-17820, BMA-24438
    DESCRIPTION: AUTOTEST [C9697786]
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User shouldn't have open bets
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
        EXPECTED: *   'Regular' sort filter is selected by default
        """
        pass

    def test_004_verify_message_on_open_bets_tab___regular_sort_filter(self):
        """
        DESCRIPTION: Verify message on 'Open Bets' tab - 'Regular' sort filter
        EXPECTED: ** 'You currently have no open bets.**' message is displayed
        """
        pass

    def test_005_select_pools_sort_filter(self):
        """
        DESCRIPTION: Select 'Pools' sort filter
        EXPECTED: **'You currently have no open bets.'** message is displayed
        """
        pass
