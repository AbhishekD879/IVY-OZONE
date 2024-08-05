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
class Test_C64597375_Verify_mybets_history_in_the_Settled_Bets_by_specifying_FROM_TO_dates_range_more_than_1_year(Common):
    """
    TR_ID: C64597375
    NAME: Verify mybets history in the Settled Bets by specifying FROM & TO dates range more than 1 year
    DESCRIPTION: Verify My bets history in the Settled Bets by specifying FROM & TO dates range more than 1 year
    PRECONDITIONS: User should have settled bets in their account in past one year
    """
    keep_browser_open = True

    def test_001_open_settled_bets_tabmobile_my_bets_page__gt_settled_betstabletdesktop_bet_slip_widget__gt_settled_bets(self):
        """
        DESCRIPTION: Open 'Settled Bets' tab
        DESCRIPTION: Mobile: 'My Bets' page -&gt; 'Settled Bets'
        DESCRIPTION: Tablet/Desktop: 'Bet Slip' widget -&gt; 'Settled Bets'
        EXPECTED: 1. 'Settled Bets' tab is opened
        EXPECTED: 2. "Your settled bets will appear here,
        EXPECTED: 3. Please login to view." message is displayed
        """
        pass

    def test_002_2_log_into_the_application(self):
        """
        DESCRIPTION: 2. Log into the application
        EXPECTED: * User is logged in
        EXPECTED: * Content of settled bets page is loaded
        """
        pass

    def test_003_3_observe_the_from__to_dates(self):
        """
        DESCRIPTION: 3. Observe the FROM & TO dates
        EXPECTED: Default Calendar shows 7 days of data
        EXPECTED: 20 bets per page is loaded if beyond then 20 add pagination i.e., Once the user views the first set of 20 records, on page scroll the next set of 20 records, shall not be appended sequentially below the first 20, rather the entire set 40 (20+20) records get sorted again.
        """
        pass

    def test_004_set_calendar_date_range_up_to_one_year_from_todays_date_to_past_one_yearex_from_01012021_to_31122021_consider_as_today_date(self):
        """
        DESCRIPTION: Set calendar date range up to one year from today's date to past one year
        DESCRIPTION: ex: FROM: 01/01/2021 TO: 31/12/2021( consider as today date)
        EXPECTED: Settled Bets content is loaded with past one year records
        """
        pass

    def test_005_set_calendar_date_range_more_than_one_year_from_todays_dateex_from_01122020_to_31122021_consider_as_today_date(self):
        """
        DESCRIPTION: Set calendar date range more than one year from today's date
        DESCRIPTION: ex: FROM: 01/12/2020 TO: 31/12/2021( consider as today date)
        EXPECTED: "If you require account or gambling history over longer periods please
        EXPECTED: contact us" message is displayed
        """
        pass

    def test_006_set_calendar_date_range_more_than_one_yearex_from_01012021_to_31012022_consider_as_one_month_forward_from_todays_date(self):
        """
        DESCRIPTION: Set calendar date range more than one year
        DESCRIPTION: ex: FROM: 01/01/2021 TO: 31/01/2022( consider as one month forward from today's date)
        EXPECTED: "If you require account or gambling history over longer periods please
        EXPECTED: contact us" message is displayed
        """
        pass

    def test_007_set_calendar_date_range_more_than_one_yearex_from_01112020_to_31112021consider_as_one_month_back_from_todays_date(self):
        """
        DESCRIPTION: Set calendar date range more than one year
        DESCRIPTION: ex: FROM: 01/11/2020 TO: 31/11/2021(consider as one month back from today's date)
        EXPECTED: "If you require account or gambling history over longer periods please
        EXPECTED: contact us" message is displayed
        """
        pass
