import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28156_Verify_Gaming_History_Page_When_There_is_no_Gaming_History(Common):
    """
    TR_ID: C28156
    NAME: Verify Gaming History Page When There is no Gaming History
    DESCRIPTION: This test case verifies Gaming History Page when there is no gaming history
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: * BMA-1753** [Compliance] As a user I wish to see my Gaming History.
    DESCRIPTION: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: * [BMA-23956 RTS: Account History > Gaming History] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-23956
    PRECONDITIONS: User should be logged in to view their Gaming history
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_right_menu_icon(self):
        """
        DESCRIPTION: Tap on Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_003_tap_on_my_account_menu_item(self):
        """
        DESCRIPTION: Tap on 'My Account' menu item
        EXPECTED: 'My Account' page is opened
        """
        pass

    def test_004_select_gaming_history_frommy_account_sub_menu(self):
        """
        DESCRIPTION: Select 'Gaming History' from 'My Account' sub menu
        EXPECTED: 'Gaming History' tab on 'Account History' page is opened
        """
        pass

    def test_005_verify_gaming_history_tab(self):
        """
        DESCRIPTION: Verify 'Gaming History' tab
        EXPECTED: *   'Gaming History' tab is empty when there is no available data in **'walletTransactions' **attribute for each **clientType ** (from response select 'Network' tab-> 'WS' filter -> choose last request ->'Frames' tab)
        EXPECTED: *   The 'You have no gaming history' message is shown
        """
        pass
