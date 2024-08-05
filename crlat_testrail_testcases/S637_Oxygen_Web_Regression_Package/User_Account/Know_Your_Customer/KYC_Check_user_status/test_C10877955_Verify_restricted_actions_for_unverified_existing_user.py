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
class Test_C10877955_Verify_restricted_actions_for_unverified_existing_user(Common):
    """
    TR_ID: C10877955
    NAME: Verify restricted actions for unverified existing user
    DESCRIPTION: This test case verifies that user is restricted to perform certain actions (like depositing/placing any bets/withdrawing) when his account is under review and is shown corresponding overlay.
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. User has logged in to application and has positive balance
    PRECONDITIONS: 3. User is on Home page and is able to browse the site
    PRECONDITIONS: 4. User account is under verification (Check for IMS 'age verification result' status = Active Grace period and Player tags = "AGP_Success_Upload=5 (or less than 5) & Verfication_Review")
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - Player tags (in IMS) are documented here and are key sensitive : https://docs.google.com/spreadsheets/d/1RM5-9MnsmsSErdENXQUrBzDJAzsroIfpYblObwnrqG8/edit#gid=0
    """
    keep_browser_open = True

    def test_001_add_any_selection_to_betslip_enter_stake_and_hit_bet_now_button(self):
        """
        DESCRIPTION: Add any selection to betslip, enter stake and hit 'Bet Now' button
        EXPECTED: - User is shown the Account in review overlay (message CMS configurable)
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_002_click_on_close_button_on_the_overlay(self):
        """
        DESCRIPTION: Click on close button on the overlay
        EXPECTED: Overlay is closed
        """
        pass

    def test_003_enter_stake_that_is_bigger_than_user_balance_and_hit_make_a_quick_deposit_button_that_is_shown(self):
        """
        DESCRIPTION: Enter stake that is bigger than user balance, and hit 'Make a quick deposit' button that is shown
        EXPECTED: User is shown the details of deposit that has to be filled in
        """
        pass

    def test_004_populate_fields_with_valid_data_and_hit_deposit_and_bet_button(self):
        """
        DESCRIPTION: Populate fields with valid data and hit 'Deposit and Bet' button
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to Deposit
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_005_close_overlay_and_clear_the_betslip_add_any_selection_to_quick_bet_and_hit_bet_now_button(self):
        """
        DESCRIPTION: Close overlay and clear the betslip, add any selection to Quick Bet, and hit 'Bet Now' button
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_006_close_overlay_enter_stake_bigger_than_user_balance_in_quick_bet_input_field_and_click_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Close overlay, enter stake bigger than user balance in quick bet input field and click 'Make a quick deposit' button
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to Deposit
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_007_close_the_overlay(self):
        """
        DESCRIPTION: Close the overlay
        EXPECTED: - Overlay is closed
        EXPECTED: - User is on same page he was before
        """
        pass

    def test_008_in_right_user_menu_click_on_deposit(self):
        """
        DESCRIPTION: In right user menu click on Deposit
        EXPECTED: - User is shown same overlay again
        EXPECTED: - User is not able to navigate to Deposit page and deposit money
        """
        pass

    def test_009_close_the_overlay_and_click_on_withdraw_in_right_user_menu(self):
        """
        DESCRIPTION: Close the overlay and click on 'Withdraw' in right user menu
        EXPECTED: - User is shown same overlay again
        EXPECTED: - User is not able to navigate to 'Withdraw' page and withdraw money
        """
        pass

    def test_010_close_the_overlay_and_click_on_cancel_withdraw_in_right_user_menu(self):
        """
        DESCRIPTION: Close the overlay and click on 'Cancel Withdraw' in right user menu
        EXPECTED: - User is able to navigate to 'Cancel Withdraw' page but cannot cancel money withdraw (when available)
        EXPECTED: - User is shown same overlay after pressing 'Cancel' button
        """
        pass

    def test_011_close_the_overlay_and_click_on_my_freebets__bonuses_in_right_user_menu(self):
        """
        DESCRIPTION: Close the overlay and click on 'My Freebets & Bonuses' in right user menu
        EXPECTED: - User is shown same overlay again
        EXPECTED: - User is not able to navigate to this page
        """
        pass

    def test_012_add_any_selection_to_betslip_open_betslip_and_try_to_place_bet_using_freebet_if_available_hit_bet_now_button(self):
        """
        DESCRIPTION: Add any selection to betslip, open betslip and try to place bet using Freebet (if available), hit 'Bet Now' button
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_013_navigate_to_hr_landing_page_add_any_selection_to_betslip_from_uk_tote_pool_enter_stake_and_hit_bet_now_button_in_betslip(self):
        """
        DESCRIPTION: Navigate to HR landing page, add any selection to betslip from UK tote pool, enter stake and hit 'Bet Now' button in betslip
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_014_navigate_to_hr_landing_page_add_any_selection_to_betslip_from_international_tote_pool_enter_stake_and_hit_bet_now_button_in_betslip(self):
        """
        DESCRIPTION: Navigate to HR landing page, add any selection to betslip from International tote pool, enter stake and hit 'Bet Now' button in betslip
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_015_navigate_to_football_jackpot_if_available_add_selections_to_bet_builder_and_hit_bet_now_button(self):
        """
        DESCRIPTION: Navigate to Football: Jackpot (if available), add selections to bet builder and hit 'Bet now' button
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to place a bet
        """
        pass

    def test_016_navigate_to_lotto_from_sports_menu_ribbon_add_selections_to_bet_builder_and_hit_place_bet_button(self):
        """
        DESCRIPTION: Navigate to Lotto from sports menu ribbon, add selections to bet builder and hit 'Place Bet' button
        EXPECTED: - User is shown the overlay
        EXPECTED: - User is not able to place a bet
        """
        pass
