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
class Test_C169181_to_update_FT_Finished_label_for_settled_selections(Common):
    """
    TR_ID: C169181
    NAME: (to update) 'FT'/'Finished' label for settled selections
    DESCRIPTION: To update: settled single bets are not displayed in cashout tab, this can be tested only for non settled multiples. What are special mathces and how to make create them? 'Finished' label is not displayed, intended?
    DESCRIPTION: This test case verified 'FT'/'Finished' label or its absence for settled selections on 'Cash Out' tab
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets on Football and some other sport events (usual match, special match and not match) where Cash Out offer is available;
    PRECONDITIONS: *   Selections within placed bet are settled
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_within_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab within 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_label_near_event_name_within_single_bet_for_not_special_football_match(self):
        """
        DESCRIPTION: Verify label near Event name within single bet for **not special football match**
        EXPECTED: **'FT'** label is displayed between Event name and Match Scores
        """
        pass

    def test_003_verify_label_near_event_name_within_single_bet_for_not_special_and_not_football_match(self):
        """
        DESCRIPTION: Verify label near Event name within single bet for **not special and not football match**
        EXPECTED: **'Finished'** label is displayed on the right side of Event Name
        """
        pass

    def test_004_verify_label_near_event_name_within_single_bet_for_special_sport_match(self):
        """
        DESCRIPTION: Verify label near Event name within single bet for **special sport match**
        EXPECTED: **Event Start Time/Date** is displayed on the right side of Event Name
        """
        pass

    def test_005_verify_label_near_event_name_within_single_bet_for_sport_outrighttournament(self):
        """
        DESCRIPTION: Verify label near Event name within single bet for **sport outright/tournament**
        EXPECTED: **Event Start Time/Date** is displayed on the right side of Event Name
        """
        pass

    def test_006_repeat_steps_2_5_for_selections_within_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #2-5 for selections within **Multiple** bets
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_6_on_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-6 on 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
