import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28581_Verify_Bet_Receipt_after_successful_bet_placement(Common):
    """
    TR_ID: C28581
    NAME: Verify Bet Receipt after successful bet placement
    DESCRIPTION: This test case verifies bet receipt that user see after successful bet placement on Football Jackpot
    DESCRIPTION: **Jira tickets: **BMA-2058
    DESCRIPTION: AUTOTEST [C9700979]
    PRECONDITIONS: *   Football Jackpot pool is available
    PRECONDITIONS: *   User is logged in with valid account with enough balance to place a bet on Football Jackpot pool
    PRECONDITIONS: Note:
    PRECONDITIONS: Line - 15 selections, 1 from each event
    PRECONDITIONS: Total Lines - number of selected combinations of 15 match results
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: *   Football Jackpot Page is opened with 15 events available
        EXPECTED: *   Each event has 3 buttons
        """
        pass

    def test_004_make_at_least_15_selection_at_least_1_from_each_event_using_lucky_dip_option_or_manually(self):
        """
        DESCRIPTION: Make at least 15 selection (at least 1 from each event) using 'Lucky Dip' option or manually
        EXPECTED: *   Selections that were made are highlighted
        EXPECTED: *   'Total Lines' field counter is increased by number of formed lines
        EXPECTED: *   'Bet Now' button is enabled
        """
        pass

    def test_005_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Bet is successfully placed
        EXPECTED: *   Football Jackpot bet is handled in page (i.e. wholly independently of bet slip)
        EXPECTED: *   User is redirected to Bet Receipt page
        """
        pass

    def test_006_verify_bet_receipt_page_header(self):
        """
        DESCRIPTION: Verify Bet Receipt page header
        EXPECTED: Page's name is 'Football Jackpot Bet Receipt'
        """
        pass

    def test_007_verify_lines_section(self):
        """
        DESCRIPTION: Verify 'Lines' section
        EXPECTED: *   Section name is 'Lines (<number of lines on which bet was placed>)'
        EXPECTED: *   Section is collapsible/expandable
        """
        pass

    def test_008_verify_section_sub_header(self):
        """
        DESCRIPTION: Verify section sub-header
        EXPECTED: *   **'Football Jackpot 15'** label is present
        EXPECTED: *   **'Bet Receipt No: P/XXX/XXX'** label with bet number is shown
        EXPECTED: *   **'Total Stake: £YY.YY'** field is present, where YY.YY - is stake amount placed on Football Jackpot lines
        EXPECTED: *   **'Number of Lines: N'** field is present, where N - number of lines user placed bet on
        """
        pass

    def test_009_verify_section_main_body(self):
        """
        DESCRIPTION: Verify section main body
        EXPECTED: *   Section's main body is divided into two columns
        EXPECTED: *   First column title is 'Game' and underneath it 15 match names that are available in Football Jackpot are displayed
        EXPECTED: *   Second column title is 'Selection' and underneath it selections made by user to place a bet are displayed ('H'/'D'/'A')
        EXPECTED: *   Events are ordered in the following way:
        EXPECTED: 1.  **startTime **- chronological order in the first instance
        EXPECTED: 2.  **Class displayOrder**
        EXPECTED: 3.  **Type displayOrder**
        EXPECTED: 4.  **Event displayOrder**
        EXPECTED: 5.  **Alphabetical order**
        """
        pass

    def test_010_verify_done_button(self):
        """
        DESCRIPTION: Verify 'Done' button
        EXPECTED: *   'Done' button redirects user back to the Football 'Jackpot' page
        EXPECTED: *   'Done' button redirects user to Football 'Matches' tab if Football Jackpot becomes unavailable
        """
        pass

    def test_011_verify_reflection_on_page_refresh_when_football_jackpot_receipt_page_is_opened(self):
        """
        DESCRIPTION: Verify reflection on page refresh when Football Jackpot Receipt page is opened
        EXPECTED: Page refresh is considered as 'Done' button clicking
        """
        pass
