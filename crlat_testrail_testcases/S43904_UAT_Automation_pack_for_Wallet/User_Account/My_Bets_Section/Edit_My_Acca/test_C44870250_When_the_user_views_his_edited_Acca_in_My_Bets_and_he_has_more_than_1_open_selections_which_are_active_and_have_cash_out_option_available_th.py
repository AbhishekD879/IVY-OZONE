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
class Test_C44870250_When_the_user_views_his_edited_Acca_in_My_Bets_and_he_has_more_than_1_open_selections_which_are_active_and_have_cash_out_option_available_then_the_cash_out_button_must_be_displayed_with_Cash_out_value_on_the_button_bVerify_Edit_My_Bet_button_is_n(Common):
    """
    TR_ID: C44870250
    NAME: "When the user views his edited Acca in My Bets and he has more than 1 open selections which are active and have cash out option available then the cash out button must be displayed with Cash out value on the button (b)Verify Edit My Bet button is n
    DESCRIPTION: "When the user views his edited Acca in My Bets and he has more than 1 open selections which are active and have cash out option available then the cash out button must be displayed with Cash out value on the button
    DESCRIPTION: (b)Verify Edit My Bet button is no longer displayed for the user when only one selection remains open ."
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_when_the_user_views_his_edited_acca_in_my_bets_and_he_has_more_than_1_open_selections_which_are_active_and_have_cash_out_option_available_then_the_cash_out_button_must_be_displayed_with_cash_out_value_on_the_button(self):
        """
        DESCRIPTION: When the user views his edited Acca in My Bets and he has more than 1 open selections which are active and have cash out option available then the cash out button must be displayed with Cash out value on the button
        EXPECTED: We should only see a cash out button
        """
        pass

    def test_002_verify_edit_my_bet_button_is_no_longer_displayed_for_the_user_when_only_one_selection_remains_open(self):
        """
        DESCRIPTION: Verify Edit My Bet button is no longer displayed for the user when only one selection remains open
        EXPECTED: The Edit My Bet button should not be available
        """
        pass
