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
class Test_C33112139_Vanilla_Deposit_link_in_the_Betslip_header(Common):
    """
    TR_ID: C33112139
    NAME: [Vanilla] Deposit link in the Betslip header
    DESCRIPTION: This test case verifies that Deposit page is opened through Deposit link in the Betslip header
    PRECONDITIONS: User account with added credit cards and positive balance
    PRECONDITIONS: Applies for Mobile
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_account__from_preconditions(self):
        """
        DESCRIPTION: Log in with User account ( from Preconditions)
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_a_selection_to_the_betslip___open_betslip_page(self):
        """
        DESCRIPTION: Add a selection to the Betslip -> Open Betslip page
        EXPECTED: Selection is displayed within Betslip content area
        EXPECTED: User balance is displayed in the header
        """
        pass

    def test_004_tap_on_user_balance_area_in_the_betslip_header__deposit_button(self):
        """
        DESCRIPTION: Tap on User Balance area in the Betslip header > Deposit button
        EXPECTED: Deposit page is opened
        """
        pass

    def test_005_close_the_deposit_page_x(self):
        """
        DESCRIPTION: Close the Deposit page ('X')
        EXPECTED: Deposit page is closed. Homepage is displayed
        """
        pass
