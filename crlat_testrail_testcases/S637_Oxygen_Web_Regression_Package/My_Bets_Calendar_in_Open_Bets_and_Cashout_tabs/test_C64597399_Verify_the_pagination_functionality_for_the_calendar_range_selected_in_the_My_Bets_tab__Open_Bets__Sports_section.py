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
class Test_C64597399_Verify_the_pagination_functionality_for_the_calendar_range_selected_in_the_My_Bets_tab__Open_Bets__Sports_section(Common):
    """
    TR_ID: C64597399
    NAME: Verify the pagination functionality for the calendar range selected in the My Bets tab -. Open Bets -> Sports section.
    DESCRIPTION: Verify the pagination functionality for the calendar range selected in the My Bets tab -. Open Bets -&gt; Sports section.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Open Bets tab -&gt; Sports section.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_open_bets__gt_sports_tabtabletdesktop_my_bets_section__gt__open_bets_tab__gt_sports_section(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; Open Bets -&gt; Sports tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; ' Open Bets tab -&gt; Sports section'
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the My Bets tab -&gt; Open Bets -&gt; Sports section.
        """
        pass

    def test_002_verify_the_details_of_all_the_bets_which_are_displayed_in_the_my_bets__gt_open_bets__gt_sports_section(self):
        """
        DESCRIPTION: Verify the details of all the bets which are displayed in the My Bets -&gt; Open Bets -&gt; Sports section.
        EXPECTED: The details of the latest 20 bets placed in the selected date range should be displayed in the Open Bets -&gt; Sports tab.
        """
        pass

    def test_003_verify_the_details_of_all_the_bets_which_are_displayed_in_the_my_bets__gt_open_bets__gt_sports_section(self):
        """
        DESCRIPTION: Verify the details of all the bets which are displayed in the My Bets -&gt; Open Bets -&gt; Sports section.
        EXPECTED: The details of the latest 20 bets placed in the selected date range should be displayed in the Open Bets -&gt; Sports tab.
        """
        pass

    def test_004_scroll_down_to_the_end_of_the_20_records_displayed_in_the_my_bets__gt_open_bets__gt_sports_tab(self):
        """
        DESCRIPTION: Scroll down to the end of the 20 records displayed in the My Bets -&gt; Open Bets -&gt; Sports tab.
        EXPECTED: On scroll to the bottom of first 20 bets the next consecutive 20 bets get populated.
        """
        pass
