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
class Test_C28158_Verify_Gaming_History_Page_for_Non_Logged_in_Customer(Common):
    """
    TR_ID: C28158
    NAME: Verify Gaming History Page for Non Logged in Customer
    DESCRIPTION: This test case verifies Gaming History Page for non logged in customer
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: * BMA-1753 [Compliance] As a user I wish to see my Gaming History
    DESCRIPTION: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: * [BMA-23956 RTS: Account History > Gaming History] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-23956
    PRECONDITIONS: User should be logged out
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_gaming_history_tab_on_account_history_page_by_using_the_next_direct_linkhttpsinvictuscoralcoukgaming_history(self):
        """
        DESCRIPTION: Go to the 'Gaming History' tab on 'Account History' page by using the next direct link:
        DESCRIPTION: https://invictus.coral.co.uk/#/gaming-history
        EXPECTED: *   User cannot access to the 'Gaming History' tab on 'Account History' page
        EXPECTED: *   Homepage is opened instead
        """
        pass
