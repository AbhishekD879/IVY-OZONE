import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870222_Betslip__Error_Handling(Common):
    """
    TR_ID: C44870222
    NAME: Betslip - Error Handling
    DESCRIPTION: "Verify User sees following errors on betslip
    DESCRIPTION: - ""There was an error when attempting to place your bet, please try again."" when there is Boosted Odds mismatch
    DESCRIPTION: -  ""Your Odds Boost has been expired/redeemed.' when token has already been used
    DESCRIPTION: -  ""Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets.""when Openbet TimeOut
    DESCRIPTION: -   ""Your bet has not been accepted. Please try again."" when bet is rejected
    DESCRIPTION: -   ""Sorry, one of the selections cannot be boosted, please remove the selection and try again."" when  Odds Boost not allowed for selection
    PRECONDITIONS: User is logged in and has sufficient balance to place bets.
    PRECONDITIONS: And has some Odds boost offers.
    """
    keep_browser_open = True

    def test_001_open_the_siteapp_and_log_in_with_a_user_who_has_all_odds_boost_available(self):
        """
        DESCRIPTION: Open the site/app and log in with a user who has all odds boost available
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_a_selection_to_the_betslip_and_the_odds_on_the_betslip_have_been_boosted_when_there_is_a_odds_mismatch_verify_the_error_message_received(self):
        """
        DESCRIPTION: Add a selection to the betslip and the odds on the betslip have been boosted. When there is a odds mismatch, verify the error message received.
        EXPECTED: When there is a odds mismatch: Error message returned as
        EXPECTED: 'There was an error when attempting to place your bet, please try again.'
        """
        pass

    def test_003_add_a_selection_to_the_betslip_and_the_odds_on_the_betslip_have_been_boosted_verify_the_error_message_when_the_odds_boost_token_has_already_expired(self):
        """
        DESCRIPTION: Add a selection to the betslip and the odds on the betslip have been boosted. Verify the error message when the odds boost token has already expired
        EXPECTED: When the odds boost token has already expired: Error message returned as
        EXPECTED: 'Your Odds Boost has been expired/redeemed.'
        """
        pass

    def test_004_add_a_selection_to_the_betslip_and_the_odds_on_the_betslip_have_been_boosted_when_this_request_timesout_verify_the_error_message_received(self):
        """
        DESCRIPTION: Add a selection to the betslip and the odds on the betslip have been boosted. When this request timesout, verify the error message received.
        EXPECTED: When this request times out: Error message returned as
        EXPECTED: "Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets."
        """
        pass

    def test_005_add_a_selection_to_the_betslip_and_the_odds_on_the_betslip_have_been_boosted_when_this_request_is_rejected_verify_the_error_message_received(self):
        """
        DESCRIPTION: Add a selection to the betslip and the odds on the betslip have been boosted. When this request is rejected, verify the error message received.
        EXPECTED: When this request is rejected: Error message returned as
        EXPECTED: "Your bet has not been accepted. Please try again."
        """
        pass

    def test_006_add_a_selection_to_the_betslip_and_the_selection_is_not_allowed_for_odds_boost_verify_the_error_message_now(self):
        """
        DESCRIPTION: Add a selection to the betslip and the selection is not allowed for odds boost. Verify the error message now
        EXPECTED: Error message returned as:
        EXPECTED: "Sorry, one of the selections cannot be boosted, please remove the selection and try again."
        """
        pass
