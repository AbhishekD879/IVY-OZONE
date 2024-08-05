import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C23201004_Verify_available_Free_Bets_eligibility(Common):
    """
    TR_ID: C23201004
    NAME: Verify available Free Bets eligibility
    DESCRIPTION: This test case verifies that eligible and NOT eligible Free Bets are displayed to user in Free Bets pop up. User should not be able to use Free Bet in case freebet / lines < 0.01
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has Free Bets available on their account (please add Free Bets with small value for, e.g. £0.10 £0.05)
    PRECONDITIONS: * User has multiple racing selections with E/W added to the Betslip
    PRECONDITIONS: -----
    PRECONDITIONS: - For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: - For PROD/HL env.:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a £5+ Win or £5+ Each Way bet on any sport. Coral will give you an instant four x £5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb/#!/promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of £5 win or £5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True

    def test_001_open_bet_slip_and_press_on_use_free_bet_link_under_multiple_bet_type_from_preconditioneg_if_you_have_010_free_bet_try_to_use_it_on_5_fold_acca_x11_multiple_bet(self):
        """
        DESCRIPTION: Open Bet Slip and press on "Use Free Bet" link under multiple bet type from precondition.
        DESCRIPTION: E.g. If you have £0.10 free bet try to use it on 5 Fold Acca (x11) multiple bet
        EXPECTED: Free Bet pop up is shown with list of Free Bets available
        """
        pass

    def test_002_validate_that_not_eligible_free_bets_are_present_on_free_bets_popup(self):
        """
        DESCRIPTION: Validate that NOT eligible free bets are present on Free Bets popup
        EXPECTED: All Free Bets (eligible and not eligible) for selected bet are displayed
        """
        pass

    def test_003__select_not_eligible_free_bet_tap_add_button(self):
        """
        DESCRIPTION: * Select NOT eligible free bet
        DESCRIPTION: * Tap 'Add' button
        EXPECTED: [From OX100.1]
        EXPECTED: * 'Free Bet Not Eligible' pop-up with 'Sorry, your free bet cannot be added.' text appears
        EXPECTED: * If [freebet value] / [lines number] is < 0.01 then this Free Bet(s) is not eligible
        EXPECTED: (e.g. if user has £0.10 free bet then it will NOT be available for multiple bets with x11 and more lines)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/38723)
        """
        pass

    def test_004_close_popup_by_tapping_ok_button(self):
        """
        DESCRIPTION: Close popup by tapping 'Ok' button
        EXPECTED: Pop up is closed
        """
        pass

    def test_005_select_each_way_checkbox_first_under_multiple_bet_and_after_select_freebet_where_free_bet_value_less_than_001_eg_010_free_bet_for_double_x6_multiple_bet_0106_per_line_and_01062_per_line_for_ew(self):
        """
        DESCRIPTION: Select Each Way checkbox first under multiple bet and after select FreeBet where free bet value less than 0.01 (e.g. £0.10 free bet for Double (x6) multiple bet 0.10/6 per line and 0.10/6/2 per line for E/W)
        EXPECTED: [From OX100.1]
        EXPECTED: * 'Free Bet Not Eligible' pop-up with 'Sorry, your free bet cannot be added.' text appears
        EXPECTED: * If [freebet value] / [lines number] is < 0.01 then this Free Bet(s) is not eligible
        EXPECTED: (e.g. if user has £0.10 free bet then it will NOT be available for multiple bets with x6 and more lines with E/W option checked)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/38723)
        """
        pass

    def test_006_close_popup_by_tapping_ok_button(self):
        """
        DESCRIPTION: Close popup by tapping 'Ok' button
        EXPECTED: Pop up is closed
        EXPECTED: EW is checked, and free bet is not selected
        """
        pass

    def test_007_verify_that_free_bet_not_eligible_is_displayed_when_selected_free_bet_becomes_not_eligible_after_ew_option_is_selectedadd_eligible_free_bet_to_multiple_bet_eg_010_on_double_x6_and_after_that_click_on_ew_checkbox(self):
        """
        DESCRIPTION: Verify that "Free Bet Not Eligible" is displayed when selected Free Bet becomes not eligible AFTER E/W option is selected.
        DESCRIPTION: Add eligible Free Bet to multiple bet (e.g. £0.10 on Double (x6)) and after that click on E/W checkbox.
        EXPECTED: Popup with message is displayed:
        EXPECTED: “Heading: Free Bet Not Eligible
        EXPECTED: Text: Sorry, your free bet cannot be added.
        EXPECTED: Button: OK
        EXPECTED: When user taps on OK, popup is removed and EW is not checked, and free bet remains selected”
        """
        pass
