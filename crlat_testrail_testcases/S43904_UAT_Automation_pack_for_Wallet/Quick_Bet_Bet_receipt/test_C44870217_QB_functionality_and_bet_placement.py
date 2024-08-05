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
class Test_C44870217_QB_functionality_and_bet_placement(Common):
    """
    TR_ID: C44870217
    NAME: QB functionality and bet placement
    DESCRIPTION: This test case verifies QB functionality. Applicable for MOBILE only.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_for_a_logged_out_user__add_to_betslip_button_is_active_log_in__place_bet_is_inactive_when_no_stake_is_entered(self):
        """
        DESCRIPTION: For a logged out user > 'ADD TO BETSLIP' button is active 'LOG IN & PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'ADD TO BETSLIP' button is active 'LOG IN & PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'LOG IN & PLACE BET' button becomes active only when stake is entered.
        """
        pass

    def test_003_check_for_logged_in_user_add_to_betslip_button_is_active_place_bet_is_inactive_when_no_stake_is_entered(self):
        """
        DESCRIPTION: Check for logged in user 'ADD TO BETSLIP' button is active 'PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'ADD TO BETSLIP' button is active 'LOG IN & PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'PLACE BET' button becomes active only when stake is entered.
        """
        pass

    def test_004_verify_quick_bet_display_when_user_clicks_on_selection(self):
        """
        DESCRIPTION: "Verify quick bet display when user clicks on selection
        EXPECTED: Quick bet pop up displayed
        """
        pass

    def test_005__check_quick_stake_selections_works_properly_click_on_quick_stake_and_check_stake_box_display(self):
        """
        DESCRIPTION: -Check quick stake selections works properly (click on quick stake and check stake box display)
        EXPECTED: Quick stake boxes displayed as £5 £10 £50 and £100
        """
        pass

    def test_006__check_display_of_key_pad_when_user_taps_on_stake_box(self):
        """
        DESCRIPTION: -Check display of Key Pad when user taps on stake box
        EXPECTED: Key pad displayed
        """
        pass

    def test_007__verify_display_and_correctness_of_price_change_notification(self):
        """
        DESCRIPTION: -Verify display and correctness of price change notification
        EXPECTED: up sell message displayed
        """
        pass

    def test_008__check_bet_placed_successfully_as_per_design_inc_tick_icon(self):
        """
        DESCRIPTION: -Check Bet Placed Successfully' as per design (inc tick icon)
        EXPECTED: Bet placed successfully
        """
        pass

    def test_009__check_display_of_selection_name_market_name_stake_odds_est_returns_in_the_quick_bet_slip(self):
        """
        DESCRIPTION: -Check display of Selection name, market name, stake, Odds, Est. Returns in the quick bet slip
        EXPECTED: 
        """
        pass

    def test_010__check_cashout_icon_on_the_quick_betslip_receipt(self):
        """
        DESCRIPTION: -Check Cashout icon on the Quick betslip receipt
        EXPECTED: Cash out icon is displayed in betslip
        """
        pass

    def test_011__check_date(self):
        """
        DESCRIPTION: -Check Date
        EXPECTED: Date is displayed
        """
        pass

    def test_012__check_event_name_selection_pricemarket_name(self):
        """
        DESCRIPTION: -Check event name, selection price,market name.
        EXPECTED: Event name, market name and price displayed on Quick bet slip
        """
        pass

    def test_013__check_potential_returns(self):
        """
        DESCRIPTION: -Check potential returns
        EXPECTED: Potential/Estimated returns calculated correct
        """
        pass

    def test_014__check_bet_receipt_display_of_selection_name_market_name_stake_odds_est_returns_and_receipt_number(self):
        """
        DESCRIPTION: -Check bet receipt display of Selection name, market name, stake, Odds, Est. Returns and receipt number
        EXPECTED: Selection name, market name, stake, Odds, Est. Returns and receipt  are displayed on betslip
        """
        pass

    def test_015__check_header_balance_update_after_placing_bet(self):
        """
        DESCRIPTION: -Check header balance update after placing bet
        EXPECTED: Balance updated
        """
        pass

    def test_016_check_bets_are_displaying_in_my_bets_open_bets_and_settle_bets(self):
        """
        DESCRIPTION: Check bets are displaying in my bets open bets and settle bets
        EXPECTED: Bets are displayed in Openbets and settle bets
        """
        pass
