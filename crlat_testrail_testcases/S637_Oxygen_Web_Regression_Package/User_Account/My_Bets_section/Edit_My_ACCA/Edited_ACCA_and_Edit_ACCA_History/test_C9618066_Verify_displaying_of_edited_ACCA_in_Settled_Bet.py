import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C9618066_Verify_displaying_of_edited_ACCA_in_Settled_Bet(Common):
    """
    TR_ID: C9618066
    NAME: Verify displaying of edited ACCA in Settled Bet
    DESCRIPTION: This test case verifies the view of an edited ACCA on My Bets>Settled Bets
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA5)
    PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 4. Remove few selections from the bet and save changes
    PRECONDITIONS: Note: all data in Step1 is based on received data from BPP in Network -> accountHistory?detailLevel=DETAILED&fromDate=<DateFrom>%2000%3A00%3A00&toDate=<DateTo> Request
    """
    keep_browser_open = True

    def test_001_go_to_my_betsopen_betsverify_that_the_edited_acca_is_shown_with_all_appropriate_elements(self):
        """
        DESCRIPTION: Go to My Bets>Open Bets
        DESCRIPTION: Verify that the edited ACCA is shown with all appropriate elements
        EXPECTED: The edited ACCA is shown with appropriate elements:
        EXPECTED: - Updated ACCA Bet Type
        EXPECTED: - Bet Result for ACCA bet
        EXPECTED: - Total stake which was used for the edited ACCA
        EXPECTED: - Returns value
        EXPECTED: - Event name is displayed for all remaining selections
        EXPECTED: - Event Date and Time
        EXPECTED: - Market names for all remaining selections
        EXPECTED: - Selection name for all remaining selections
        EXPECTED: - Prices accepted for the new ACCA for all selections
        EXPECTED: - Scores result (if available)
        EXPECTED: - Status for each selection
        EXPECTED: - 'SHOW EDIT HISTORY' button is shown
        """
        pass

    def test_002_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets(self):
        """
        DESCRIPTION: Make a placed bet (edited bet) SETTLED (add and settle the result for each event in the edited bet)
        DESCRIPTION: Verify that the new bet is resulted and shown on By Bets>(Bet History)Settled Bets
        EXPECTED: - Edited Bet is resulted
        EXPECTED: - Edited Bet is shown on By Bets>(Bet History)Settled Bets
        """
        pass

    def test_003_go_to_by_betsbet_historysettled_betsverify_that_the_edited_acca_is_shown_with_all_appropriate_elements(self):
        """
        DESCRIPTION: Go to By Bets>(Bet History)Settled Bets
        DESCRIPTION: Verify that the edited ACCA is shown with all appropriate elements
        EXPECTED: The edited ACCA is shown with appropriate elements:
        EXPECTED: - Updated ACCA Bet Type
        EXPECTED: - Bet Result for ACCA bet
        EXPECTED: - Date and time of when the bet was placed
        EXPECTED: - Total stake which was used for the edited ACCA
        EXPECTED: - Returns value
        EXPECTED: - New Bet Receipt ID
        EXPECTED: - Event name is displayed for all remaining selections
        EXPECTED: - Event Date and Time
        EXPECTED: - Market names for all remaining selections
        EXPECTED: - Selection name for all remaining selections
        EXPECTED: - Prices accepted for the new ACCA for all selections
        EXPECTED: - Scores result (if available)
        EXPECTED: - Status for each selection
        EXPECTED: - 'SHOW EDIT HISTORY' button is shown
        """
        pass
