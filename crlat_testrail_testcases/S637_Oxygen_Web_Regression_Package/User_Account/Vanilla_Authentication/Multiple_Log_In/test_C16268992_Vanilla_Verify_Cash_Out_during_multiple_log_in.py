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
class Test_C16268992_Vanilla_Verify_Cash_Out_during_multiple_log_in(Common):
    """
    TR_ID: C16268992
    NAME: [Vanilla] Verify Cash Out during multiple log in
    DESCRIPTION: This test case verifies Cash Out during multiple log in
    PRECONDITIONS: User should be logged in the same account from multiple devices
    """
    keep_browser_open = True

    def test_001_make_multiple_login_the_same_account(self):
        """
        DESCRIPTION: Make multiple login the same account
        EXPECTED: 
        """
        pass

    def test_002_place_a_bet_from_device_1(self):
        """
        DESCRIPTION: Place a bet from Device 1
        EXPECTED: Bet placement is successful on Device 1
        """
        pass

    def test_003_navigate_to_cash_out_pagewidget_on_device_2(self):
        """
        DESCRIPTION: Navigate to Cash out page/widget on Device 2
        EXPECTED: Bet is displayed on Cash out page/widget
        """
        pass

    def test_004_place_a_bet_from_device_1_while_staying_on_cash_out_pagewidget_on_device_2(self):
        """
        DESCRIPTION: Place a bet from Device 1 while staying on Cash Out page/widget on Device 2
        EXPECTED: - Bet placement is successful on Device 1
        EXPECTED: - 'Bet History' page is not updated in real time on Device 2
        """
        pass

    def test_005_refresh_cash_out_pagewidget_on_device_2_within_browser_refresh_button(self):
        """
        DESCRIPTION: Refresh Cash Out page/widget on Device 2 within browser refresh button
        EXPECTED: Bet is present on Cash Out page/widget  on Device 2 after page refreshing
        """
        pass

    def test_006_navigate_to_cash_out_pagewidget_from_both_devices(self):
        """
        DESCRIPTION: Navigate to Cash Out page/widget from both devices
        EXPECTED: The same bets are displayed on Cash Out page/widget for both devices
        """
        pass
