import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2064598_Verify_SSBT_coupons_for_Racing(Common):
    """
    TR_ID: C2064598
    NAME: Verify SSBT coupons for Racing
    DESCRIPTION: 
    PRECONDITIONS: Request creating of SSBT Horse Racing and Greyhound Racing barcodes
    PRECONDITIONS: with pre-play events
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_submit_ssbt_horse_racing_barcodes_that_contain_pre_play_and_finished_events(self):
        """
        DESCRIPTION: Submit SSBT horse racing barcodes that contain pre-play and finished events
        EXPECTED: Barcodes are submitted successfully
        """
        pass

    def test_003_verify_barcode_view(self):
        """
        DESCRIPTION: Verify barcode view
        EXPECTED: * barcode number and bet creation date/time at the top:
        EXPECTED: * XXXXXXXXXXXXX - XX/XX/XXXX XX:XX
        EXPECTED: * Delete button at the top right corner
        EXPECTED: * 'Betstation bet' title
        EXPECTED: * Stake and bet type:
        EXPECTED: £X.XX BetType
        EXPECTED: * List of events is displayed is following way:
        EXPECTED: * 'Sport' icon
        EXPECTED: * Selection name
        EXPECTED: * Market name
        EXPECTED: * Event name
        EXPECTED: * Event start date/time under sport icon (only fro pre-play event)
        EXPECTED: * Once event goes in-play nothing is shown under Sport icon
        EXPECTED: * Stake
        EXPECTED: * Returns (if bet is settled) or Potential Returns (if bet is not settled)
        EXPECTED: * Border button that says 'Bet settled' (when bet is settled) or shows Cash Out value and allows to cash out bet (when at least one event is started and bet is not settled yet)
        """
        pass

    def test_004__submit_ssbt_greyhound_barcodes_that_contain_pre_play_and_finished_events_repeat_step_3(self):
        """
        DESCRIPTION: * Submit SSBT greyhound barcodes that contain pre-play and finished events
        DESCRIPTION: * Repeat step #3
        EXPECTED: 
        """
        pass

    def test_005_go_to_my_bets__in_shop_bets_sub_tub__repeat_steps_3_4(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat steps #3-4
        EXPECTED: 
        """
        pass
