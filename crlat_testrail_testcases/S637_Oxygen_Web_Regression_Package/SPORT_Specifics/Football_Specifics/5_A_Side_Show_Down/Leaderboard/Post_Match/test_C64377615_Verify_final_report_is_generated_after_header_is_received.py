import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64377615_Verify_final_report_is_generated_after_header_is_received(Common):
    """
    TR_ID: C64377615
    NAME: Verify final report is generated after header is received
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: Create multiple contests for different events
    PRECONDITIONS: Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: 5) Wait for Event to start
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_navigate_to_any_llb(self):
        """
        DESCRIPTION: Navigate to any LLB
        EXPECTED: User should be navigated to LLB
        """
        pass

    def test_002_send_ertwhich_is_replay_incident___replay_stat_in_tst0_wait_until_event_is_finishedhlv0(self):
        """
        DESCRIPTION: Send ERT(which is replay incident _ replay stat in tst0)/ wait until event is finished(hlv0)
        EXPECTED: ERT should be received and stat should be updated
        """
        pass

    def test_003_wait_for_10m_and_send_1_more_stat(self):
        """
        DESCRIPTION: Wait for 10m and send 1 more stat
        EXPECTED: Stat should be sent at 10th min and updated in FE
        """
        pass

    def test_004_observe_header_is_received(self):
        """
        DESCRIPTION: Observe header is received
        EXPECTED: Header should be received
        """
        pass

    def test_005_verify_csv_file_from_cms_and_observe_final_report_is_generated_after_header_is_received(self):
        """
        DESCRIPTION: Verify CSV file from CMS and observe final report is generated after header is received
        EXPECTED: Final CSV should be generated after header is received and should match with LLB data including grace period stat updates
        """
        pass
