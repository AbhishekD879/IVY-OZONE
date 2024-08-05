import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C16268965_Vanilla_Successful_Log_Out(Common):
    """
    TR_ID: C16268965
    NAME: [Vanilla] Successful Log Out
    DESCRIPTION: This test case verifies user logging out
    DESCRIPTION: Autotest: [C58618735]
    PRECONDITIONS: User is logged In
    """
    keep_browser_open = True

    def test_001_click_on_my_account_button____log_out_buttonindexphpattachmentsget34287_____indexphpattachmentsget34288(self):
        """
        DESCRIPTION: Click on 'My Account' button --> 'Log Out' button
        DESCRIPTION: ![](index.php?/attachments/get/34287) -->  ![](index.php?/attachments/get/34288)
        EXPECTED: * User is logged out
        EXPECTED: * 'JOIN' and 'LOG IN' buttons are displayed in the header
        EXPECTED: * User Balance is not shown any more
        EXPECTED: ![](index.php?/attachments/get/34256)
        EXPECTED: * User is not able to access Right Menu, User Account menu, Deposit, Withdrawal pages
        EXPECTED: * **FOR Desktop**'Log In' button is displayed on Cash Out, Open Bets, Bet History, Favourites page/widget
        """
        pass
