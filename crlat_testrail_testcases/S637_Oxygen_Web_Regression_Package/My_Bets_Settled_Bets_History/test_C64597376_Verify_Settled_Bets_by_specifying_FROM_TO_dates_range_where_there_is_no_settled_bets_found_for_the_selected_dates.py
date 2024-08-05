import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64597376_Verify_Settled_Bets_by_specifying_FROM_TO_dates_range_where_there_is_no_settled_bets_found_for_the_selected_dates(Common):
    """
    TR_ID: C64597376
    NAME: Verify Settled Bets by specifying FROM & TO dates range where there is no settled bets found for the selected dates
    DESCRIPTION: Verify Settled Bets by specifying FROM & TO dates range where there is no settled bets found for the selected dates
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should have settled bets in account
    """
    keep_browser_open = True

    def test_001_open_settled_bets_tabmobile_my_bets_page__gt_settled_betstabletdesktop_bet_slip_widget__gt_settled_bets(self):
        """
        DESCRIPTION: Open 'Settled Bets' tab
        DESCRIPTION: Mobile: 'My Bets' page -&gt; 'Settled Bets'
        DESCRIPTION: Tablet/Desktop: 'Bet Slip' widget -&gt; 'Settled Bets'
        EXPECTED: * User is logged in
        EXPECTED: * Content of settled bets page is loaded
        """
        pass

    def test_002_select_the_date_range_in_which_user_doesnt_have_settled_bets(self):
        """
        DESCRIPTION: Select the date range in which user doesn't have settled bets
        EXPECTED: * Settled Bets were not founded for the selected dates
        EXPECTED: * "You have no Settled Bets" message is displayed
        """
        pass
