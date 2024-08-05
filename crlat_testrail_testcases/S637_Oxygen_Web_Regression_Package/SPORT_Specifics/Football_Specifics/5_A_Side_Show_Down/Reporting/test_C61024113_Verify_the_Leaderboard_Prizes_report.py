import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C61024113_Verify_the_Leaderboard_Prizes_report(Common):
    """
    TR_ID: C61024113
    NAME: Verify the Leaderboard Prizes report
    DESCRIPTION: This test case validates the data in Leaderboard information report.
    PRECONDITIONS: 1. User should have admin access to CMS.
    PRECONDITIONS: 2. Navigate to CMS->5-A-Side Showdown--> Completed Contest. Click the button "Download prize report csv" underneath the pay table.
    PRECONDITIONS: Note: Download contest information csv and Download prize report csv buttons are available once is report generated = true
    PRECONDITIONS: ![](index.php?/attachments/get/151940538)
    PRECONDITIONS: NOTE: During the event, the CSV will update every 5 mins. Before the event, this time can be extended to every 30 mins. Once the Event Settled flag is sent, the CSV does not have to update. **
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_5_a_side_leaderboard___completed_contest_click_the_button_download_prize_report_csv_underneath_the_pay_table(self):
        """
        DESCRIPTION: Navigate to CMS->5-A-Side Leaderboard--> Completed Contest. Click the button "Download prize report csv" underneath the pay table.
        EXPECTED: User should be able to download a csv file with the leaderboard prizes information if is report generated= true
        """
        pass

    def test_002_validate_the_data_in_the_downloaded_report(self):
        """
        DESCRIPTION: Validate the data in the downloaded report
        EXPECTED: 1.Contests included in the report should be in completed state.
        EXPECTED: 2.Leaderboard prizes report should have the following fields in the report
        EXPECTED: Username
        EXPECTED: Prize Type (Cash=Cash, Ticket or Free Bet = Free Bet)
        EXPECTED: Prize Amount
        """
        pass
