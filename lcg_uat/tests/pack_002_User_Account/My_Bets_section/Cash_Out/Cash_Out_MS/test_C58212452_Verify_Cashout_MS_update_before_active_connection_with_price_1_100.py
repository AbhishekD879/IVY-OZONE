import pytest
import voltron.environments.constants as vec
from time import sleep
from voltron.pages.shared import get_device
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # events cannot be suspended in prod
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C58212452_Verify_Cashout_MS_update_before_active_connection_with_price_1_100(BaseBetSlipTest):
    """
    TR_ID: C58212452
    NAME: Verify Cashout MS update before active connection with price > 1/100
    DESCRIPTION: This test case verifies the updates in Cashout MS when event becomes suspended before user navigates to 'My Bets' tab and when the price/s of selection is > 1/100
    PRECONDITIONS: Story related: https://jira.egalacoral.com/browse/BMA-51061
    PRECONDITIONS: https://jira.egalacoral.com/browse/BMA-51067
    PRECONDITIONS: Epic related: https://jira.egalacoral.com/browse/BMA-51056
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: In CMS: System Config: Structure: CashOut: Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In app:
    PRECONDITIONS: - Login
    PRECONDITIONS: - Place few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: - Navigate to any page in the app except 'Cashout/Open Bets' tab
    PRECONDITIONS: - Open Dev Tools -> Network tab -> XHR filter (bet-details request) for checking cashout MS once on 'Cashout/Open Bets' tab
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Price odds of the bet are > 1/100 (eg. 1/2)
    PRECONDITIONS: - Bet/s is active/not resulted
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True
    cashout_update_status = False
    bet_update_status = False
    correct_price = '1/4'

    def get_cashout_bet_sel_susp_cashout_error(self, selection_name):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                payload = entry[1]['message']['message']['params']['response']['payloadData']
                if 'CASHOUT_SELN_SUSPENDED' in payload and \
                        selection_name in payload and 'initial' in payload:
                    return payload.split('42/0,')[0]
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

    def cashout_bet_update_status(self, bet_id, bet_type, eventname):

        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                payload = entry[1]['message']['message']['params']['response']['payloadData']
                if bet_id in payload and 'cashoutUpdate' in payload:
                    self.__class__.cashout_update_status = True
                if bet_id in payload and 'betUpdate' in payload:
                    self.__class__.bet_update_status = True
            except (KeyError, IndexError, AttributeError):
                continue
        self.assertTrue(self.cashout_update_status,
                        msg=f'Cashout MS didnt send cashoutUpdate message for the bet')
        self.assertTrue(self.bet_update_status,
                        msg=f'Cashout MS didnt send betUpdate message for the bet')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_my_bets_open_bets()
        self.__class__.bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, event_names=eventname)

    def navigate_and_check_updates_in_cashout(self, bet_type, eventname, selection_name):

        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=bet_type, event_names=eventname)
        self.assertFalse(bet.buttons_panel.cashout_button.is_enabled(expected_result=False),
                         msg=f'Cash Out button is enabled for "{bet_name}" bet')
        cashout_suspended = bet.buttons_panel.cashout_button.label
        self.assertEqual(cashout_suspended, vec.bet_history.CASHOUT_BET.cash_out_bet_suspended,
                         msg=f'Actual message: "{cashout_suspended}", is not the same '
                             f'as expected: "{vec.bet_history.CASHOUT_BET.cash_out_bet_suspended}"')
        for bet_leg_name, bet_leg in bet.items_as_ordered_dict.items():
            if bet_leg_name == selection_name:
                actual_status = bet_leg.icon.status
                self.assertEqual(actual_status, "SUSP",
                                 msg=f'Selection: "{bet_name}" current status is: '
                                     f'"{actual_status}", expected: "SUSP"')
            else:
                continue

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
        self.__class__.selection_name1, selection_id1 = list(event1.selection_ids.items())[0]
        self.__class__.eventID1 = event1.event_id
        event2 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event_name2 = event2[7]['event']['name']
        self.__class__.selection_name2, self.__class__.selection_id2 = list(event2.selection_ids.items())[0]
        self.__class__.eventID2 = event2.event_id
        event3 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.selection_id3 = list(event3.selection_ids.values())[0]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[selection_id1])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.ob_config.change_price(selection_id1, self.correct_price)

    def test_001_in_ti_suspend_the_event_on_any_level_eventmarketselectionnote_user_is_on_home_page_meanwhile_or_any_other_except_cashoutopen_bets_tab(self):
        """
        DESCRIPTION: In TI suspend the event on any level (event/market/selection)
        DESCRIPTION: Note: user is on Home page meanwhile or any other except 'Cashout/Open Bets' tab
        """
        self.ob_config.change_event_state(event_id=self.eventID1)

    def test_002_navigate_to_cashoutopen_bets_tab_afterwards_and_check_the_updates_on_ui(self):
        """
        DESCRIPTION: Navigate to 'Cashout/Open Bets' tab afterwards and check the updates on UI
        EXPECTED: Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
        EXPECTED: - initial bets data will be returned after establishing connection
        """
        self.navigate_and_check_updates_in_cashout(bet_type='SINGLE', eventname=self.event_name1,
                                                   selection_name=self.selection_name1)
        result = self.get_cashout_bet_sel_susp_cashout_error(selection_name=self.selection_name1)
        self.__class__.bet_id = result.split("\"bets\":[{")[1].split(",")[0].replace("\"", "").split(":")[1]

    def test_003_in_ti_unsuspend_the_bet_on_the_level_suspended_before_and_meanwhile_check_the_ui_for_updated(self):
        """
        DESCRIPTION: In TI unsuspend the bet on the level suspended before and meanwhile check the UI for updated
        EXPECTED: - Bet becomes active
        EXPECTED: - In Cashout MS betUpdate: getBetDetail (full betUpdate) is received
        EXPECTED: ![](index.php?/attachments/get/100880923)
        EXPECTED: From release OX105:
        EXPECTED: * Bet becomes active
        EXPECTED: * Cashout MS will send betUpdate message
        EXPECTED: From release OX106:
        EXPECTED: * Bet becomes active
        EXPECTED: * Cashout MS will send cashoutUpdate message
        """
        self.ob_config.change_event_state(event_id=self.eventID1, displayed=True, active=True)

        sleep(5)
        self.cashout_bet_update_status(bet_id=self.bet_id, bet_type='SINGLE', eventname=self.event_name1)
        for bet_leg_name, bet_leg in self.bet.items_as_ordered_dict.items():
            if bet_leg_name == self.selection_name1:
                actual_status = bet_leg.icon.status
                self.assertNotEqual(actual_status, "SUSP",
                                    msg=f'Selection: "{self.bet_name}" current status is: '
                                    f'"{actual_status}", expected: "SUSP"')
            else:
                continue

    def test_004_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet
        EXPECTED: Results are the same as above
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id2, self.selection_id3])
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.ob_config.change_event_state(event_id=self.eventID2)
        self.navigate_and_check_updates_in_cashout(bet_type='DOUBLE', eventname=self.event_name2,
                                                   selection_name=self.selection_name2)
        result = self.get_cashout_bet_sel_susp_cashout_error(selection_name=self.selection_name2)
        self.__class__.bet_id = result.split("\"bets\":[{")[1].split(",")[0].replace("\"", "").split(":")[1]
        self.ob_config.change_event_state(event_id=self.eventID2, displayed=True, active=True)
        sleep(3)
        self.cashout_bet_update_status(bet_id=self.bet_id, bet_type='DOUBLE', eventname=self.event_name2)
        for bet_leg_name, bet_leg in self.bet.items_as_ordered_dict.items():
            if bet_leg_name == self.selection_name2:
                actual_status = bet_leg.icon.status
                self.assertNotEqual(actual_status, "SUSP",
                                    msg=f'Selection: "{self.bet_name}" current status is: '
                                        f'"{actual_status}", expected: "SUSP"')
            else:
                continue
