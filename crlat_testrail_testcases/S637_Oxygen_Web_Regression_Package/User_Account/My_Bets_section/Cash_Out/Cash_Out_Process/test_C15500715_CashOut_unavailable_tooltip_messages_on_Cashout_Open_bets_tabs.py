import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C15500715_CashOut_unavailable_tooltip_messages_on_Cashout_Open_bets_tabs(Common):
    """
    TR_ID: C15500715
    NAME: CashOut unavailable tooltip messages on Cashout/Open bets tabs
    DESCRIPTION: This test case covers the messages which will be displayed to the user under bet placed depending on the error code received.
    DESCRIPTION: Designs Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f20923c692ebf5ccd63b3
    DESCRIPTION: Demo video link on one drive is available here:
    DESCRIPTION: https://coralracing-my.sharepoint.com/:v:/r/personal/sofiya_savka_ladbrokescoral_com/Documents/Coral%20Sportsbook%20Sprint%20Demos/PI15/Sprint%201/Web/BMA-39080-Cash-Out%20unavailable%20tooltip%20messages.mov?csf=1&e=e2UWWh
    DESCRIPTION: ![](index.php?/attachments/get/3051046)
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User is on Cashout/Open Bets tabs
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: * User has placed a bet using Free Bet where Cash Out offer is available
    PRECONDITIONS: Check the **accountHistory** responce for errors received or
    PRECONDITIONS: Coral CO Messages : https://confluence.egalacoral.com/pages/viewpage.action?pageId=58391155
    PRECONDITIONS: Charles installation guide: https://docs.google.com/document/d/1_7xC2eRQmXLWfiDRIOq9IUzrb964qG470AA0wCJEJug/edit?usp=sharing
    PRECONDITIONS: For this case you need to set a breakpoint for emulation error codes. Add a breakpoint to the cashoutBet response.
    PRECONDITIONS: ![](index.php?/attachments/get/31456)
    """
    keep_browser_open = True

    def test_001_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_code_with_the_help_of_charles_or_other_tool_availablecashout_bet_settled_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code (with the help of Charles or other tool available)
        DESCRIPTION: 'CASHOUT_BET_SETTLED' and observe the bet view
        EXPECTED: WHEN the user views the bet in the My Bets > Open Bets/Cashout tab or My Bets on event EDP, the following error message is displayed at the bottom of the bet, instead of 'Cashout' button:
        EXPECTED: **Your Cash Out attempt was unsuccessful as your bet has already been settled.**
        EXPECTED: The message is displayed on the grey background.
        """
        pass

    def test_002_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_codecashout_bet_cashed_out_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code:
        DESCRIPTION: 'CASHOUT_BET_CASHED_OUT' and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **Your Cash Out attempt was unsuccessful as your bet has already been Cashed Out.**
        """
        pass

    def test_003_find_bet_placed_using_free_bet_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_codecashout_freebet_used_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Find bet placed using Free bet, tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code:
        DESCRIPTION: 'CASHOUT_FREEBET_USED' and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **Bets placed with a free bet or bets triggering a free bet offer cannot be cashed out.**
        """
        pass

    def test_004_trigger_any_of_the_following_errors_code_while_confirming_cashout_processcashout_bet_no_cashoutcashout_singles_not_allowedcashout_multis_not_allowedcashout_bettype_not_allowedcashout_bet_not_loadedcashout_bettype_not_allowedcashout_disabledcashout_hcap_changedcashout_legsort_not_allowedand_observe_the_bet_view(self):
        """
        DESCRIPTION: Trigger any of the following errors code: (while confirming cashout process)
        DESCRIPTION: CASHOUT_BET_NO_CASHOUT
        DESCRIPTION: CASHOUT_SINGLES_NOT_ALLOWED
        DESCRIPTION: CASHOUT_MULTIS_NOT_ALLOWED
        DESCRIPTION: CASHOUT_BETTYPE_NOT_ALLOWED
        DESCRIPTION: CASHOUT_BET_NOT_LOADED
        DESCRIPTION: CASHOUT_BETTYPE_NOT_ALLOWED
        DESCRIPTION: CASHOUT_DISABLED
        DESCRIPTION: CASHOUT_HCAP_CHANGED
        DESCRIPTION: CASHOUT_LEGSORT_NOT_ALLOWED
        DESCRIPTION: and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **'Cash out is unavailable on this bet.**
        """
        pass

    def test_005_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_codecashout_pricetype_not_allowed_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code:
        DESCRIPTION: 'CASHOUT_PRICETYPE_NOT_ALLOWED' and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **Bets placed at starting price (SP) cannot be cashed out.**
        """
        pass

    def test_006_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_codecashout_cust_error_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code:
        DESCRIPTION: 'CASHOUT_CUST_ERROR' and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **Sorry, we cannot authorise Cash Out from your location.**
        """
        pass

    def test_007_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_errors_codecashout_cust_restrict_flagcashout_unavailable_cust_no_cashout_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following errors code:
        DESCRIPTION: 'CASHOUT_CUST_RESTRICT_FLAG'
        DESCRIPTION: 'CASHOUT_UNAVAILABLE_CUST_NO_CASHOUT' and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **'Sorry, we cannot authorise Cash Out from your account. Please contact us if you feel this may be in error**
        """
        pass

    def test_008_trigger_the_situation_when_bet_does_not_qualify_for_cash_out_because_the_cash_out_value_is_zero_openbet_ti_tool_for_current_selection_and_eg_change_price_from_41_to_4001_confirm_cashout_at_the_same_time_and_observe_the_bet(self):
        """
        DESCRIPTION: Trigger the situation when bet does not qualify for cash out because the cash-out value is zero (Openbet TI tool for current selection and e.g change price from 4/1 to 400/1), confirm cashout at the same time and observe the bet:
        EXPECTED: The following error message is displayed:
        EXPECTED: **Cash Out is unavailable because the offer is less than 0.00** and observe the bet view
        """
        pass

    def test_009_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_codecashout_no_odds__and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code:
        DESCRIPTION: 'CASHOUT_NO_ODDS'  and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **One or more events in your bet are not available for in-play Cash Out**
        """
        pass

    def test_010_tap_cashout_button_confirm_cashout_and_meanwhile_trigger_the_following_error_codecashout_seln_no_cashout_and_observe_the_bet_view(self):
        """
        DESCRIPTION: Tap 'Cashout' button, confirm cashout and meanwhile trigger the following error code:
        DESCRIPTION: 'CASHOUT_SELN_NO_CASHOUT' and observe the bet view
        EXPECTED: The following error message is displayed:
        EXPECTED: **One or more events in your bet are not available for cash out**
        """
        pass

    def test_011_trigger_the_situation_when_user_tries_to_cashout_bet_and_an_error_occurs_when_loadingerror_code_cashout_unavailable__sys_no_cashout(self):
        """
        DESCRIPTION: Trigger the situation when user tries to cashout bet and an error occurs when loading
        DESCRIPTION: Error code: 'CASHOUT_UNAVAILABLE_ SYS_NO_CASHOUT'
        EXPECTED: The following error message is displayed:
        EXPECTED: **Cash Out unsuccessful, please try again. **
        """
        pass
