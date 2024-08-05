import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C59898510_Bet_more_than_balance_Quick_Deposit__Quick_Deposit_should_open_and_then_after_you_add_funds_the_bet_should_go_to_the_OA_flow(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C59898510
    NAME: Bet more than balance (Quick Deposit) - Quick Deposit should open and then after you add funds, the bet should go to the OA flow
    PRECONDITIONS: You have Quick Deposit enabled for your user i.e. you have a card attached
    """
    keep_browser_open = True
    max_bet = 2
    prices = {0: '1/12', 1: '1/2', 2: '1/3'}

    def test_001_add_a_selection_to_quick_betbet_slip_and_add_a_stake_that_is_greater_than_that_selections_max_stake_and_is_greater_than_your_balance(self):
        """
        DESCRIPTION: Add a selection to Quick Bet/Bet Slip and add a stake that is greater than that selection's max stake and is greater than your balance.
        EXPECTED: You should have added stake greater than the selection's max stake and your balance.
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount,
                                  card_number=tests.settings.visa_card)
        self.site.login(username=self.username)
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet, lp_prices=self.prices)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.eventID, selection_id = event_params.event_id, list(event_params.selection_ids.values())[0]
        balance = self.site.header.user_balance
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.__class__.bet_amount = balance + 1 if balance > self.max_bet else self.max_mult_bet + 1

        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = self.bet_amount

    def test_002_verify_that_you_see_the_message_please_deposit_a_min_of_and_that_you_see_a_make_a_deposit_button(self):
        """
        DESCRIPTION: Verify that you see the message "Please deposit a min of..." and that you see a Make A Deposit button.
        EXPECTED: You should see the message and the Make A Deposit button
        """
        expected_message_text = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Info panel message: "{actual_message_text}" '
                             f'is not as expected: "{expected_message_text}"')

        self.__class__.deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(self.deposit_button.is_enabled(), msg=f'"{self.deposit_button.name}" button is not enabled')
        self.assertEqual(self.deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{self.deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_003_click_on_make_a_deposit_add_an_amount_that_will_allow_you_to_place_the_bet_and_then_click_on_deposit__place_bet(self):
        """
        DESCRIPTION: Click on Make A Deposit, add an amount that will allow you to place the bet and then click on Deposit & Place Bet.
        EXPECTED: You should have clicked on Make A Deposit, added an amount to cover the bet and clicked on Deposit & Place Bet
        """
        self.deposit_button.click()
        self.site.wait_splash_to_hide(5)
        quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        quick_deposit.plus_button.click()
        quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            keyboard = quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.visa_card_cvv)
        else:
            quick_deposit.cvv_2.input.value = tests.settings.visa_card_cvv
        quick_deposit.deposit_and_place_bet_button.click()

    def test_004_verify_that_you_are_taken_to_the_overask_flow(self):
        """
        DESCRIPTION: Verify that you are taken to the Overask flow.
        EXPECTED: You should be taken to the Overask flow.
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_005_accept_the_bet_and_verify_the_bet_receipt_is_correct_and_that_the_bet_shows_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Accept the bet and verify the bet receipt is correct and that the bet shows in My Bets->Open Bets
        EXPECTED: The bet receipt should be correct and My Bets->Open Bets should correctly show the bet.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.check_bet_receipt_is_displayed(timeout=20)
        receipt_bet_type_section = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict.get(vec.betslip.SINGLE)
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='No bets found in BetReceipt')
        bet_info = list(section_items.values())[0]
        self.assertEqual(bet_info.type_name.name, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE.title(),
                         msg=f'Actual Bet type: "{bet_info.type_name.name}" is not same as Expected Bet type: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE.title()}"')
        self.assertEqual(bet_info.event_name, self.event_name,
                         msg=f'Actual Event name: "{bet_info.event_name}" is not same as Expected Event name: "{self.event_name}"')
        self.site.bet_receipt.footer.done_button.click()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
