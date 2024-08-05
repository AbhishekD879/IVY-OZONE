import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.bet_receipt
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55996')
@vtest
class Test_C29134_Rejecting_an_automatic_Offer(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29134
    NAME: Rejecting an automatic Offer
    DESCRIPTION: This test case verifies rejecting an automatic Overask offer
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: NOTE: System always automatically declined bet during testing
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = [{0: '1/12'}, {0: '1/11'}]
    selection_ids_list = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events with bet limit
        DESCRIPTION: - User is logged in to application
        """
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices[i],
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids_list.append(list(self.selection_ids.values())[0])
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self, single=True):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        if single:
            self.__class__.bet_amount = self.max_mult_bet + 0.1
            self.place_single_bet(number_of_stakes=1)
        else:
            self.__class__.bet_amount = self.max_mult_bet + 0.1
            self.place_multiple_bet(number_of_stakes=1)

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.site.wait_content_state_changed(timeout=15)

    def test_004_wait_till_the_request_expires_without_traders_offer_for_max_bet(self, single=True):
        """
        DESCRIPTION: Wait till the Request expires without Trader's Offer for Max Bet
        EXPECTED: * Bet is not placed and a 'This bet has not been accepted by traders!' message is shown
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present
        EXPECTED: * Balance is not reduced
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        if single:
            overask_warning_message = section.declined_bet.stake_content.stake_message
        else:
            overask_warning_message = section.multiple_declined_bet.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

        self.verify_user_balance(expected_user_balance=self.user_balance)
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')

    def test_005_click_tap_continue_go_betting(self):
        """
        DESCRIPTION: Click / tap 'Continue'/ 'Go betting' (From OX 99) button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        self.site.bet_receipt.footer.done_button.click()

        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Bet Slip is not closed')
        else:
            self.assertFalse(self.get_betslip_content().wait_for_overask_panel(expected_result=False),
                             msg='Overask is still shown')
            actual_message = self.get_betslip_content().no_selections_title
            self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

            if self.brand != 'ladbrokes':
                no_selections = self.get_betslip_content().no_selections_message
                self.assertEqual(no_selections, vec.betslip.NO_SELECTIONS_MSG,
                                 msg=f'Actual body message "{no_selections}" != Expected {vec.betslip.NO_SELECTIONS_MSG}')

    def test_006_add_few_selections_and_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections and for one of them enter stake value which will trigger overask for the selection
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids_list)

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: *   No bets are placed even if these Selections did not trigger the Overask
        EXPECTED: *   All selections stay in Betslip allowing Customer to modify and resubmit it
        """
        self.test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(single=False)
        self.test_003_tap_bet_now_button()
        self.test_004_wait_till_the_request_expires_without_traders_offer_for_max_bet(single=False)
        self.test_005_click_tap_continue_go_betting()
