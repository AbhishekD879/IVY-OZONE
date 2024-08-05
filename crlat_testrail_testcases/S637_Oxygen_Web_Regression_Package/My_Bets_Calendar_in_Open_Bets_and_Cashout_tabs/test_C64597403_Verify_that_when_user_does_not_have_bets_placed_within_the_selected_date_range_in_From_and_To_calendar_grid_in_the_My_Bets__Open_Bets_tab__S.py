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
class Test_C64597403_Verify_that_when_user_does_not_have_bets_placed_within_the_selected_date_range_in_From_and_To_calendar_grid_in_the_My_Bets__Open_Bets_tab__Sports_section(Common):
    """
    TR_ID: C64597403
    NAME: Verify that when user does not have bets placed within the selected date range in From and To calendar grid in the My Bets -> Open Bets tab -> Sports section.
    DESCRIPTION: Verify that when user does not have bets placed within the selected date range in From and To calendar grid in the My Bets -&gt; Open Bets tab -&gt; Sports section.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Open Bets tab -&gt; Sports section.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_open_bets_tabtabletdesktop_my_bets_section__gt_open_bets_tab(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Open Bets tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Open Bets tab'.
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the My Bets tab -&gt; Sports.
        """
        pass

    def test_002_select_a_date_range_in_the_from_and_to_calendar_grids_in_the_open_bets_tab_for_which_the_user_does_not_have_bets(self):
        """
        DESCRIPTION: Select a date range in the From and To calendar grids in the Open Bets tab for which the user does not have bets.
        EXPECTED: Verify that the message shows up stating that "You currently have no open bets".
        """
        pass
