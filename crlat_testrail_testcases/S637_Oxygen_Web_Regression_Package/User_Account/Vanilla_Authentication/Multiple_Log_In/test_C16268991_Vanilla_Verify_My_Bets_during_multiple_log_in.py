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
class Test_C16268991_Vanilla_Verify_My_Bets_during_multiple_log_in(Common):
    """
    TR_ID: C16268991
    NAME: [Vanilla] Verify My Bets during multiple log in
    DESCRIPTION: This test case verifies Bet History/My Bets during multiple log in
    PRECONDITIONS: User should be logged in the same account from multiple devices
    """
    keep_browser_open = True

    def test_001_make_multiple_login_the_same_account(self):
        """
        DESCRIPTION: Make multiple login the same account
        EXPECTED: 
        """
        pass

    def test_002_place_a_bet_on_device_1(self):
        """
        DESCRIPTION: Place a bet on Device 1
        EXPECTED: Bet placement is successful on Device 1
        """
        pass

    def test_003_navigate_to_my_bets__open_bets_on_device_2_and_check_bet(self):
        """
        DESCRIPTION: Navigate to 'My Bets'-> 'Open Bets' on Device 2 and check bet
        EXPECTED: Bet is present on 'Open Bets' page on Device 2
        """
        pass

    def test_004_place_a_bet_from_device_1_while_staying_on__my_bets_from_event_detail_page_on_device_2(self):
        """
        DESCRIPTION: Place a bet from Device 1 while staying on  'My Bets' from event detail page on Device 2
        EXPECTED: - Bet placement is successful on Device 1
        EXPECTED: - 'My Bets' page is not updated in real time on Device 2
        """
        pass

    def test_005_refresh_my_bets_on_device_2_within_browser_refresh_button(self):
        """
        DESCRIPTION: Refresh 'My Bets' on Device 2 within browser refresh button
        EXPECTED: Bet is present on 'My Bets' on Device 2 after page refreshing
        """
        pass

    def test_006_make_multiple_login_old_account(self):
        """
        DESCRIPTION: Make multiple login old account
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_bet_history_page_from_both_devices(self):
        """
        DESCRIPTION: Navigate to 'Bet History' page from both devices
        EXPECTED: The same bet history is displayed on both devices
        """
        pass
