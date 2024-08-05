import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C402589_Betslip_View_For_User_with_FreeBets_on_Mobile(Common):
    """
    TR_ID: C402589
    NAME: Betslip View For User with FreeBets on Mobile
    DESCRIPTION: This test case verifies whether freebet icon is displayed in the right side of the balance bar of the Betslip header if user has free bets
    DESCRIPTION: ** JIRA tickets:**
    DESCRIPTION: BMA-20361 New betslip design - header (mobile only)
    PRECONDITIONS: User account with positive balance and with free bets available
    PRECONDITIONS: Applies for Mobile
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: - Homepage is opened
        """
        pass

    def test_002_log_in_user_account__from_preconditions(self):
        """
        DESCRIPTION: Log in User account ( from Preconditions)
        EXPECTED: - User is logged in
        """
        pass

    def test_003_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: **VALID UP TO OX98**
        EXPECTED: - Betslip is opened
        EXPECTED: - "You have no selections in the slip." message is shown at the top of Betslip content
        EXPECTED: - 'Quick Deposit' link is not available in the Betslip header
        EXPECTED: - "Your Balance is: <currency symbol>XX.XX" message is shown in the Betslip header
        EXPECTED: - 'FB' icon is displayed in the right corner of the balance bar in the 'Betslip' header
        EXPECTED: **VALID FROM OX99**
        EXPECTED: - Betslip is opened
        EXPECTED: - "Your betslip is empty" message in bold is shown at the top of Betslip content and "Please add one or more selections to place a bet" message is displayed below
        EXPECTED: - "GO BETTING" button is displayed
        EXPECTED: - User balance is displayed at the top right corner of the 'Betslip' header
        EXPECTED: - 'Quick Deposit' link is not available in the Betslip header, only when user taps the balance button drop down with  'Hide Balance' and 'Deposit' options appear
        EXPECTED: - 'FB' icon is NOT displayed in the right corner of the balance bar in the 'Betslip' header
        """
        pass

    def test_004_close_betslip_page__x_in_left_top_corner_of_betslip(self):
        """
        DESCRIPTION: Close Betslip page ( 'X' in left top corner of Betslip)
        EXPECTED: Betslip is closed
        """
        pass

    def test_005_add_a_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add a selection to the Betslip
        EXPECTED: -  Yellow Circle is displayed on 'Betslip' icon  in the top right corner with 'X' - number of added selections
        """
        pass

    def test_006_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: **VALID UP TO OX98**
        EXPECTED: - Betslip is opened
        EXPECTED: - Selection is displayed in Betslip content area
        EXPECTED: - 'Quick Deposit' link is available in the Betslip header
        EXPECTED: - "Your Balance is: <currency symbol>X.XX" message is shown in the Betslip header
        EXPECTED: - 'FB' icon is displayed in the right corner of the balance bar in the 'Betslip' header
        EXPECTED: **VALID FROM OX99**
        EXPECTED: - Betslip is opened
        EXPECTED: - User balance is displayed at the top right corner of the 'Betslip' header
        EXPECTED: - 'Quick Deposit' link is not available in the Betslip header, only when user taps the balance button drop down with  'Hide Balance' and 'Deposit' options appear
        EXPECTED: - 'FB' icon is NOT displayed in the right corner of the balance bar in the 'Betslip' header
        """
        pass
