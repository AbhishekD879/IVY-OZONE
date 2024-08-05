import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result
from random import uniform
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod do not have users with freebet tokens on prod
# @pytest.mark.hl
@pytest.mark.build_your_bet
@pytest.mark.bet_placement
@pytest.mark.banach
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C2490964_Banach_Placing_a_bet_using_free_bet(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C2490964
    VOL_ID: C9698259
    NAME: Banach Placing a bet using free bet
    DESCRIPTION: Test case verifies Banach bet placement using free bet token and Bet receipt
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: **User has added at least two combinable selections to BYB Dasboard**
    PRECONDITIONS: **On Betslip user has selected free bet without cash stake**
    """
    keep_browser_open = True
    proxy = None
    default_freebets_message = vec.sb.FREE_BETS_AVAILABLE
    currency = '£'
    freebet_value = f'{uniform(2, 3):.2f}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as user that has freebets
        DESCRIPTION: Find event with Banach markets
        DESCRIPTION: Add two combinable selections to BYB Dashboard
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market()

        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value)

        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance

        self.navigate_to_edp(event_id=self.event_id)
        # self.device.refresh_page()  # TODO w/a because of issue with loading of Banach markets for the first time EDP is opened, works after refresh
        # self.site.wait_splash_to_hide()
        # self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting,
                                            selection_index=0)
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.both_teams_to_score,
                                            selection_name='Yes')

        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        summary_block.place_bet.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(
            expected_result=False, timeout=15),
            msg='BYB Dashboard panel is still displayed, BYB Betslip is not shown')
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip is not shown')

        byb_betslip_panel = self.site.byb_betslip_panel.selection.content

        self.assertTrue(byb_betslip_panel.has_use_free_bet_link(), msg='"Use Free Bet" link is not present')
        wait_for_result(lambda: byb_betslip_panel.use_free_bet_link.is_enabled(),
                        name='"Use Free Bet" link is to be enabled', timeout=20)
        byb_betslip_panel.use_free_bet_link.click()
        self.__class__.selected_freebet_value = self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap PLACE BET button
        EXPECTED: - On UI bet receipt is displayed
        EXPECTED: - User balance is not changed
        """
        self.site.byb_betslip_panel.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=15),
                        msg='BYB Bet Receipt is not displayed')
        self.verify_user_balance(expected_user_balance=self.user_balance)

    def test_002_verify_channel_used_for_byb_bet_builder_bets(self):
        """
        DESCRIPTION: Verify channel used for BYB/Bet builder bets
        EXPECTED: Channel: "e" is present in '50011' request in 'remotebetslip' websocket
        """
        response = wait_for_result(
            lambda: self.get_web_socket_response_by_id(response_id=self.response_50011, delimiter='42'),
            name=f'WS message with code {self.response_50011} to appear',
            timeout=30,
            poll_interval=1)
        self.assertTrue(response, msg=f'Response with frame ID #{self.response_50011} not received')
        self.assertEqual(response.get('channel'), 'e',
                         msg=f'Channel: "e" is not present in "{self.response_50011}" request among "{response}"')

    def test_003_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet receipt
        EXPECTED: * Main Header: 'Bet receipt' title with 'X' button
        EXPECTED: * Sub header : Tick icon, 'Bet Placed Successfully' text, date & time stamp (in the next format: i.e. 19/09/2019, 14:57)
        EXPECTED: * Block of Bet Type Summary:
        EXPECTED: * Win Alerts Toggle (if enabled in CMS)
        EXPECTED: * bet type name: e.g Single
        EXPECTED: * price of BYB selections bet : e.g @90/1
        EXPECTED: * Bet ID:(Coral)/Receipt No:(Ladbrokes) e.g Bet ID: 0/17781521/0000041
        EXPECTED: * For each selection:
        EXPECTED: * selection name
        EXPECTED: * market
        EXPECTED: * Footer:
        EXPECTED: * 'Total stake'(Coral) / 'Stake for this bet' (Ladbrokes): Free bet with icon e.g. FB £5.00
        EXPECTED: * 'Est. returns'(Coral) / 'Potential returns' (Ladbrokes)
        """
        bet_receipt_selection = self.site.byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in Build Your Bet receipt')
        self.assertTrue(bet_receipt_content.odds, msg='Odds value not found')

        self.assertEqual(bet_receipt_content.bet_id_label, vec.betslip.BET_ID,
                         msg=f'Bet id label "{bet_receipt_content.bet_id_label}" '
                             f'is not the same as expected "{vec.betslip.BET_ID}"')
        self.assertTrue(bet_receipt_content.bet_id_value, msg='Bet ID value not found')

        self.assertEqual(bet_receipt_selection.total_est_returns_label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Total Est. Returns label "{bet_receipt_selection.total_est_returns_label}" '
                             f'is not the same as expected "{vec.bet_history.TOTAL_RETURN}"')
        self.assertIn(self.currency, bet_receipt_selection.total_est_returns,
                      msg=f'"{self.currency}" not found in "{bet_receipt_selection.total_est_returns}"')
        self.assertTrue(bet_receipt_selection.total_est_returns_value, msg='Total Est. Returns value not found')

        self.assertTrue(bet_receipt_selection.freebet_icon, msg='There is no freebet icon on bet receipt')
        self.assertEqual(bet_receipt_selection.total_stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg=f'Total Stake label "{bet_receipt_selection.total_stake_label}" '
                             f'is not the same as expected "{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}"')

        self.assertIn(self.currency, bet_receipt_selection.freebet_stake.text,
                      msg=f'"{self.currency}" not found in "{bet_receipt_selection.freebet_stake.text}"')
        actual_free_bet_stake_value = bet_receipt_selection.freebet_stake.text.replace(self.currency, '')
        self.assertEqual(float(actual_free_bet_stake_value), float(self.selected_freebet_value),
                         msg=f'Actual Total Stake value: "{actual_free_bet_stake_value}" '
                             f'not match with expected: "{self.selected_freebet_value}"')

        self.assertEqual(vec.betslip.BET_RECEIPT, self.site.byb_bet_receipt_panel.header.title,
                         msg=f'Bet receipt header title does not equal "{vec.betslip.BET_RECEIPT}" '
                             f'and is "{self.site.byb_bet_receipt_panel.header.title}" instead')
        self.assertTrue(self.site.byb_bet_receipt_panel.header.has_close_button(),
                        msg='Bet Receipt header does not have "Close" button')
        bet_receipt_header = self.site.byb_bet_receipt_panel.bet_receipt.header
        self.assertEqual(bet_receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt_header.bet_placed_text}" is not equal to expected '
                             f'"{vec.betslip.SUCCESS_BET}"')

        self.assertRegex(bet_receipt_header.receipt_datetime, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet receipt data and time: "{bet_receipt_header.receipt_datetime}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')

    def test_004_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet receipt
        EXPECTED: Bet receipt is removed
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')
