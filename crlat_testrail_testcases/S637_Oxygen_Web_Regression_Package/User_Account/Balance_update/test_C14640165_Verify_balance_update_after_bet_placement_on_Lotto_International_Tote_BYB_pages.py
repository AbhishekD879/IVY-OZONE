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
class Test_C14640165_Verify_balance_update_after_bet_placement_on_Lotto_International_Tote_BYB_pages(Common):
    """
    TR_ID: C14640165
    NAME: Verify balance update after bet placement on Lotto, International Tote, BYB pages
    DESCRIPTION: This test case verifies successful balance update after bet placement on Lotto, International Tote pages
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: User is logged in.
    """
    keep_browser_open = True

    def test_001_go_to_lotto_page(self):
        """
        DESCRIPTION: Go to Lotto page
        EXPECTED: Lotto page is opened
        """
        pass

    def test_002_choose_any_digits_in_ballsenter_any_stake(self):
        """
        DESCRIPTION: Choose any digits in balls
        DESCRIPTION: Enter any stake
        EXPECTED: 'Place Bet for amount of stake' button becomes enabled.
        """
        pass

    def test_003_tap_on_place_bet_for_amount_of_stake_button(self):
        """
        DESCRIPTION: Tap on 'Place Bet for amount of stake' button.
        EXPECTED: 'Confirm?' button appears
        """
        pass

    def test_004_tap_on_confirm_buttonverify_the_balance(self):
        """
        DESCRIPTION: Tap on 'Confirm?' button
        DESCRIPTION: Verify the balance
        EXPECTED: Bet receipt is displayed
        EXPECTED: Balance is updated automatically, it is decremented by entered stake.
        """
        pass

    def test_005_tap_on_done_buttonswitch_to_international_tote_page(self):
        """
        DESCRIPTION: Tap on 'Done' button
        DESCRIPTION: Switch to International Tote page
        EXPECTED: International Tote page is opened
        """
        pass

    def test_006_tap_on_any_evententer_any_stake(self):
        """
        DESCRIPTION: Tap on any event
        DESCRIPTION: Enter any stake
        EXPECTED: 'BET NOW' button becomes enabled.
        """
        pass

    def test_007_tap_on_bet_now_buttonverify_the_balance(self):
        """
        DESCRIPTION: Tap on 'BET NOW' button
        DESCRIPTION: Verify the balance
        EXPECTED: Balance is updated automatically, it is decremented by entered stake.
        """
        pass

    def test_008_add_2_selection_to_the_betslip_from_below_build_your_bet_tab(self):
        """
        DESCRIPTION: Add 2 selection to the betslip from below Build your bet tab
        EXPECTED: Selection are added
        EXPECTED: A tab with selections appears with a "Place Bet" button
        """
        pass

    def test_009_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place Bet" button
        EXPECTED: Betslip is opened at the bottom of page (UI is similar to quick bet);
        """
        pass

    def test_010_enter_any_stake_less_than_user_balancetap_on_place_bet_button(self):
        """
        DESCRIPTION: Enter any stake less than user balance
        DESCRIPTION: Tap on 'PLACE BET' button
        EXPECTED: Bet Receipt is displayed
        """
        pass

    def test_011_close_bet_receipt_screenverify_the_balance(self):
        """
        DESCRIPTION: Close Bet Receipt screen
        DESCRIPTION: Verify the balance
        EXPECTED: Balance is updated automatically, it is decremented by entered stake.
        """
        pass
