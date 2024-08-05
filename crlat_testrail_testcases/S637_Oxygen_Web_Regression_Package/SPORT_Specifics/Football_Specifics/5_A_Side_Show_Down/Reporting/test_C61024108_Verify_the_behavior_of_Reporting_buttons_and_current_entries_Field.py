import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C61024108_Verify_the_behavior_of_Reporting_buttons_and_current_entries_Field(Common):
    """
    TR_ID: C61024108
    NAME: Verify the behavior of Reporting buttons and current entries Field
    DESCRIPTION: Verify the behavior of Reporting buttons
    PRECONDITIONS: 1. User should have admin access to CMS.
    PRECONDITIONS: NOTE: During the event, the CSV will update every 5 mins.Once the Event Settled flag is sent, the CSV does not have to update.
    """
    keep_browser_open = True

    def test_001_login_to_cms_with_admin_credentials_and_navigate_to_5_a_side_leaderboard_section_and_create_one_active_contest_for_5_a_side_event(self):
        """
        DESCRIPTION: Login to CMS with admin credentials and Navigate to 5-A-Side leaderboard section and create one active contest for 5-A-side event.
        EXPECTED: User can successfully logged in and contest created successfully.
        """
        pass

    def test_002_verify_current_entries_field_underneath_team_sizeindexphpattachmentsget156157917(self):
        """
        DESCRIPTION: verify current entries field underneath team size.
        DESCRIPTION: ![](index.php?/attachments/get/156157917)
        EXPECTED: Current entries field should be shown with default value zero.
        """
        pass

    def test_003_go_to_the_contest_and_place_5_a_side_bets_with_qualified_stake_to_enter_the_contest(self):
        """
        DESCRIPTION: Go to the contest and place 5-a-side bets with qualified stake to enter the contest.
        EXPECTED: Bets should enter contest successfully.
        """
        pass

    def test_004_verify_current_entries_in_cms(self):
        """
        DESCRIPTION: verify current entries in CMS
        EXPECTED: we get current entries count in pre state and get updates as and when scheduler runs in the background. count will update on refresh only.
        """
        pass

    def test_005_verify_download_contest_info_csv_and_download_prize_report_csv_buttons_underneath_paytable(self):
        """
        DESCRIPTION: Verify Download contest info CSV and Download prize report csv buttons underneath paytable.
        EXPECTED: These two buttons will available when we receive is report generated as true.
        EXPECTED: ![](index.php?/attachments/get/156157918)
        """
        pass

    def test_006_click_on_download_contest_information_csv(self):
        """
        DESCRIPTION: Click on Download contest information csv
        EXPECTED: Contest information csv should be downloaded with following data.
        EXPECTED: Contest Information:
        EXPECTED: Contest Name
        EXPECTED: Contest ID
        EXPECTED: Contest Date
        EXPECTED: Event
        EXPECTED: Entry Stake
        EXPECTED: Total Entries (this is the total number of teams entered at the time)
        EXPECTED: Leaderboard:
        EXPECTED: Position
        EXPECTED: Username
        EXPECTED: Bet ID
        EXPECTED: Progress%
        EXPECTED: Odds
        EXPECTED: Prize Type
        EXPECTED: Prize Amount
        """
        pass

    def test_007_click_on_download_prize_report_csv(self):
        """
        DESCRIPTION: Click on Download prize report CSV
        EXPECTED: Prize report csv should be downloaded with following data.
        EXPECTED: Column 1: Username
        EXPECTED: Column 2: Prize Type (Cash=Cash, Ticket or Free Bet = Free Bet)
        EXPECTED: Column 3: Prize Amount
        EXPECTED: Note: Do not include Vouchers in this report
        """
        pass
