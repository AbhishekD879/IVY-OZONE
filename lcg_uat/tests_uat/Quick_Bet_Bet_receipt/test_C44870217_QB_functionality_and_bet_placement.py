import random
import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.pages.shared.components.base import ComponentBase
from selenium.common.exceptions import ElementClickInterceptedException


@pytest.mark.p1
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870217_QB_functionality_and_bet_placement(BaseCashOutTest, ComponentBase):
    """
    TR_ID: C44870217
    NAME: QB functionality and bet placement
    DESCRIPTION: This test case verifies QB functionality. Applicable for MOBILE only.
    """
    keep_browser_open = True
    device_name = 'Nexus 5X' if not tests.use_browser_stack else tests.default_pixel
    selection_list = []
    bet_amount = 0.05
    count = 0

    def button_validation(self):
        bet_panel = self.site.quick_bet_panel
        self.assertTrue(bet_panel.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO BETSLIP" button is not active')
        self.assertFalse(bet_panel.place_bet.is_enabled(),
                         msg=f'"{vec.Betslip.LOGIN_AND_PLACE_BET_QUICK_BET}" button is enabled when stake in not entered')
        bet_panel.selection.content.amount_form.input.click()
        bet_panel.selection.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
        self.assertTrue(bet_panel.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO BETSLIP" button is not active')
        self.assertTrue(bet_panel.place_bet.is_enabled(),
                        msg=f'"{vec.Betslip.LOGIN_AND_PLACE_BET_QUICK_BET}" button is not enabled when stake is entered')

    def clear_stake_box(self):
        value = len(self.quick_bet.selection.content.amount_form.input.value)
        for i in range(0, value):
            self.quick_bet.selection.keyboard.enter_amount_using_keyboard(value='delete')
        self.quick_bet.header.click()

    def selections(self, selection):
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        length = len(bet_buttons_list)
        sel = 0
        for i in range(0, 10):
            index = random.randint(0, length)
            selection_btn = bet_buttons_list[index]
            self.site.contents.scroll_to_we(selection_btn)
            if selection_btn.is_enabled() and not selection_btn.is_selected() and selection_btn.text != 'SP':
                try:
                    selection_btn.click()
                    self.count += 1
                    sel = sel + 1
                except ElementClickInterceptedException:
                    print('ElementClickInterceptedException ..')
                    continue
            else:
                continue
            if sel == selection:
                return

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_for_a_logged_out_user__add_to_betslip_button_is_active_log_in__place_bet_is_inactive_when_no_stake_is_entered(self):
        """
        DESCRIPTION: For a logged out user > 'ADD TO BETSLIP' button is active 'LOG IN & PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'ADD TO BETSLIP' button is active 'LOG IN & PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'LOG IN & PLACE BET' button becomes active only when stake is entered.
        """
        self.selections(1)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
        self.button_validation()
        self.site.quick_bet_panel.header.close_button.click()

    def test_003_check_for_logged_in_user_add_to_betslip_button_is_active_place_bet_is_inactive_when_no_stake_is_entered(self):
        """
        DESCRIPTION: Check for logged in user 'ADD TO BETSLIP' button is active 'PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'ADD TO BETSLIP' button is active 'LOG IN & PLACE BET' is inactive when no stake is entered.
        EXPECTED: 'PLACE BET' button becomes active only when stake is entered.
        """
        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance
        self.site.open_betslip()
        betslip_content = self.get_betslip_content()
        betslip_content.remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()

        self.selections(1)
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.button_validation()
        self.clear_stake_box()

    def test_004_verify_quick_bet_display_when_user_clicks_on_selection(self):
        """
        DESCRIPTION: "Verify quick bet display when user clicks on selection
        EXPECTED: Quick bet pop up displayed
        """
        # This test step is covered in step 2

    def test_005__check_quick_stake_selections_works_properly_click_on_quick_stake_and_check_stake_box_display(self):
        """
        DESCRIPTION: -Check quick stake selections works properly (click on quick stake and check stake box display)
        EXPECTED: Quick stake boxes displayed as £5 £10 £50 and £100
        """
        index = 0
        quick_stake_list = self.quick_bet.quick_stake_panel.items_as_ordered_dict
        stake_list = self.quick_bet.quick_stake_panel.items
        for stake in self.quick_stakes:
            expected_key = ('+' + '£' + str(stake))
            self.assertIn(expected_key, quick_stake_list.keys(),
                          msg=f'"{expected_key}" not found in "{list(quick_stake_list.keys())}"')

            self.quick_bet.selection.content.amount_form.input.click()
            self.clear_stake_box()
            stake_list[index].click()
            expected_stack_value = (str(stake) + '.00')
            actual_stake_value = self.quick_bet.selection.content.amount_form.input.value
            self.assertEqual(actual_stake_value, expected_stack_value,
                             msg=f'Actual item:"{actual_stake_value}" not same as Expected: "{expected_stack_value}"')
            self.clear_stake_box()
            index = index + 1

    def test_006__check_display_of_key_pad_when_user_taps_on_stake_box(self):
        """
        DESCRIPTION: -Check display of Key Pad when user taps on stake box
        EXPECTED: Key pad displayed
        """
        self.quick_bet.selection.content.amount_form.input.click()
        self.assertTrue(self.quick_bet.selection.keyboard.is_displayed(), msg='Quick Bet input keyboard not displayed')

    def test_007__verify_display_and_correctness_of_price_change_notification(self):
        """
        DESCRIPTION: -Verify display and correctness of price change notification
        EXPECTED: up sell message displayed
        """
        # This step is not automatable

    def test_008__check_bet_placed_successfully_as_per_design_inc_tick_icon(self):
        """
        DESCRIPTION: -Check Bet Placed Successfully' as per design (inc tick icon)
        EXPECTED: Bet placed successfully
        """
        self.quick_bet.selection.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
        self.quick_bet.place_bet.click()
        self.assertTrue(self.quick_bet.bet_receipt.header.check_icon.is_displayed(), msg='tick icon not displayed')
        self.assertEqual(self.quick_bet.bet_receipt.header.bet_placed_text, vec.Betslip.SUCCESS_BET,
                         msg='Quick stake not working correctly')

    def test_009__check_display_of_selection_name_market_name_stake_odds_est_returns_in_the_quick_bet_slip(self):
        """
        DESCRIPTION: -Check display of Selection name, market name, stake, Odds, Est. Returns in the quick bet slip
        """
        self.assertTrue(self.quick_bet.bet_receipt.name is not None,
                        msg='Selection name not displayed')
        self.assertTrue(self.quick_bet.bet_receipt.event_market_name is not None,
                        msg='Market name not displayed')
        self.assertTrue(self.quick_bet.bet_receipt.total_stake is not None,
                        msg='Stake is not displayed')
        self.assertTrue(self.quick_bet.bet_receipt.estimate_returns is not None,
                        msg='Estimated returns is not displayed')
        self.assertTrue(self.quick_bet.bet_receipt.odds is not None,
                        msg='Odds is not displayed')
        self.assertTrue(self.quick_bet.bet_receipt.event_name is not None,
                        msg='event name is not displayed')
        self.assertTrue(self.quick_bet.bet_receipt.bet_id is not None,
                        msg='Bet id is not displayed')

    def test_010__check_cashout_icon_on_the_quick_betslip_receipt(self):
        """
        DESCRIPTION: -Check Cashout icon on the Quick betslip receipt
        EXPECTED: Cash out icon is displayed in betslip
        """
        self.assertTrue(self.quick_bet.bet_receipt.has_cashout_label, msg='"Cashout" label not displayed')

    def test_011__check_date(self):
        """
        DESCRIPTION: -Check Date
        EXPECTED: Date is displayed
        """
        self.assertTrue(self.quick_bet.bet_receipt.header.receipt_datetime is not None,
                        msg='Date is not displayed')

    def test_012__check_event_name_selection_pricemarket_name(self):
        """
        DESCRIPTION: -Check event name, selection price,market name.
        EXPECTED: Event name, market name and price displayed on Quick bet slip
        """
        # This test step is covered in step 8

    def test_013__check_potential_returns(self):
        """
        DESCRIPTION: -Check potential returns
        EXPECTED: Potential/Estimated returns calculated correct
        """
        num, denom = self.quick_bet.bet_receipt.odds.split('/')
        odds_price = float(num) / float(denom)
        expected_estimated_price = round(self.bet_amount + (odds_price * self.bet_amount), 2)
        actual_estimated_price = round(float(self.quick_bet.bet_receipt.estimate_returns), 2)
        self.assertAlmostEqual(expected_estimated_price, actual_estimated_price, delta=0.04,
                               msg=f'expected price:"{expected_estimated_price}" not same as actual:"{actual_estimated_price}"')

    def test_014__check_bet_receipt_display_of_selection_name_market_name_stake_odds_est_returns_and_receipt_number(self):
        """
        DESCRIPTION: -Check bet receipt display of Selection name, market name, stake, Odds, Est. Returns and receipt number
        EXPECTED: Selection name, market name, stake, Odds, Est. Returns and receipt  are displayed on betslip
        """
        # This test step is covered in step 8

    def test_015__check_header_balance_update_after_placing_bet(self):
        """
        DESCRIPTION: -Check header balance update after placing bet
        EXPECTED: Balance updated
        """
        betplaced_balance = self.site.header.user_balance
        self.assertGreater(self.user_balance, betplaced_balance, msg='Balance not updated successfully')

    def test_016_check_bets_are_displaying_in_my_bets_open_bets_and_settle_bets(self):
        """
        DESCRIPTION: Check bets are displaying in my bets open bets and settle bets
        EXPECTED: Bets are displayed in Openbets and settle bets
        """
        self.quick_bet.header.close_button.click()
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets, msg='Bets not present in "OPEN BETS"')
        self.site.open_my_bets_settled_bets()
        self.site.wait_content_state(state_name='BetHistory', timeout=10)
        settled_bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        try:
            self.assertTrue(settled_bets, msg='Bets not present in "SETTLED BETS"')
        except:
            if (len(settled_bets)) == 0:
                self._logger.info(
                    f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
