import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C28154_Verify_Gaming_History_Page(Common):
    """
    TR_ID: C28154
    NAME: Verify Gaming History Page
    DESCRIPTION: This test case verifies the 'Gaming History' page
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: * BMA-1753 [Compliance] As a user I wish to see my Gaming History
    DESCRIPTION: *  [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: * [BMA-23956 RTS: Account History > Gaming History] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-23956
    PRECONDITIONS: User should be logged in to view their Gaming history
    PRECONDITIONS: User should have Gaming History
    PRECONDITIONS: Note: The page has been further updated in BMA-23956 - RTS: Account History > Gaming History
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
        EXPECTED: * 'Gaming History' tab on 'Account History' page is opened
        EXPECTED: * "From" and "To" date pickers with user's current date selected by default in both of them
        EXPECTED: * (not yet implemented) 'gaming history' table is shown with data from today's date
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: *   User is directed to 'My Account' page after tapping Back button
        EXPECTED: *   User is directed to Homepage when she/he uses direct link
        """
        pass

    def test_006_verify_data_displaying(self):
        """
        DESCRIPTION: Verify data displaying
        EXPECTED: The data is organised and displayed in a table into following columns:
        EXPECTED: *   **'Date/Time'** column is shown in** DD-MM HH:MM AM/PM** format (e.g 04/05 06:45 AM)
        EXPECTED: *   **'Game'** column is shown in **\[client type] wager: [game\_name\] ([game\_category]) **format (e.g. Casino wager: Blackjack Multihand 5 (Cards))
        EXPECTED: *   **'Amount' **coulmn is shown in** **+-**\[currencyCode\]\[amount\] **format (e.g. £+10.00)
        """
        pass

    def test_007_verify_default_data(self):
        """
        DESCRIPTION: Verify default data
        EXPECTED: All data is shown chronologically, most recent first (see **'Data/Time' **column)
        """
        pass

    def test_008_verify_lazy_load(self):
        """
        DESCRIPTION: Verify lazy load
        EXPECTED: *   First 20 item are shown by default
        EXPECTED: *   Next 20 item will load when user scrolls down
        """
        pass
