from time import sleep

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot change selection results on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.timeout(720)
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C2292553_Open_won_void_cashed_out_bet_statuses_on_Open_BetsSettled_Bets(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C2292553
    NAME: Open/won/void/cashed out bet statuses on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies showing the bet statuses
    """
    keep_browser_open = True
    number_of_events = 5
    bet_amount = 0.3

    def update_selection_result(self, selections_ids: dict, market_id: str, event_id: str):
        """
        Update selections results with Won/Void/Lose and Settle statuses
        :param selections_ids: specifies selections and results
        :param market_id: specifies market
        :param event_id: specifies event
        """
        for key, value in selections_ids.items():
            self.ob_config.update_selection_result(selection_id=key,
                                                   market_id=market_id,
                                                   event_id=event_id,
                                                   result=value)

    def place_bet(self, selections_ids: list, multiple=False):
        """
        Place and validate bet
        :param selections_ids: specifies selections
        :param multiple: flag if need to place multiple bet
        """
        self.open_betslip_with_selections(selection_ids=selections_ids)
        if multiple:
            self.place_multiple_bet()
        else:
            self.place_single_bet()
        self.site.bet_receipt.footer.click_done()
        self.__class__.expected_betslip_counter_value = 0

    def verify_bet_status(self, selection: str, bet_status: str):
        """
        Verify bet has appropriate status
        :param selection: selection of Bet.
        :param bet_status: expected bet status
        """
        selections = self.verify_selections_displayed(selections=[selection], tab=self.site.bet_history)
        self.assertEqual(selections[selection].icon.status, bet_status,
                         msg=f'Bet with selection {selections[selection]} does not have "{bet_status}" status')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Create test events
        DESCRIPTION: 2. Login with User1
        EXPECTED: 3. User1 has placed Single Bets, where
        EXPECTED: - **Bet1** with **'WON'** result
        EXPECTED: - **Bet2** with **'VOID'** result
        EXPECTED: - **Bet3** with **'LOSE'** result
        EXPECTED: 4. User1 has placed Multiple Bets, where
        EXPECTED: - **Bet4** has 1 selection with **'WON'** result
        EXPECTED: - **Bet5** has 1 selection with **'VOID'** result
        EXPECTED: - **Bet6** has 1 selection with **'LOSE'** result
        """
        events_info = self.create_several_autotest_premier_league_football_events(
            number_of_events=self.number_of_events)

        event_1 = events_info[0]
        event_2 = events_info[1]
        event_3 = events_info[2]
        event_4 = events_info[3]
        event_5 = events_info[4]

        self.__class__.event2_name = f'{event_2.event_name} {"FT"}'

        self.__class__.selection_1 = list(event_1.selection_ids.items())[0]
        self.__class__.selection_2 = list(event_1.selection_ids.items())[1]
        self.__class__.selection_3 = list(event_2.selection_ids.items())[0]
        self.__class__.selection_4 = list(event_2.selection_ids.items())[1]
        self.__class__.selection_5 = list(event_3.selection_ids.items())[0]
        self.__class__.selection_6 = list(event_3.selection_ids.items())[1]
        self.__class__.selection_7 = list(event_4.selection_ids.items())[0]
        self.__class__.selection_8 = list(event_4.selection_ids.items())[1]
        self.__class__.selection_9 = list(event_5.selection_ids.items())[0]

        username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=username, amount=tests.settings.min_deposit_amount)
        self.site.login(username=username)

        self.place_bet(selections_ids=[self.selection_1[1], self.selection_2[1], self.selection_3[1]])
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.update_selection_result(selections_ids={self.selection_1[1]: 'W', self.selection_2[1]: 'V'},
                                     market_id=self.ob_config.market_ids[event_1.event_id][market_short_name],
                                     event_id=event_1.event_id)

        self.update_selection_result({self.selection_3[1]: 'L'},
                                     self.ob_config.market_ids[event_2.event_id][market_short_name],
                                     event_2.event_id)

        self.place_bet([self.selection_4[1], self.selection_7[1]], multiple=True)
        self.place_bet([self.selection_5[1], self.selection_8[1]], multiple=True)
        self.place_bet([self.selection_6[1], self.selection_9[1]], multiple=True)

        self.update_selection_result(selections_ids={self.selection_4[1]: 'W'},
                                     market_id=self.ob_config.market_ids[event_2.event_id][market_short_name],
                                     event_id=event_2.event_id)
        self.update_selection_result(selections_ids={self.selection_5[1]: 'V'},
                                     market_id=self.ob_config.market_ids[event_3.event_id][market_short_name],
                                     event_id=event_3.event_id)
        self.update_selection_result(selections_ids={self.selection_6[1]: 'L'},
                                     market_id=self.ob_config.market_ids[event_3.event_id][market_short_name],
                                     event_id=event_3.event_id)

    def test_001_verify_single_and_multiple_bets_with_won_result_and_verify_that_appropriate_statuses_are_shown_for_other_multiple_bets(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets tab
        DESCRIPTION: Verify that Single Bets and multiple bet with 'WON' result are NOT shown (it is already Settled)
        DESCRIPTION: Verify that appropriate statuses are shown for other multiple bets
        EXPECTED: - Single bets: **Bet1, Bet2, Bet3** are NOT shown
        EXPECTED: - Multiple bet:
        EXPECTED: - 'green tick' icon is shown for one of selection in **Bet4** on the left of selection
        EXPECTED: - 'VOID' label is shown for one of selection in **Bet5** on the left of selection
        EXPECTED: - **Bet6** is NOT shown
        """
        self.site.open_my_bets_open_bets()
        settled_bets = self.verify_selections_displayed(
            selections=[self.selection_1[0], self.selection_2[0], self.selection_3[0], self.selection_6[0]],
            tab=self.site.open_bets, expected_result=False)
        self.assertFalse(settled_bets,
                         msg=f'Single Bets and multiple bet with "LOSE" result are shown: "{settled_bets}"')
        # wait some time for results to appear on page
        sleep(20)

        active_bets = self.verify_selections_displayed(selections=[self.selection_4[0], self.selection_5[0]],
                                                       tab=self.site.open_bets)

        self.assertEqual(len(active_bets), 2, msg='Multiple bet with "WON" and "VOID" results are not shown')

        result = wait_for_result(lambda: active_bets[self.selection_4[0]].icon.status == vec.betslip.WON_STAKE.lower(),
                                 timeout=10,
                                 name='Wait for bet status to be "Won"',
                                 bypass_exceptions=(KeyError, IndexError, AttributeError, VoltronException))
        self.assertTrue(result, msg=f'Actual status for multiple bet "{self.selection_4[0]}" is not "Won", it is: '
                                    f'"{active_bets[self.selection_4[0]].icon.status}"')

        result = wait_for_result(lambda: active_bets[self.selection_5[0]].icon.status == vec.betslip.CANCELLED_STAKE.lower(),
                                 timeout=10,
                                 name='Wait for bet status to be "Void"',
                                 bypass_exceptions=(KeyError, IndexError, AttributeError, VoltronException))
        self.assertTrue(result, msg=f'Actual status for multiple bet "{self.selection_5[0]}" is not "Void", it is: '
                                    f'"{active_bets[self.selection_5[0]].icon.status}"')

    def test_002_make_full_cash_out_for_bet4_verify_that_after_successful_full_cash_out_bet4_disappeared_from_open_bets_tab(self):
        """
        DESCRIPTION: Make full cash out for **Bet4**
        DESCRIPTION: Verify that after successful full cash out **Bet4** disappeared from Open Bets tab
        EXPECTED: **Bet4** disappeared from Open Bets tab
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event2_name, number_of_bets=9)
        self.assertTrue(bet, msg=f'Bet for "{self.selection_4[0]}"" and "{self.selection_7[0]}" is not shown')
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(), msg='Full Cash Out button is not present')
        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS),
                        msg=f'Message "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()

        result = self.site.cashout.tab_content.accordions_list.wait_till_bet_disappear(bet_name)
        self.assertTrue(result, msg=f'Bet: "{bet_name}" is still displayed after reloading the page')

    def test_003_navigate_to_my_bets_settled_bets_verify_that_all_settled_bets_are_shown_with_appropriate_statuses(self):
        """
        DESCRIPTION: Navigate to My Bets>Settled Bets
        DESCRIPTION: Verify that all settled bets are shown with appropriate statuses
        EXPECTED: - **Bet1** is shown with "green tick' icon on the left of selection and 'WON' label in the header
        EXPECTED: - **Bet2** is shown with "VOID' label on the left of selection
        EXPECTED: - **Bet3** is shown with "red cross' icon on the left of selection and 'LOST' label in  the header
        EXPECTED: - **Bet6** is shown with "red cross' icon on the left of the selection and 'LOST' label in the header
        EXPECTED: - **Bet4** is shown with "CASHED OUT' label in the header
        """
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        self.verify_bet_status(self.selection_1[0], vec.betslip.WON_STAKE.lower())
        self.verify_bet_status(self.selection_2[0], vec.betslip.CANCELLED_STAKE.lower())
        self.verify_bet_status(self.selection_3[0], vec.betslip.LOST_STAKE.lower())
        self.verify_bet_status(self.selection_6[0], vec.betslip.LOST_STAKE.lower())

        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event2_name, number_of_bets=9)

        actual_status = bet.bet_status
        expected_status = vec.betslip.CASHOUT_STAKE
        self.assertEquals(actual_status, expected_status,
                          msg=f'Actual bet status: "{actual_status}" is not equal to expected: "{expected_status}"')
