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
class Test_C64597401_Verify_fetching_data_for_a_date_range_beyond_four_years_in_the_From_and_To_calendar_grids_in_the_My_Bets__Open_Bets_tab__Sports_section(Common):
    """
    TR_ID: C64597401
    NAME: Verify fetching data for a date range beyond four years in the From and To calendar grids in the My Bets -> Open Bets tab -> Sports section.
    DESCRIPTION: Verify fetching data for a date range beyond four years in the From and To calendar grids in the My Bets -&gt; Open Bets tab -&gt; Sports section.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Open Bets tab -&gt; Sports section.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_open_bets_tabtabletdesktop_my_bets_section__gt_open_bets_tab(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Open Bets tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Open Bets tab'.
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the My Bets tab -&gt; Sports section.
        """
        pass

    def test_002_select_a_date_range_beyond_four_years_in_the_from_and_to_calendar_grids_in_the_open_bets_tab(self):
        """
        DESCRIPTION: Select a date range beyond four years in the From and To calendar grids in the Open Bets tab.
        EXPECTED: Verify that the message shows up stating that "If you require account or gambling history over longer periods, or details of unsettled bets placed over 4 years ago, please contact us."
        """
        pass
