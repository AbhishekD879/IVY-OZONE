import pytest
import tests
from voltron.pages.shared import get_device
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # events cannot be settled in prod
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C60092546_Cash_Out_bets_handling_CASHOUT_BET_NO_CASHOUT_errors(BaseBetSlipTest):
    """
    TR_ID: C60092546
    NAME: Cash Out bets handling CASHOUT_BET_NO_CASHOUT errors
    DESCRIPTION: This case verifies Cash Out bets handling receiving CASHOUT_BET_NO_CASHOUT errors
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Single and Multiple bets with available cash out
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: CASHOUT_BET_NO_CASHOUT - This update can be triggered by resulting one of selection to L (Lose) and confirming it
    """
    keep_browser_open = True
    incorrect_price = '400/1'
    device_name = tests.desktop_default

    def get_cashout_bet_no_cashout_error(self, selection_name):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                if 'CASHOUT_BET_NO_CASHOUT' in entry[1]['message']['message']['params']['response']['payloadData'] and \
                        selection_name in entry[1]['message']['message']['params']['response']['payloadData']:
                    return entry[1]['message']['message']['params']['response']['payloadData']
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

    def cashout_bets_are_present(self, bet_type, eventname):
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, event_names=eventname)

        self.assertTrue(bet.buttons_panel.full_cashout_button.is_enabled(),
                        msg=f'Cash Out button is not enabled for "{bet_name}" bet')

    def triggering_no_cashout_error(self, selection_id, market_id, event_id, bet_type, eventname):
        self.ob_config.result_selection(selection_id=selection_id,
                                        market_id=market_id,
                                        event_id=event_id,
                                        result='L',
                                        wait_for_update=True)
        self.ob_config.confirm_result(selection_id=selection_id,
                                      market_id=market_id,
                                      event_id=event_id,
                                      result='L',
                                      wait_for_update=True)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_my_bets_open_bets()
        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, event_names=eventname)

        self.assertFalse(self.bet.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg=f'Cash Out button is present for "{bet_name}" bet')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place Single and Multiple bets with available cash out
        """
        # Verify CashOut tab configuration in CMS
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')

        event1 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event_name1 = event1[7]['event']['name']
        self.__class__.selection_name1, self.__class__.selection_id1 = list(event1.selection_ids.items())[0]
        self.__class__.eventID1 = event1.event_id
        self.__class__.marketID1 = event1.default_market_id
        event2 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event_name2 = event2[7]['event']['name']
        self.__class__.selection_name2, self.__class__.selection_id2 = list(event2.selection_ids.items())[0]
        self.__class__.eventID2 = event2.event_id
        self.__class__.marketID2 = event2.default_market_id
        event3 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event_name3 = event3[7]['event']['name']
        self.__class__.selection_name3, self.__class__.selection_id3 = list(event3.selection_ids.items())[0]
        self.__class__.eventID3 = event3.event_id
        self.__class__.marketID3 = event3.default_market_id
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[self.selection_id1])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_open_my_bets_pagesection__cash_out_or_open_bets_tab(self):
        """
        DESCRIPTION: Open My Bets page/section > 'Cash Out' or 'Open Bets' tab
        EXPECTED: Single and Multiple bets with available cash out are present in selected tab
        """
        self.cashout_bets_are_present(bet_type='SINGLE', eventname=self.event_name1)

    def test_002_single_bet_for_any_of_present_single_bet_events_trigger_cashout_bet_no_cashout_error_check_preconditions_observe_ui(self):
        """
        DESCRIPTION: **[Single bet]**
        DESCRIPTION: * For any of present single bet events trigger CASHOUT_BET_NO_CASHOUT error (check Preconditions)
        DESCRIPTION: * Observe UI
        EXPECTED: Cashout button is hidden from event on selected My Bets tab
        """
        self.triggering_no_cashout_error(self.selection_id1, self.marketID1, self.eventID1, bet_type='SINGLE',
                                         eventname=self.event_name1)

    def test_003__check_messages_in_current_cashout_ws_connectionindexphpattachmentsget122292771(self):
        """
        DESCRIPTION: * Check messages in current CashOut WS connection
        DESCRIPTION: ![](index.php?/attachments/get/122292771)
        EXPECTED: * betUpdate with cashoutStatus CASHOUT_BET_NO_CASHOUT is received
        """
        self.__class__.result1 = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name1)
        self.assertTrue(self.result1, msg='betUpdate with cashoutStatus CASHOUT_BET_NO_CASHOUT is not recieved')

    def test_004__send_any_cash_out_updates_for_the_selected_event_eg_price_updates_check_ui_and_current_cashout_ws_connection(self):
        """
        DESCRIPTION: * Send any Cash Out updates for the selected event (e.g. price updates)
        DESCRIPTION: * Check UI and current CashOut WS connection
        EXPECTED: * No changes on UI
        EXPECTED: * Any further updates from websocket (like cashout value updates) are ignored
        """
        self.ob_config.change_price(self.selection_id1, self.incorrect_price)
        result2 = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name1)
        self.assertEqual(self.result1, result2, msg='updates from websocket (like cashout value updates) are displayed but they should be ignored')
        self.assertFalse(self.bet.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg='Cash Out button is present for single bet')

    def test_005_repeat_steps_1_4_for_multiples_bet(self):
        """
        DESCRIPTION: Repeat steps 1-4 for **Multiples** bet
        EXPECTED: Result is the same
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id2, self.selection_id3])
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.cashout_bets_are_present(bet_type='DOUBLE', eventname=self.event_name2)
        self.triggering_no_cashout_error(self.selection_id2, self.marketID2, self.eventID2, bet_type='DOUBLE',
                                         eventname=self.event_name2)
        result1 = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name2)
        self.assertTrue(result1, msg='betUpdate with cashoutStatus CASHOUT_BET_NO_CASHOUT is not recieved')
        self.ob_config.change_price(self.selection_id2, self.incorrect_price)
        result2 = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name2)
        self.assertEqual(result1, result2,
                         msg='updates from websocket (like cashout value updates) are displayed but they should be ignored')
        self.assertFalse(self.bet.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg='Cash Out button is present for single bet')

    def test_006_coral_only_navigate_to_edp_of_the_event_with_available_placed_bet_and_cash_out_open_my_bets_tab_on_edp(self):
        """
        DESCRIPTION: **[Coral only]**
        DESCRIPTION: * Navigate to EDP of the event with available placed bet and cash out
        DESCRIPTION: * Open 'My bets' tab on EDP
        EXPECTED: * EDP My Bets tab is displayed with placed bets including this event
        EXPECTED: * Cash Out is available for any present bet
        """
        if self.brand == 'bma':
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=[self.selection_id3])
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.close_button.click()
            self.navigate_to_edp(event_id=self.eventID3)
            self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)
            bet_name, bet = self.site.sport_event_details.my_bets.accordions_list.get_bet(
                bet_type='SINGLE', event_names=self.selection_name3)
            self.assertTrue(bet.buttons_panel.full_cashout_button.is_enabled(),
                            msg=f'Cash Out button is not enabled for "{bet_name}" bet in EDP my bets page')
            self.ob_config.result_selection(selection_id=self.selection_id3,
                                            market_id=self.marketID3,
                                            event_id=self.eventID3,
                                            result='L',
                                            wait_for_update=True)
            self.ob_config.confirm_result(selection_id=self.selection_id3,
                                          market_id=self.marketID3,
                                          event_id=self.eventID3,
                                          result='L',
                                          wait_for_update=True)
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)
            bet_name, bet = self.site.sport_event_details.my_bets.accordions_list.get_bet(
                bet_type='SINGLE', event_names=self.selection_name3)

            self.assertFalse(bet.buttons_panel.has_full_cashout_button(expected_result=False),
                             msg=f'Cash Out button is present for "{bet_name}" bet in EDP my bets page')
            result1 = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name3)
            self.assertTrue(result1, msg='betUpdate with cashoutStatus CASHOUT_BET_NO_CASHOUT is not recieved')
            self.ob_config.change_price(self.selection_id3, self.incorrect_price)
            result2 = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name3)
            self.assertEqual(result1, result2,
                             msg='updates from websocket (like cashout value updates) are displayed but they should be ignored')
            self.assertFalse(bet.buttons_panel.has_full_cashout_button(expected_result=False),
                             msg='Cash Out button is present for single bet in EDP My bets page')

    def test_007_repeat_steps_1_4_for_my_bets_edp_page(self):
        """
        DESCRIPTION: Repeat steps 1-4 for **My Bets (EDP)** page
        EXPECTED: Result is the same
        """
        # covered in step 6
