import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2161873_Verify_Cash_Out_button_when_all_bets_events_are_not_started(Common):
    """
    TR_ID: C2161873
    NAME: Verify Cash Out button when all bet's events are not started
    DESCRIPTION: This test case verify that Cash Out is unavailable when all bet's events are pre-play
    PRECONDITIONS: 1. Load Sportbook App
    PRECONDITIONS: 2. Log in
    PRECONDITIONS: 3. Chose 'Connect' from header ribbon
    PRECONDITIONS: 4. Select 'Shop Bet Tracker'
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001_bet_tracker_page_is_opened(self):
        """
        DESCRIPTION: Bet Tracker page is opened
        EXPECTED: 
        """
        pass

    def test_002_submit_valid_cash_out_code_that_contains_only_pre_play_events(self):
        """
        DESCRIPTION: Submit valid Cash Out Code that contains only pre-play events
        EXPECTED: * Cash Out Code is submitted successfully
        """
        pass

    def test_003_verify_cash_out_section_of_added_coupon(self):
        """
        DESCRIPTION: Verify Cash Out section of added coupon
        EXPECTED: Button is disabled and says 'Event not started'
        """
        pass

    def test_004_go_to_my_bets__in_shop_bets__sub_tub__repeat_step_3(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets'  sub-tub ->
        DESCRIPTION: repeat step #3
        EXPECTED: 
        """
        pass
