import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C41790462_Verify_quantity_of_the_bets_on_the_Cash_Out_Open_Bets_tabs(Common):
    """
    TR_ID: C41790462
    NAME: Verify quantity of the bets on the  Cash Out/Open Bets tabs
    DESCRIPTION: This test case verifies connection creation to Cash Out MS and accountHistory request removed.
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In the app
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: * https://cashout-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/bet-details?token={token} - beta
    PRECONDITIONS: where token - bpp token
    """
    keep_browser_open = True

    def test_001_log_in_with_the_user_without_any_placed_bet(self):
        """
        DESCRIPTION: Log in with the user without any placed bet.
        EXPECTED: 
        """
        pass

    def test_002_place_21_bets_with_available_cashout_and_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Place 21 bets with available cashout and navigate to **Open Bets** tab
        EXPECTED: * **Open Bets** tab is opened.
        """
        pass

    def test_003_verify_the_number_of_bets_on_the_open_bets_tab(self):
        """
        DESCRIPTION: Verify the number of bets on the **Open Bets** tab.
        EXPECTED: * All 21 bets are available on the Open Bets tab.
        EXPECTED: * lazy loading and pagination logic is removed from cash out/open bets tabs and no spinner is shown to the user at the bottom of the page (bet-details stream return all data in initial request)
        """
        pass

    def test_004_place_40_more_bets_with_available_cashout_and_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Place 40 more bets with available cashout and navigate to **Open Bets** tab.
        EXPECTED: * All 61 bets are available on the **Open Bets** tab.
        EXPECTED: * lazy loading and pagination logic is removed from cash out/open bets tabs and no spinner is shown to the user at the bottom of the page (bet-details stream returns all data in initial request)
        """
        pass

    def test_005_repeat_steps_2_3_for_cash_out_tab(self):
        """
        DESCRIPTION: Repeat steps 2-3 for **Cash Out** tab
        EXPECTED: 
        """
        pass
