import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C9726422_Verify_displaying_EDIT_MY_ACCA_Bet_button_during_Partial_Cash_Out_Journey(BaseCashOutTest):
    """
    TR_ID: C9726422
    NAME: Verify displaying 'EDIT MY ACCA/Bet' button during Partial Cash Out Journey
    DESCRIPTION: This test case verifies displaying 'EDIT MY ACCA' button during Partial Cashout Journey
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login and place a multiple bet with Partial Cash Out available
    PRECONDITIONS: 2. Navigate to My Bets page -> Cash Out tab
    PRECONDITIONS: 3. Navigate to My Bets page -> Open Bets tab
    PRECONDITIONS: Need to verify on both Cash Out tab and Open Bets tab
    """
    keep_browser_open = True
    bet_amount = 1
    number_of_events = 3
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS:  Login and place a multiple bet with Partial Cash Out available
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                event_name = normalize_name(event['event']['name'])
                self.event_names.append(event_name)
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            for event in event_params:
                self.__class__.event_names = f'{event.team1} v {event.team2}'
            self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE,
            event_names=self.event_names)
        self.assertTrue(self.bet, msg=f'"{self.bet}" is not displayed')

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        self.__class__.partial_cashout_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_accabet_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY ACCA/Bet' button is shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out value is changing
        """
        self.bet.buttons_panel.move_partial_cashout_slider()
        sleep(2)
        right_slider_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        self.assertTrue(right_slider_value > self.partial_cashout_value,
                        msg=f'right slided value "{right_slider_value}" is not greater than the previous cashout value "{self.partial_cashout_value}"')
        self.bet.buttons_panel.partial_cashout_close_button.click()
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_003_tap_x_button_to_close_partial_cash_outverify_that_partial_cash_out_bar_is_closed_and_edit_my_accabet_button_is_shown(self):
        """
        DESCRIPTION: Tap 'X' button to close partial cash out
        DESCRIPTION: Verify that Partial Cash Out bar is closed and 'EDIT MY ACCA/Bet' button is shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is closed
        EXPECTED: - 'Cash Out' and 'Partial Cash Out' buttons are shown
        """
        self.bet.buttons_panel.partial_cashout_close_button.click()
        self.assertFalse(self.bet.buttons_panel.wait_for_cashout_slider(expected_result=False),
                         msg='PARTIAL CASHOUT slider is present')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(),
                        msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}" button is not displayed')
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg=f'"{vec.bet_history.PARTIAL_CASH_OUT_BTN_TEXT}" button is not displayed')

    def test_004_tap_partial_cash_out_button_one_more_timeverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button one more time
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_005_tap_partial_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button
        DESCRIPTION: Verify that 'Confirm Cash Out' and 'EDIT MY ACCA/Bet' buttons are shown and enabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - 'Confirm Cash Out' button is shown and enabled
        EXPECTED: - 'Confirm Cash Out' button is flashing 3 times
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.has_cashout_button(), msg='confirm cashout button is not displayed ')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_006_wait_while_confirm_cash_out_button_disappearverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Wait while 'Confirm Cash Out' button disappear
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        self.bet.buttons_panel.cashout_button.wait_for_element_disappear()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_007_tap_partial_cash_out_button_againverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button again
        DESCRIPTION: Verify that 'Confirm Cash Out' and 'EDIT MY ACCA/Bet' buttons are shown and enabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - 'Confirm Cash Out' button is shown and enabled
        EXPECTED: - 'Confirm Cash Out' button is flashing 3 times
        """
        self.test_005_tap_partial_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled()

        # flashing cannot test in automation

    def test_008_tap_confirm_cash_out_buttonverify_that_edit_my_accabet_button_is_shown_and_disabled(self):
        """
        DESCRIPTION: Tap 'Confirm Cash Out' button
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button is shown and disabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and disabled
        EXPECTED: - Spiner for partial cash out is shown
        EXPECTED: - 'Partial Cash Out Successful' is shown
        """
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertFalse(self.bet.edit_my_acca_button.is_enabled(expected_result=False),
                         msg=f'"{vec.EMA.EDIT_MY_BET}" button is enabled')
        self.assertTrue(self.bet.buttons_panel.has_spinner_icon, msg='Spinner icon is not present')
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')
        success_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS if self.brand == 'ladbrokes' \
            else vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=success_message, timeout=10),
                        msg=f'Message "{success_message}" was not shown')

    def test_009_verify_that_after_partial_cash_out_successful_message_disappearnavigate_between_tabs_the_edit_my_accabet_button_is_shown_and_enabled(self):
        """
        DESCRIPTION: Verify that after 'Partial Cash Out Successful' message disappear(navigate between tabs) the 'EDIT MY ACCA/Bet' button is shown and enabled
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enabled
        EXPECTED: - On Open Betds tab: 'Partial Cash Out History' drop down is shown with cashed out value in the table
        """
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.partial_cash_out_history.header.click()
        content = self.bet.partial_cash_out_history.content
        table = content.table
        cashout_value = list(table.items_as_ordered_dict.keys())
        self.assertTrue(cashout_value, msg='cashed out value is not displayed')

        # below code for cashout tab
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.site.wait_content_state_changed()
            _, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history._bet_types_TBL.upper(),
                event_names=self.event_names)
            self.assertTrue(self.bet, msg=f'"{self.bet}" is not displayed')
            self.test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown()
            self.test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_accabet_button_is_shown()
            self.test_003_tap_x_button_to_close_partial_cash_outverify_that_partial_cash_out_bar_is_closed_and_edit_my_accabet_button_is_shown()
            self.test_004_tap_partial_cash_out_button_one_more_timeverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown()
            self.test_005_tap_partial_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled()
            self.test_006_wait_while_confirm_cash_out_button_disappearverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown()
            self.test_007_tap_partial_cash_out_button_againverify_that_confirm_cash_out_and_edit_my_accabet_buttons_are_shown_and_enabled()
            self.test_008_tap_confirm_cash_out_buttonverify_that_edit_my_accabet_button_is_shown_and_disabled()
            self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                            msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
            self.bet.buttons_panel.partial_cashout_button.click()
            self.bet.partial_cash_out_history.header.click()
            content = self.bet.partial_cash_out_history.content
            table = content.table
            cashout_value = list(table.items_as_ordered_dict.keys())
            self.assertTrue(cashout_value, msg='cashed out value is not displayed')
