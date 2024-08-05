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
class Test_C11257180_To_archive_Betslip_displaying_show_hide_balance_without_any_selections_in_betslip(Common):
    """
    TR_ID: C11257180
    NAME: [To archive] Betslip: displaying show/hide balance without any selections in betslip
    DESCRIPTION: After new Wallet implementation show/hide balance buttons are displayed in Betslip header in both cases - if selections are added to Betslip or no
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies that show/hide balance buttons are not available for the user until some selections are added to betslip
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have no selections in betslip
    PRECONDITIONS: - Betslip should be opened
    """
    keep_browser_open = True

    def test_001_verify_displaying_balance_at_the_top_right_corner_of_betslip_header(self):
        """
        DESCRIPTION: Verify displaying balance at the top right corner of betslip header
        EXPECTED: Balance is not displayed
        """
        pass
