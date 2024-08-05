import pytest
import time
import voltron.environments.constants as vec
from fractions import Fraction
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod      As bet needs to be settled, cannot script on prod
@pytest.mark.hl
@pytest.mark.acca
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870248_Verify_user_can_edit_ACCA_bets_when_prices_update_to_open_selections_price_increase_Decrease_click_Confirm_button_when_there_is_price_update__Check_that_the_new_potential_returns_on_my_acca_page_and_my_bets_Verify_Edit_My_Acca_button_no_longe(BaseBetSlipTest):
    """
    TR_ID: C44870248
    NAME: "Verify user can edit ACCA bets when prices update to open selections (price increase/Decrease , click Confirm button when there is price update) - Check that the new potential returns on my acca page and my bets.  Verify Edit My Acca button no longe
    DESCRIPTION: "Verify user can edit ACCA bets when prices update to open selections (price increase/Decrease , click Confirm button when there is price update)
    DESCRIPTION: - Check that the new potential returns on my acca page and my bets.
    DESCRIPTION: Verify Edit My Acca button no longer displayed as only one selection remains open
    DESCRIPTION: Verify Display of the Edit My Acca button when any selection is suspended"
    """
    keep_browser_open = True
    event_names = []
    eventIDs = []
    marketIDs = []
    selectionIDs = []
    new_price_selection = '3/2'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have 4 or 5+ accumulator bets.
        """
        for i in range(0, 4):
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.event_names.append(event.team1)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
            market_short_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
            self.marketIDs.append(self.ob_config.market_ids[event.event_id][market_short_name])
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)

    def test_001_verify_user_can_edit_acca_bets_when_prices_update_to_open_selections_price_increasedecrease_click_confirm_button_when_there_is_price_update(self):
        """
        DESCRIPTION: Verify user can edit ACCA bets when prices update to open selections (price increase/Decrease, click Confirm button when there is price update)
        EXPECTED: Users should still be able to edit ACCA bets when prices update to open selections (price increase/Decrease, click Confirm button when there is price update)
        """
        self.ob_config.change_price(selection_id=self.selectionIDs[0], price=self.new_price_selection)
        # TODO: raised bug for ladbrokes for price updation issue
        if self.brand == 'bma':
            price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selectionIDs[0],
                                                                     price=self.new_price_selection)
            self.assertTrue(price_update,
                            msg=f'Price update for selection "{self.event_names[0]}" with id "{self.selectionIDs[0]}" is not received')
            actual_error_betslip_msg = self.get_betslip_content().wait_for_warning_message()
            self.assertEqual(actual_error_betslip_msg, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                             msg=f'Actual BetSlip error message "{actual_error_betslip_msg}" not same as '
                                 f'Expected "{vec.betslip.PRICE_CHANGE_BANNER_MSG}" ')
        else:  # TODO BMA-55571
            self.device.refresh_page()
            self.site.open_betslip()
        self.place_multiple_bet(number_of_stakes=1)
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_my_bets_open_bets()
        bet_before_EMA = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(bet_before_EMA, msg="cannot find any bets in open bets")
        bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        selection = list(bet_before_EMA.items_as_ordered_dict.values())[0]
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_remove_icon.is_displayed(), timeout=3),
                        msg='"Remove icon" not displayed')
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg='"undo button" not displayed')
        confirm_button = bet_before_EMA.confirm_button.name
        self.assertEqual(confirm_button, vec.ema.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{confirm_button}" is not same as Expected text:"{vec.ema.CONFIRM_EDIT.upper()}".')
        bet_before_EMA.confirm_button.click()
        self.__class__.bet_after_EMA = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bet_after_EMA, msg="cannot find any bets in open bets")
        EMA_success_msg = self.bet_after_EMA.cash_out_successful_message
        self.assertEqual(EMA_success_msg, vec.ema.EDIT_SUCCESS.caption,
                         msg=f'Message "{EMA_success_msg}" is not the same as expected "{vec.ema.EDIT_SUCCESS.caption}"')

    def test_002_after_you_have_edited_an_acca_check_that_the_correct_new_potential_returns_are_shown_for_that_acca_in_my_bets_open_bets(self):
        """
        DESCRIPTION: After you have edited an ACCA, check that the correct New Potential Returns are shown for that ACCA in My Bets->Open Bets
        EXPECTED: You should see correct New Potential Returns for your ACCA in My Bets->Open Bets
        """
        selections = self.bet_after_EMA.items_as_ordered_dict.values()
        self.assertTrue(selections, msg="cannot find any selections")
        odd_values = []
        for selection in selections:
            odd = selection.odds_value
            odd_values.append(float(Fraction(odd)))
        stake = float(self.bet_after_EMA.stake.stake_value)
        expected_potential_ret_after_EMA = round((stake * (odd_values[0] + 1) * (odd_values[1] + 1) * (odd_values[2] + 1)), 1)
        potential_ret_after_EMA = round((float(self.bet_after_EMA.est_returns.value.replace('£', '').replace('$', '').replace('€', ''))), 1)
        self.assertEqual(potential_ret_after_EMA, expected_potential_ret_after_EMA,
                         msg=f'Actual potential returns "{potential_ret_after_EMA}" are not same as Expected potential returns "{expected_potential_ret_after_EMA}"')

    def test_003_when_all_but_one_selection_in_an_acca_has_not_resulted_in_a_win_verify_that_the_edit_my_acca_button_is_not_seen(self):
        """
        DESCRIPTION: When all but one selection in an ACCA has not resulted in a win, verify that the Edit My ACCA button is not seen
        EXPECTED: When all but one selection in an ACCA has not resulted in a win, the Edit My ACCA button should not be seen
        """
        selection_ids = [self.selectionIDs[1], self.selectionIDs[2]]
        market_ids = [self.marketIDs[1], self.marketIDs[2]]
        event_ids = [self.eventIDs[1], self.eventIDs[2]]
        for i in range(len(selection_ids)):
            self.ob_config.update_selection_result(selection_id=selection_ids[i], market_id=market_ids[i],
                                                   event_id=event_ids[i])
        time.sleep(5)
        self.device.refresh_page()
        if self.device_type == 'desktop':
            self.site.wait_splash_to_hide()
            self.site.open_my_bets_open_bets()
        bet_after_two_settles = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(bet_after_two_settles, msg="cannot find any bets in open bets")
        new_selections = bet_after_two_settles.items_as_ordered_dict.values()
        bet_leg_status = [list(new_selections)[0], list(new_selections)[1]]
        for bet in bet_leg_status:
            self.assertTrue(wait_for_result(lambda: bet.icon.is_displayed(), timeout=10),
                            msg=f'"symbol for win status" is not displayed')
        self.assertFalse(bet_after_two_settles.has_edit_my_acca_button(expected_result=False),
                         msg=f'"{vec.ema.EDIT_MY_BET}" is still shown for this Acca edited bet which has '
                             f'won two of its selections')
