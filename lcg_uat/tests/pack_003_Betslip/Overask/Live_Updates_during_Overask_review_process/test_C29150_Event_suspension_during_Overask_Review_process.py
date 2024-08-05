import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.betslip
@vtest
class Test_C29150_Event_suspension_during_Overask_Review_process(BaseBetSlipTest):
    """
    TR_ID: C29150
    NAME: Event suspension during Overask Review process
    DESCRIPTION: This test case verifies Event suspension during Oversk Review process
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: Edited based on LCRCORE-13090: AS A Trader I NEED a way to prevent any overasked bets on suspended selections from getting accepted through TI
    """
    keep_browser_open = True
    suggested_max_bet = 1.5
    bir_delay = 30
    selection_ids = []
    event_ids = []

    def verify_trigger_offer_or_declined_bet(self, offer_trigger=True):

        if offer_trigger:
            account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                    event_id=self.event_ids[0])
            self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                           betslip_id=betslip_id, max_bet=self.suggested_max_bet, bet_status_suspended=True)
        else:
            account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                    event_id=self.event_ids[1])
            self.bet_intercept.decline_bet(event_id=self.event_ids[1], bet_id=bet_id, betslip_id=betslip_id)

        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
        bet_receipt_footer = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt_footer.done_button.is_displayed(), msg='"Done" button is not displayed')
        self.assertTrue(bet_receipt_footer.done_button.is_enabled(), msg='"Done" button is not enabled')
        actual_balance = self.site.header.user_balance
        self.assertEqual(actual_balance, self.expected_balance,
                         msg=f'"{actual_balance}" and "{self.expected_balance}" are not same')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)
        self.__class__.expected_balance = self.site.header.user_balance

    def test_001_add_selection_to_the_betslip(self, sel_id=None):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        if not sel_id:
            sel_id = self.selection_ids[0]
        self.open_betslip_with_selections(selection_ids=sel_id)

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        self.__class__.bet_amount = self.max_bet + 1

    def test_003_clicktap_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Now' button
        EXPECTED: *   CMS configurable Title and Message for OverAsk are displayed on an overlay on white background anchored to the footer
        EXPECTED: * Mobile: Background is disabled and not clickable, Desktop/Tablet: Widget is disabled and not clickable
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: *   'maxAllowed' value is displayed in the text in '£X,XXX' format and comes from OB in 'buildBet' response while adding selection to the bet slip
        """
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_while_review_is_pending_trigger_event_suspension_for_selection_under_the_review(self, event_id=None):
        """
        DESCRIPTION: While review is pending trigger event suspension for selection under the review
        EXPECTED: Selection is suspended in the Betslip
        """
        if not event_id:
            event_id = self.event_ids[0]
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)
        self.device.refresh_page()
        self.site.open_betslip()
        sections = self.get_betslip_sections().Singles
        stake = list(sections.values())[0]
        result = wait_for_result(lambda: stake.suspended_stake_label, name='SUSPENDED label to appear',
                                 timeout=self.bir_delay)
        self.assertEqual(result.strip('"'), vec.betslip.SUSPENDED_LABEL,
                         msg=f'{vec.betslip.SUSPENDED_LABEL} does not appear Actual content "{result}"')

    def test_005_trigger_offer_for_the_selection(self):
        """
        DESCRIPTION: Trigger Offer for the selection
        EXPECTED: * Result is FAIL in the backoffice.
        EXPECTED: * Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**.
        EXPECTED: * Selection, Market and Even names are still displayed
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Continue'/'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is not reduced
        """
        self.verify_trigger_offer_or_declined_bet(offer_trigger=True)

    def test_006_clicktap_the_continuego_betting_button(self):
        """
        DESCRIPTION: Click/Tap the 'Continue'/'Go Betting' button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        self.site.bet_receipt.footer.done_button.click()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Bet Slip is not closed')

    def test_007_repeat_steps_1_4(self):
        """
        DESCRIPTION: Repeat steps 1-4
        """
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_add_selection_to_the_betslip(sel_id=self.selection_ids[1])
        self.test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection()
        self.test_003_clicktap_bet_now_button()
        self.test_004_while_review_is_pending_trigger_event_suspension_for_selection_under_the_review(event_id=self.event_ids[1])

    def test_009_trigger_bet_decline_by_trader(self):
        """
        DESCRIPTION: Trigger bet decline by Trader
        EXPECTED: * Result is FAIL in the backoffice.
        EXPECTED: * Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**.
        EXPECTED: * Selection, Market and Even names are still displayed
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Continue'/'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is not reduced
        """
        self.verify_trigger_offer_or_declined_bet(offer_trigger=False)

    def test_010_clicktap_on_continuego_betting_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue'/'Go Betting' button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        self.test_006_clicktap_the_continuego_betting_button()
