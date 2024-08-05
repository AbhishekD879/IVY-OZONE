import pytest
import voltron.environments.constants as vec
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choices
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - Not valid as OB is involved in granting a free bet for the user
@pytest.mark.crl_uat
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C44870230_Verify_Free_Bet_notification_on_Header_for_logged_in_user(BaseBetSlipTest, ComponentBase):
    """
    TR_ID: C44870230
    NAME: Verify Free Bet notification on Header for  logged in user
    DESCRIPTION: "-Verify Free Bet notification to Header area once user is logged into his account
    DESCRIPTION: 1.Customer places bets on any sports event using available Free bets which are sufficient for bet placement
    DESCRIPTION: - Check header balance
    DESCRIPTION: - Check freebet message on receipt
    DESCRIPTION: - Check Use FreeBet under selection in quick betslip
    DESCRIPTION: -Check user can use the freebet for placing bet(Single/multiple)"
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        freebet_username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(username=freebet_username)
        self.site.login(username=freebet_username,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION,
                        async_close_dialogs=False,
                        timeout_wait_for_dialog=1)

    def test_002_verify_free_bet_notification_on_header_area_once_user_is_logged_into_his_account(self):
        """
        DESCRIPTION: Verify Free Bet notification on Header area once user is logged into his account
        EXPECTED: Free bet available notification displayed
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, timeout=3)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION}" is not shown')
        dialog.close_dialog()
        self.assertTrue(self.site.home.is_displayed(), msg='Home page is not displayed')
        self.__class__.actual_balance = self.site.header.user_balance
        self.site.close_all_dialogs(async_close=False, timeout=3)

    def test_003_check_use_freebet_under_selection_in_quick_betslip(self):
        """
        DESCRIPTION: Check Use FreeBet under selection in quick betslip
        EXPECTED: user freebet hyperlink is displayed
        """
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on HomePage')
        bet_btn = bet_buttons_list[0]
        if bet_btn.is_displayed():
            self.scroll_to_we(bet_btn)
            bet_btn.click()
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertTrue(quick_bet.has_use_free_bet_link(), msg=f'{vec.betslip.USE_FREE_BET} link is not present')
            quick_bet.use_free_bet_link.click()
            self.select_free_bet()
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not shown')
            actual_bet_placed = self.site.quick_bet_panel.bet_receipt.header.bet_placed_text
            self.assertEqual(vec.betslip.SUCCESS_BET, actual_bet_placed,
                             msg=f'"{vec.betslip.SUCCESS_BET}"and "{actual_bet_placed}" are not same')
            self.assertTrue(self.site.quick_bet_panel.bet_receipt.has_free_bet_icon(),
                            msg='"Free bet icon" is not displayed')
        else:
            self.site.header.bet_slip_counter.click()
            self.place_single_bet(freebet=True)
            actual_bet_placed = self.site.bet_receipt.receipt_header.bet_placed_text
            self.assertEqual(vec.betslip.SUCCESS_BET, actual_bet_placed,
                             msg=f'"{vec.betslip.SUCCESS_BET}"and "{actual_bet_placed}" are not same')

    def test_004_check_user_can_use_the_freebet_for_placing_betsinglemultiple(self, expected_betslip_counter_value=0):
        """
        DESCRIPTION: Check user can use the freebet for placing bet(Single/multiple)
        EXPECTED: Single and multiple bets are placed using free bets
        """
        selection_ids = []
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(
            LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True,
                                                     additional_filters=cashout_filter, in_play_event=False)
        event1 = choices(events, k=2)
        for event in event1:
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(all_selection_ids.values())[0]
            selection_ids.append(selection_id)
        self.open_betslip_with_selections(selection_ids=selection_ids)

    def test_005_verify_user_can__places_bets_on_any_sports_event_using_available_free_bets_which_are_sufficient_for_bet_placement(self):
        """
        DESCRIPTION: Verify user can  places bets on any sports event using available Free bets which are sufficient for bet placement
        EXPECTED: Bet placed using freebet successfully
        """
        self.place_multiple_bet(number_of_stakes=1, freebet=True)
        actual_bet_placed = self.site.bet_receipt.receipt_header.bet_placed_text
        self.assertEqual(vec.betslip.SUCCESS_BET, actual_bet_placed,
                         msg=f'"{vec.betslip.SUCCESS_BET}"and "{actual_bet_placed}" are not same')

    def test_006_verify_no_amount_is_deducted_from_header_balance(self):
        """
        DESCRIPTION: Verify No amount is deducted from header balance
        EXPECTED: Header balance display same
        """
        expected_balance = self.site.header.user_balance
        self.assertEqual(self.actual_balance, expected_balance,
                         msg=f'"{self.actual_balance}" and "{expected_balance}" are not same')

    def test_007_verify__freebet_message_on_receipt(self):
        """
        DESCRIPTION: Verify  freebet message on receipt
        EXPECTED: Message displayed
        """
        self.assertTrue(self.site.bet_receipt.has_free_bet_icon(), msg='"Free bet icon" is not displayed')
