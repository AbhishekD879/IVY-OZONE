import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870218_QB__Error_Handling(Common):
    """
    TR_ID: C44870218
    NAME: QB - Error Handling
    DESCRIPTION: "Verify User sees following errors on Quick bet
    DESCRIPTION: - ""There was an error when attempting to place your bet, please try again."" when there is Boosted Odds mismatch
    DESCRIPTION: -  ""Your Odds Boost has been expired/redeemed.' when token has already been used
    DESCRIPTION: -  ""Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets.""when Openbet TimeOut
    DESCRIPTION: -   ""Your bet has not been accepted. Please try again."" when bet is rejected
    DESCRIPTION: -   ""Sorry, one of the selections cannot be boosted, please remove the selection and try again."" when  Odds Boost not allowed for selection
    PRECONDITIONS: UserName: goldenbuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is displayed
        """
        pass

    def test_002_verify_user_can_select_any_in_play_selection(self):
        """
        DESCRIPTION: verify user can select any in-play selection
        EXPECTED: Selection selected and appear in green
        """
        pass

    def test_003_verify_selection_added_to_quick_bet(self):
        """
        DESCRIPTION: Verify selection added to Quick bet
        EXPECTED: Selection displayed in Quick bet popup
        """
        pass

    def test_004_verify_user_sees_following_errors_on_quick_bet__there_was_an_error_when_attempting_to_place_your_bet_please_try_again_when_there_is_boosted_odds_mismatch__your_odds_boost_has_been_expiredredeemed_when_token_has_already_been_used__sorry_there_may_have_been_a_problem_placing_your_bet_to_confirm_if_your_bet_was_placed_please_check_your_open_betswhen_openbet_timeout__your_bet_has_not_been_accepted_please_try_again_when_bet_is_rejected__sorry_one_of_the_selections_cannot_be_boosted_please_remove_the_selection_and_try_again_when_odds_boost_not_allowed_for_selection(self):
        """
        DESCRIPTION: "Verify User sees following errors on Quick bet
        DESCRIPTION: - ""There was an error when attempting to place your bet, please try again."" when there is Boosted Odds mismatch
        DESCRIPTION: - ""Your Odds Boost has been expired/redeemed.' when token has already been used
        DESCRIPTION: - ""Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets.""when Openbet TimeOut
        DESCRIPTION: - ""Your bet has not been accepted. Please try again."" when bet is rejected
        DESCRIPTION: - ""Sorry, one of the selections cannot be boosted, please remove the selection and try again."" when Odds Boost not allowed for selection
        EXPECTED: Error message displayed
        """
        pass
