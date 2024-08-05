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
class Test_C64597391_Verify_the_pagination_functionality_for_the_calendar_range_selected_in_the_Cashout_tab(Common):
    """
    TR_ID: C64597391
    NAME: Verify the pagination functionality for the calendar range selected in the Cashout tab.
    DESCRIPTION: Verify the pagination functionality for the calendar range selected in the Cashout tab.
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

    def test_002_verify_the_details_of_all_the_bets_which_are_displayed_in_the_cashout_tab(self):
        """
        DESCRIPTION: Verify the details of all the bets which are displayed in the cashout tab.
        EXPECTED: The details of the bets placed in the selected date range which has the cashout option should be displayed in the cashout tab.
        """
        pass

    def test_003_scroll_down_to_the_end_of_the_20_records_displayed_in_the_cashout_tab(self):
        """
        DESCRIPTION: Scroll down to the end of the 20 records displayed in the cashout tab.
        EXPECTED: On scroll to the bottom of first 20 bets the next consecutive 20 bets get populated.
        """
        pass
