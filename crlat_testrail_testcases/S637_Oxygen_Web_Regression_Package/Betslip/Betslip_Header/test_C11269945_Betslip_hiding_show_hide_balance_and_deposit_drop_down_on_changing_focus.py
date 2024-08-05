import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C11269945_Betslip_hiding_show_hide_balance_and_deposit_drop_down_on_changing_focus(Common):
    """
    TR_ID: C11269945
    NAME: Betslip: hiding show/hide balance and deposit drop down on changing focus
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies that show/hide balance and deposit drop down is hidden on changing focus
    PRECONDITIONS: - You should be logged on
    PRECONDITIONS: - You should have added selections to betslip
    PRECONDITIONS: - Betslip should be opened
    """
    keep_browser_open = True

    def test_001_tap_account_balance_area_and_verify_displaying_of_showhide_balance_and_deposit_drop_down(self):
        """
        DESCRIPTION: Tap 'Account Balance' area and verify displaying of show/hide balance and deposit drop down
        EXPECTED: Show/hide balance and deposit drop down is displayed
        """
        pass

    def test_002_tap_anywhere_outside_of_the_drop_down_and_verify_the_drop_down_displaying(self):
        """
        DESCRIPTION: Tap anywhere outside of the drop down and verify the drop down displaying
        EXPECTED: Show/hide balance and deposit drop down is undisplayed
        """
        pass
