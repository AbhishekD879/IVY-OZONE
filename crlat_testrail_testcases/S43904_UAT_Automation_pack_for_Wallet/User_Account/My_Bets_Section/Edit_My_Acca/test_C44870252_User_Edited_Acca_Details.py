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
class Test_C44870252_User_Edited_Acca_Details(Common):
    """
    TR_ID: C44870252
    NAME: "User Edited Acca Details
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User have accumulator bets on my bets area
    PRECONDITIONS: and has some EMA bets
    """
    keep_browser_open = True

    def test_001_verify_user_should_able_to_see_the_details_of_an_edited_acca_in_account_history(self):
        """
        DESCRIPTION: Verify user should able to see the details of an edited acca in account history
        EXPECTED: Verify is able to see the details of an edited acca in account history
        """
        pass

    def test_002_check_if_the_selection_name_is_displayed_for_all_remaining_selections_and_returns(self):
        """
        DESCRIPTION: Check if the selection name is displayed for all remaining selections and returns
        EXPECTED: Selection name is displayed for all remaining selections and returns
        """
        pass

    def test_003___verify_user_sees_selections_which_were_removed_have_a_removed_token_displayed_on_open_bets(self):
        """
        DESCRIPTION: - Verify user sees selection(s) which were removed have a Removed token displayed on open bets
        EXPECTED: user sees selection(s) which were removed have a Removed token displayed on open bets
        """
        pass

    def test_004___verify_my_bets_show_edit_history_functionality(self):
        """
        DESCRIPTION: - Verify my bets 'SHOW EDIT HISTORY' functionality
        EXPECTED: 'SHOW EDIT HISTORY' functionality displayed
        """
        pass

    def test_005___verify_show_edit_history_under_my_bets__verify_show_edit_history_shows_edited_history_on_my_bets_on_same_page__verify_user_can_foldunfold_show_edit_history_page_each_acca_bets__verify_user_sees_show_edit_history_under_my_bets_settle_bets_verify_settle_bets_show_edit_history__button_click_opens_show_edit_history__page__verfiy_show_edit_history_summary_details_and_it_should_havetitle__oddsmarketevent__date__time_stamp(self):
        """
        DESCRIPTION: - Verify 'SHOW EDIT HISTORY' under my bets
        DESCRIPTION: - Verify 'SHOW EDIT HISTORY' shows edited history on my bets on same page.
        DESCRIPTION: - Verify user can fold/unfold 'SHOW EDIT HISTORY' page each ACCA bets
        DESCRIPTION: - Verify user sees 'SHOW EDIT HISTORY' under my bets settle bets
        DESCRIPTION: -Verify settle bets 'SHOW EDIT HISTORY'  button click opens 'SHOW EDIT HISTORY'  page
        DESCRIPTION: - Verfiy 'SHOW EDIT HISTORY summary details and it should have
        DESCRIPTION: Title & odds
        DESCRIPTION: Market
        DESCRIPTION: Event , date & time stamp
        EXPECTED: User displayed with
        EXPECTED: 'SHOW EDIT HISTORY' under my bets
        EXPECTED: SHOW EDIT HISTORY' shows edited history on my bets on same page.
        EXPECTED: User can fold/unfold 'SHOW EDIT HISTORY' page each ACCA bets
        EXPECTED: User sees 'SHOW EDIT HISTORY' under my bets settle bets (
        EXPECTED: 'SHOW EDIT HISTORY'  button click opens 'SHOW EDIT HISTORY'  page
        EXPECTED: 'SHOW EDIT HISTORY summary details displays
        EXPECTED: Title & odds
        EXPECTED: Market
        EXPECTED: Event , date & time stamp
        """
        pass

    def test_006___verify_edit_history_details_for_singlemultiple_edit(self):
        """
        DESCRIPTION: - Verify Edit History details for Single/Multiple edit
        EXPECTED: Edit History details for Single/Multiple edit displays
        EXPECTED: For Each bet:
        EXPECTED: Header
        EXPECTED: the total stake which was used at the time of bet placement
        EXPECTED: Receipt ID is displayed
        EXPECTED: Date and Time of bet placement is displayed
        EXPECTED: Cashout History : Stake Used and Cashed out value
        EXPECTED: For each selection:
        EXPECTED: the selection name
        EXPECTED: the market names
        EXPECTED: the event name is displayed
        EXPECTED: Event Date and Time is displayed
        EXPECTED: Selection Price is displayed when bet was placed
        EXPECTED: the returns status
        """
        pass

    def test_007___verify_edit_history_details_with_won_lost_indicator_settled_bets_and_summary_details_same_as_above_(self):
        """
        DESCRIPTION: - Verify EDIT HISTORY DETAILS with won/ lost indicator (Settled bets) and summary details same as above ."
        EXPECTED: EDIT HISTORY DETAILS displayed with won/ lost indicator (Settled bets) and summary details same as above ."
        """
        pass
