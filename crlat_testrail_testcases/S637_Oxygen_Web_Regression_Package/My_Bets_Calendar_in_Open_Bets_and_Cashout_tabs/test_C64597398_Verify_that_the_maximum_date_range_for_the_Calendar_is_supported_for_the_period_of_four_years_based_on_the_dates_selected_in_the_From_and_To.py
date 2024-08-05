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
class Test_C64597398_Verify_that_the_maximum_date_range_for_the_Calendar_is_supported_for_the_period_of_four_years_based_on_the_dates_selected_in_the_From_and_To_Calendar_grids_in_My_Bets_tab__Open_Bets__Sports_section(Common):
    """
    TR_ID: C64597398
    NAME: Verify that the maximum date range for the Calendar is supported for the period of four years based on the dates selected in the From and To Calendar grids in My Bets tab - Open Bets -> Sports section
    DESCRIPTION: Verify that the maximum date range for the Calendar is supported for the period of four years based on the dates selected in the From and To Calendar grids in My Bets tab - Open Bets -&gt; Sports section
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Open Bets tab -&gt; Sports section.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_open_bets_tabtabletdesktop_my_bets_section__gt_open_bets__tab__gt_sports_section(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Open Bets tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Open Bets  tab -&gt; Sports section'
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the My Bets tab.
        """
        pass

    def test_002_select_a_date_range_of_4_years_span_in_the_from_and_to_calendar_grid_which_is_available(self):
        """
        DESCRIPTION: Select a date range of 4 years span in the From and To calendar grid which is available.
        EXPECTED: The user should be able to select the date range of 4 years in the Calendar grid by selecting the dates in the From and To Calendar grid available for the user.
        """
        pass

    def test_003_verify_the_details_of_all_the_bets_which_are_displayed_in_the_my_bets__gt_sports_section(self):
        """
        DESCRIPTION: Verify the details of all the bets which are displayed in the My Bets -&gt; Sports section.
        EXPECTED: The details of the bets placed in the selected date range four years should be displayed in the My Bets tab -. Open Bets -&gt; Sports section.
        """
        pass
