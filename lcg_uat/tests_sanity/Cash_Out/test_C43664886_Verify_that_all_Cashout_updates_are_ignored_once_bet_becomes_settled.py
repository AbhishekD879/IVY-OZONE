import pytest
import voltron.environments.constants as vec
from voltron.pages.shared import get_device
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Need to settle selection/markets from OB
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.bet_placement
@pytest.mark.desktop
@vtest
class Test_C43664886_Verify_that_all_Cashout_updates_are_ignored_once_bet_becomes_settled(BaseBetSlipTest):
    """
    TR_ID: C43664886
    NAME: Verify that all Cashout updates are ignored once bet becomes settled
    DESCRIPTION: This test case verified that there are no updates in Cashout EventStream (cashout V4) when bet becomes settled
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WS connection to Cashout MS is created when user lands on myBets page
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User have at least one open bet (Single / Multiple)
    PRECONDITIONS: - Cashout isV4Enabled = true in system-configuration/structure
    PRECONDITIONS: NB! CMS config will be removed when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    PRECONDITIONS: [1]:https://jira.egalacoral.com/browse/BMA-55051
    """
    keep_browser_open = True
    number_of_events = 2

    def check_cashout_MS_entries(self, pattern, selection_name):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                if pattern in entry[1]['message']['message']['params']['response']['payloadData'] and \
                        selection_name in entry[1]['message']['message']['params']['response']['payloadData']:
                    return entry[1]['message']['message']['params']['response']['payloadData']
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

    def get_cashout_bet_market(self, market_name):
        logs = get_device().get_performance_log()
        cashout_count = 0
        for entry in logs[::-1]:
            try:
                if 'CASHOUT' in entry[1]['message']['message']['params']['response']['payloadData'] and \
                        market_name in entry[1]['message']['message']['params']['response']['payloadData']:
                    cashout_count = cashout_count + 1
            except (KeyError, IndexError, AttributeError):
                continue
        return cashout_count

    def triggering_no_cashout_error(self, selection_id, market_id, event_id, bet_type, eventname, selection_name):
        self.ob_config.result_selection(selection_id=selection_id,
                                        market_id=market_id,
                                        event_id=event_id,
                                        result='L',
                                        wait_for_update=True)
        for bet_leg_name, bet_leg in self.bet.items_as_ordered_dict.items():
            if bet_leg_name == selection_name:
                actual_status = bet_leg.icon.status
                self.assertEqual(actual_status, "SUSP",
                                 msg=f'Selection: "{self.bet_name}" current status is: '
                                 f'"{actual_status}", expected: "SUSP"')
            else:
                continue
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, event_names=eventname)
        self.assertFalse(bet.buttons_panel.cashout_button.is_enabled(expected_result=False),
                         msg=f'Cash Out button is enabled for "{bet_name}" bet')
        cashout_suspended = bet.buttons_panel.cashout_button.label
        self.assertEqual(cashout_suspended, vec.bet_history.CASHOUT_BET.cash_out_bet_suspended,
                         msg=f'Actual message: "{cashout_suspended}", is not the same '
                             f'as expected: "{vec.bet_history.CASHOUT_BET.cash_out_bet_suspended}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login
        DESCRIPTION: * Place Single and multiple bet on any Pre-Match or In-Play events that have Cashout option
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
        self.__class__.selection_id3 = list(event3.selection_ids.values())[0]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[self.selection_id1])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001___navigate_to_open_bets__in_devtools_open_cashout_eventstream_requestfrom_release_xxxxxin_devtools_open_websocket_connection_to_cashout_ms(self):
        """
        DESCRIPTION: - Navigate to Open Bets
        DESCRIPTION: - In Devtools open Cashout EventStream request
        DESCRIPTION: **From release XXX.XX:**
        DESCRIPTION: In Devtools open Websocket connection to Cashout MS
        EXPECTED: - Open Bets are displayed
        EXPECTED: - In Cashout EventStream within "initial" type we received Data for open bet (selection) from preconditions
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WebSocket connection to Cashout MS is created
        EXPECTED: * Within "initial" type we received Data for open bet (selection) from preconditions
        """
        self.site.open_my_bets_open_bets()
        wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        result = self.check_cashout_MS_entries(pattern='cashout', selection_name=self.selection_id1)
        self.assertTrue(result, msg='Cashout MS data not available in WS')

    def test_002_in_ti_settle_marketselections_on_which_you_have_placed_bet(self):
        """
        DESCRIPTION: In TI settle market(selections) on which you have placed bet
        EXPECTED: - Bet is settled (Win/Lose icon appeared)
        EXPECTED: - betUpdate is received from Cashout MS
        """
        self.__class__.bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name1)
        self.triggering_no_cashout_error(self.selection_id1, self.marketID1, self.eventID1, bet_type='SINGLE',
                                         eventname=self.event_name1, selection_name=self.selection_name1)
        result = self.check_cashout_MS_entries(pattern='CASHOUT_SELN_SUSPENDED', selection_name=self.selection_name1)
        self.assertTrue(result, msg='Cashout Suspension MS data not available in WS')

    def test_003_in_ti_make_updates_pricestatusdisplay_changes_on_settled_marketeventselection_levels(self):
        """
        DESCRIPTION: In TI make updates (price/status/display changes) on settled market/event/selection levels
        EXPECTED: No updates are received from Cashout MS
        """
        before_mrkt_suspension = self.get_cashout_bet_market(market_name='Match Result')
        self.ob_config.change_market_state(event_id=self.eventID1, market_id=self.marketID1, displayed=True)
        after_mrkt_suspension = self.get_cashout_bet_market(market_name='Match Result')
        self.assertEqual(before_mrkt_suspension, after_mrkt_suspension,
                         msg=f'Cashout entries before market suspension {before_mrkt_suspension}'
                             f'is not same as after suspension {after_mrkt_suspension}')

    def test_004_repeat_steps_1_3_for_multiple_bet_where_at_least_1_legselection_is_lost(self):
        """
        DESCRIPTION: Repeat steps 1-3 for Multiple bet where at least 1 leg(selection) is lost
        EXPECTED: No updates are received from Cashout MS
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id2, self.selection_id3])
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.__class__.bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=self.event_name2)
        self.triggering_no_cashout_error(self.selection_id2, self.marketID2, self.eventID2, bet_type='DOUBLE',
                                         eventname=self.event_name2, selection_name=self.selection_name2)
        result = self.check_cashout_MS_entries(pattern='CASHOUT_SELN_SUSPENDED', selection_name=self.selection_name2)
        self.assertTrue(result, msg='Cashout Suspension MS data not available in WS')

        before_mrkt_suspension = self.get_cashout_bet_market(market_name='Match Result')
        self.ob_config.change_market_state(event_id=self.eventID2, market_id=self.marketID2, displayed=True)
        after_mrkt_suspension = self.get_cashout_bet_market(market_name='Match Result')
        self.assertEqual(before_mrkt_suspension, after_mrkt_suspension,
                         msg=f'Cashout entries before market suspension {before_mrkt_suspension}'
                             f'is not same as after suspension {after_mrkt_suspension}')
