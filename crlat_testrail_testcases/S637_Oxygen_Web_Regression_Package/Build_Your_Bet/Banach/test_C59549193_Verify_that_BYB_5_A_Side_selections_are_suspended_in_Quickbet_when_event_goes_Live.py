import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C59549193_Verify_that_BYB_5_A_Side_selections_are_suspended_in_Quickbet_when_event_goes_Live(Common):
    """
    TR_ID: C59549193
    NAME: Verify that BYB/5-A-Side selections are suspended in Quickbet when event goes Live
    DESCRIPTION: This TC verifies that:
    DESCRIPTION: - BYB/5-A-Side selections in Quickbet become suspended when event goes live
    DESCRIPTION: - User is redirected to All markets tab when they close Quickbet
    DESCRIPTION: - 5-A-Side/BYB tabs are not shown
    PRECONDITIONS: User is on EDP page, 5-A-Side/BYB tab
    """
    keep_browser_open = True

    def test_001_add_some_selections_and_click_place_bet(self):
        """
        DESCRIPTION: Add some selections and click Place Bet
        EXPECTED: Quickbet is shown with the selections
        """
        pass

    def test_002_trigger_push_update_from_ti_event_should_become_live___set_event_start_time__current_time_and_flag_is_off__yes(self):
        """
        DESCRIPTION: Trigger push update from TI (event should become Live - set event start time = current time and flag is off = yes)
        EXPECTED: - started: "Y" is received in push update
        EXPECTED: - Selections in quickbet are suspended
        EXPECTED: - Relevant message is displayed
        EXPECTED: - User cannot place bet
        EXPECTED: ![](index.php?/attachments/get/118215617)
        """
        pass

    def test_003_close_quickbet(self):
        """
        DESCRIPTION: Close Quickbet
        EXPECTED: - User is redirected to All markets tab
        EXPECTED: - 5-A-Side/BYB tabs are not shown
        """
        pass
