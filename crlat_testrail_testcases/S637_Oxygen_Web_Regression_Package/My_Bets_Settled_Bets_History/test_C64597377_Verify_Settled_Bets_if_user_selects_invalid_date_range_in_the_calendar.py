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
class Test_C64597377_Verify_Settled_Bets_if_user_selects_invalid_date_range_in_the_calendar(Common):
    """
    TR_ID: C64597377
    NAME: Verify Settled Bets if user selects invalid date range in the calendar
    DESCRIPTION: Verify Settled Bets if user selects invalid date range in the calendar
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User should have settled bets in their account in past one year
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

    def test_002_set_from_date_beyond_the_todays_dateex_if_today_date_is_01012021_then_keep_from_date_as_02012021__to_date_as_03012021(self):
        """
        DESCRIPTION: Set FROM date beyond the today's date
        DESCRIPTION: ex: If today date is 01/01/2021 then keep FROM date as 02/01/2021 & TO date as 03/01/2021
        EXPECTED: * Settled Bets were not founded for the selected dates
        EXPECTED: * "Please select a valid time range" message is displayed
        """
        pass

    def test_003_set_from_date_greater_than_the_todays_dateex_if_today_date_is_01012021_then_keep_from_date_as_02012021__to_date_as_01012021(self):
        """
        DESCRIPTION: Set FROM date greater than the today's date
        DESCRIPTION: ex: If today date is 01/01/2021 then keep FROM date as 02/01/2021 & TO date as 01/01/2021
        EXPECTED: * Settled Bets were not founded for the selected dates
        EXPECTED: * "Please select a valid time range" message is displayed
        """
        pass

    def test_004_set_from_date_greater_than_the_todays_date_with_one_year_gapex_if_today_date_is_01012021_then_keep_from_date_as_02012021__to_date_as_01012022(self):
        """
        DESCRIPTION: Set FROM date greater than the today's date with one year gap
        DESCRIPTION: ex: If today date is 01/01/2021 then keep FROM date as 02/01/2021 & TO date as 01/01/2022
        EXPECTED: * Settled Bets were not founded for the selected dates
        EXPECTED: * "Please select a valid time range" message is displayed
        """
        pass
