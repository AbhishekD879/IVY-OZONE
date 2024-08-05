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
class Test_C44870230_Verify_Free_Bet_notification_on_Header_for_logged_in_user(Common):
    """
    TR_ID: C44870230
    NAME: Verify Free Bet notification on Header for  logged in user
    DESCRIPTION: "-Verify Free Bet notification to Header area once user is logged into his account
    DESCRIPTION: 1.Customer places bets on any sports event using available Free bets which are sufficient for bet placement
    DESCRIPTION: - Check header balance
    DESCRIPTION: - Check freebet message on receipt
    DESCRIPTION: - Check Use FreeBet under selection in quick betslip
    DESCRIPTION: -Check user can use the freebet for placing bet(Single/multiple)
    DESCRIPTION: "
    PRECONDITIONS: UserName: goldenbuild1   Password : password1
    """
    keep_browser_open = True

    def test_001_launch_httpsbeta_sportscoralcouk_application(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/ application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_verify_free_bet_notification_on_header_area_once_user_is_logged_into_his_account(self):
        """
        DESCRIPTION: Verify Free Bet notification on Header area once user is logged into his account
        EXPECTED: Free bet (FB) notification displayed on the header.
        """
        pass

    def test_003_check_use_freebet_under_selection_in_quick_betslip(self):
        """
        DESCRIPTION: Check Use FreeBet under selection in quick betslip
        EXPECTED: user freebet hyperlink is displayed
        """
        pass

    def test_004_check_user_can_use_the_freebet_for_placing_betsinglemultiple(self):
        """
        DESCRIPTION: Check user can use the freebet for placing bet(Single/multiple)
        EXPECTED: Single and multiple bets are placed using free bets
        """
        pass

    def test_005_verify_user_can__places_bets_on_any_sports_event_using_available_free_bets_which_are_sufficient_for_bet_placement(self):
        """
        DESCRIPTION: Verify user can  places bets on any sports event using available Free bets which are sufficient for bet placement
        EXPECTED: Bet placed using freebet successfully
        """
        pass

    def test_006_verify_no_amount_is_deducted_from_header_balance(self):
        """
        DESCRIPTION: Verify No amount is deducted from header balance
        EXPECTED: Header balance display same
        """
        pass

    def test_007_verify__freebet_message_on_receipt(self):
        """
        DESCRIPTION: Verify  freebet message on receipt
        EXPECTED: Message displayed
        """
        pass
