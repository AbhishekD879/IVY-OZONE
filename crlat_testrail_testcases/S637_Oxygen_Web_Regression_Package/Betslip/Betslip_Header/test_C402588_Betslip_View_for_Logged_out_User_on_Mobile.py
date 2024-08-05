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
class Test_C402588_Betslip_View_for_Logged_out_User_on_Mobile(Common):
    """
    TR_ID: C402588
    NAME: Betslip View for Logged out User on Mobile
    DESCRIPTION: This test case verifies Betslip header if user is logged out
    DESCRIPTION: AUTOTEST: [C2604424]
    PRECONDITIONS: Applies for Mobile only
    """
    keep_browser_open = True

    def test_001_load_oxygen_on_mobile(self):
        """
        DESCRIPTION: Load Oxygen on mobile
        EXPECTED: 
        """
        pass

    def test_002_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: **Before OX99**
        EXPECTED: - Betslip is opened
        EXPECTED: - No 'Quick Deposit' link is displayed in Betslip header
        EXPECTED: - "Please log in to see your balance" message is shown in the Betslip header
        EXPECTED: - "You have no selections in the slip." message is shown in the Betslip content area
        EXPECTED: **After OX99**
        EXPECTED: - Betslip is opened
        EXPECTED: - No 'Quick Deposit' link is displayed in Betslip header
        EXPECTED: - 'Your Betslip is empty' text is shown
        EXPECTED: - 'Please add one or more selections to place a bet' text is shown
        EXPECTED: - 'GO BETTING' button is shown
        EXPECTED: ![](index.php?/attachments/get/31448)
        EXPECTED: ![](index.php?/attachments/get/31449)
        """
        pass

    def test_003_close_betslip(self):
        """
        DESCRIPTION: Close Betslip
        EXPECTED: 
        """
        pass

    def test_004_add_a_1_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add a 1 selection to the Betslip
        EXPECTED: **Before OX99**
        EXPECTED: Yellow Circle is displayed on 'Betslip' icon in the top right corner displaying '1' as a number of added selections
        EXPECTED: **After OX99**
        EXPECTED: Coral: Yellow square is displayed on 'Betslip' icon in the top right corner displaying '1' as a number of added selections
        EXPECTED: ![](index.php?/attachments/get/31446)
        EXPECTED: Ladbrokes: White circle is displayed on 'Betslip' icon in the top right corner displaying '1' as a number of added selections
        EXPECTED: ![](index.php?/attachments/get/31447)
        """
        pass

    def test_005_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: **Before OX99**
        EXPECTED: - Betslip is opened
        EXPECTED: - No 'Quick Deposit' link is displayed in Betslip header
        EXPECTED: - "Please log in to see your balance" message is shown in the Betslip header
        EXPECTED: - Added selection is displayed in the Betslip content area
        EXPECTED: **After OX99**
        EXPECTED: - Betslip is opened
        EXPECTED: - No 'Quick Deposit' link is displayed in Betslip header
        EXPECTED: - Your Selections: N (where N - number of selections) and 'REMOVE ALL' button is shown in the header
        EXPECTED: - Added selection is displayed in the Betslip content area
        """
        pass
