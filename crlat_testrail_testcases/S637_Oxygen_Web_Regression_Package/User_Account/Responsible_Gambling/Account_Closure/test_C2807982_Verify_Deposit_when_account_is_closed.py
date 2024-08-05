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
class Test_C2807982_Verify_Deposit_when_account_is_closed(Common):
    """
    TR_ID: C2807982
    NAME: Verify Deposit when account is closed
    DESCRIPTION: This test case verifies deposit functionality when the user's account is closed
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C8146668](https://ladbrokescoral.testrail.com/index.php?/cases/view/8146668)
    DESCRIPTION: Desktop - [C8146669](https://ladbrokescoral.testrail.com/index.php?/cases/view/8146669)
    PRECONDITIONS: * Load app and log in with user that has closed his account already (tag **Account_Closed_By_Player=true** is present in 35548 response in WS)
    PRECONDITIONS: * Navigate to Right Menu -> Deposit page
    PRECONDITIONS: * To see response from OpenAPI open DevTools -> Network tab -> WS -> Frames -> select responce from OpenAPI
    """
    keep_browser_open = True

    def test_001_verify_deposit_page_my_payments_tab(self):
        """
        DESCRIPTION: Verify Deposit page, 'My Payments' tab
        EXPECTED: * 'Your account is Closed. You cannot place bets/play games/ deposit new funds. In order to reactivate your account "Click Here"' error message is displayed above page content
        EXPECTED: where "Click Here" part is the hyperlink
        EXPECTED: * No tabs are displayed to user (e.g. 'My Payments', 'Add PayPal' and so on)
        """
        pass

    def test_002_clicktap_click_here_hyperlink_on_error_message(self):
        """
        DESCRIPTION: Click/tap "Click Here" hyperlink on error message
        EXPECTED: 'Reactivation' page is opened
        """
        pass
