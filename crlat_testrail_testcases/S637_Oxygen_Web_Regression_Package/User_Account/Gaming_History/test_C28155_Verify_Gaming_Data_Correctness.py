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
class Test_C28155_Verify_Gaming_Data_Correctness(Common):
    """
    TR_ID: C28155
    NAME: Verify Gaming Data Correctness
    DESCRIPTION: This test case verifies gaming data correctness
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *BMA-1753** [Compliance] As a user I wish to see my Gaming History.
    DESCRIPTION: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: * [BMA-23956 RTS: Account History > Gaming History] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-23956
    PRECONDITIONS: 1. User should be logged in to view their gaming history
    PRECONDITIONS: 2. Open console -> Network -> WS -> Frames -> chose 32012 request and 32013 response to check data correctness
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_game_icon_on_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Game' icon on Sports Menu Ribbon
        EXPECTED: Homepage of Gaming Lobby is opened
        """
        pass

    def test_003_find_a_game_with_clienttypecasinoand_play_it(self):
        """
        DESCRIPTION: Find a game with **clientType=Casino **and play it
        EXPECTED: 
        """
        pass

    def test_004_go_back_to_invictus_application(self):
        """
        DESCRIPTION: Go back to Invictus application
        EXPECTED: 
        """
        pass

    def test_005_tap_on_right_menu_icon(self):
        """
        DESCRIPTION: Tap on Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_006_tap_on_my_account_menu_item(self):
        """
        DESCRIPTION: Tap on 'My Account' menu item
        EXPECTED: 'My Account' page is opened
        """
        pass

    def test_007_select_gaming_history_frommy_account_sub_menu(self):
        """
        DESCRIPTION: Select 'Gaming History' from 'My Account' sub menu
        EXPECTED: 'Gaming History' tab on 'Account History' page
        """
        pass

    def test_008_verify_configuration_of_32012_request(self):
        """
        DESCRIPTION: Verify configuration of 32012 request
        EXPECTED: Next data should be present in 32012 request:
        EXPECTED: **ignorePlayerViewConf=false**
        """
        pass

    def test_009_verify_data_displayed_in_datetime_column(self):
        """
        DESCRIPTION: Verify data displayed in **'Date/Time'** column
        EXPECTED: Date corresponds to   **'walletTransactions.transactionDateInUms'** attribute from 32013 response
        """
        pass

    def test_010_verify_data_displayed_in_gamecolumn(self):
        """
        DESCRIPTION: Verify data displayed in  **'Game'** column
        EXPECTED: *   Name of game corresponds to  **'walletTransactions.templateTags.game_name'** attribute
        EXPECTED: *   Game category corresponds to  **'walletTransactions.templateTags.game_category'** attribute
        EXPECTED: OR
        EXPECTED: * Game name and category correspond to  **'walletTransactions.templateTags.description'** attribute
        """
        pass

    def test_011_verify_data_displayed_in_amount_column(self):
        """
        DESCRIPTION: Verify data displayed in **'Amount'** column
        EXPECTED: -  Currency corresponds to  **'walletTransactions.amount.currencyCode'** attribute from responce
        EXPECTED: -  Amount corresponds to  **'walletTransactions.amount.amount'** attribute from responce
        """
        pass

    def test_012_verify_sign_displayed_in_amount_column(self):
        """
        DESCRIPTION: Verify sign displayed in **'Amount'** column
        EXPECTED: - Sing is '-' when **'walletTransactions.direction=Debit'**
        EXPECTED: - Sing is '+' when **'walletTransactions.direction=Credit'**
        """
        pass

    def test_013_repeat_steps_2_12_for_clienttypegames(self):
        """
        DESCRIPTION: Repeat steps 2-12 for **clientType=Games**
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_2_12_for_clienttypebingo(self):
        """
        DESCRIPTION: Repeat steps 2-12 for **clientType=Bingo**
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_2_12_for_clienttypepoker(self):
        """
        DESCRIPTION: Repeat steps 2-12 for **clientType=Poker**
        EXPECTED: 
        """
        pass

    def test_016_repeat_steps_2_12_for_clienttypelive(self):
        """
        DESCRIPTION: Repeat steps 2-12 for **clientType=Live**
        EXPECTED: 
        """
        pass
