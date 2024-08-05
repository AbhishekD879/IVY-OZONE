import pytest
import voltron.environments.constants as vec
from voltron.pages.shared import get_device
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot result a selection in prod
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C58212491_Verify_Cashout_MS_resulted_updates_before_Active_connection(BaseBetSlipTest):
    """
    TR_ID: C58212491
    NAME: Verify Cashout MS resulted updates before Active connection
    DESCRIPTION: This test case verifies the resulted updates in Cashout MS while before connection.
    PRECONDITIONS: Story related: https://jira.egalacoral.com/browse/BMA-51068
    PRECONDITIONS: Epic related: https://jira.egalacoral.com/browse/BMA-51056
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: In CMS: System Config: Structure: CashOut: Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In app:
    PRECONDITIONS: - Login
    PRECONDITIONS: - Place few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: - Navigate to any page in the app except 'Cashout/Open Bets' tab
    PRECONDITIONS: - Open Dev Tools -> Network tab -> XHR filter (bet-details request)
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Bet/s is active/not resulted
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page/tab
    PRECONDITIONS: - No requests to BPP getBetDetails and getBetDetail should be performed on cashout page
    """
    keep_browser_open = True

    def get_cashout_bet_no_cashout_error(self, selection_name):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                if 'CASHOUT_SELN_SUSPENDED' in entry[1]['message']['message']['params']['response']['payloadData'] and \
                        selection_name in entry[1]['message']['message']['params']['response']['payloadData']:
                    return entry[1]['message']['message']['params']['response']['payloadData']
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

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
        self.__class__.selection_id3 = list(event3.selection_ids.values())[0]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[self.selection_id1])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_in_ti_result_selection_save_changesindexphpattachmentsget100880880(self):
        """
        DESCRIPTION: In TI result selection, save changes.
        DESCRIPTION: ![](index.php?/attachments/get/100880880)
        EXPECTED: Selection becomes a resulted.
        """
        self.site.open_my_bets_open_bets()
        self.__class__.bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name1)
        self.triggering_no_cashout_error(self.selection_id1, self.marketID1, self.eventID1, bet_type='SINGLE',
                                         eventname=self.event_name1, selection_name=self.selection_name1)

    def test_002_navigate_to_cashoutopen_bets_tab_afterwards_and_check_the_updates_on_ui(self):
        """
        DESCRIPTION: Navigate to 'Cashout/Open Bets' tab afterwards and check the updates on UI
        EXPECTED: - Bet is suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - In 'bet-details' EventStream appears ONLY 'Initial' call
        EXPECTED: ![](index.php?/attachments/get/100880927)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: - Bet is suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - In WebSocket connection to Cashout MS is only initial bets response
        """
        result = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name1)
        self.assertTrue(result, msg='In WebSocket connection to Cashout MS doesnot have initial bets response')

    def test_003_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet.
        EXPECTED: Results are same as above
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
        result = self.get_cashout_bet_no_cashout_error(selection_name=self.selection_name2)
        self.assertTrue(result, msg='In WebSocket connection to Cashout MS doesnot have initial bets response')
