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
class Test_C64597387_Verify_that_the_maximum_date_range_for_the_Calendar_is_supported_for_the_period_of_four_years_based_on_the_dates_selected_in_the_From_and_To_Calendar_grids(Common):
    """
    TR_ID: C64597387
    NAME: Verify that the maximum date range for the Calendar is supported for the period of four years based on the dates selected in the From and To Calendar grids.
    DESCRIPTION: Verify that the maximum date range for the Calendar is supported for the period of four years based on the dates selected in the From and To Calendar grids.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Cashout tab.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_cashout_tabtabletdesktop_my_bets_section__gt_cashout_tab(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Cashout tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Cashout tab'
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the Cashout tab.
        """
        pass

    def test_002_select_the_date_range_of_4_years_span_in_the_from_and_to_calendar_grid_try_opting_for_4_years_date_range_which_covers_a_future_date_as_well(self):
        """
        DESCRIPTION: Select the date range of 4 years span in the From and To Calendar grid. Try opting for 4 years date range which covers a future date as well.
        EXPECTED: The user should be able to select the date range of 4 years in the Calendar grid in the Cashout tab.
        """
        pass

    def test_003_verify_the_details_of_all_the_bets_which_are_displayed_in_the_cashout_tab(self):
        """
        DESCRIPTION: Verify the details of all the bets which are displayed in the cashout tab
        EXPECTED: The details of the bets placed in the selected date range which has the cashout option should be displayed in the cashout tab.
        """
        pass
