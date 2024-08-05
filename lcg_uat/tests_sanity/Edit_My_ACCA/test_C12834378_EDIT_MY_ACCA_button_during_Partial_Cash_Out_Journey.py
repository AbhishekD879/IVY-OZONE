import pytest
import tests
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod   # EMA is NA for Coral prod, Applicable for other envs
@pytest.mark.sanity
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.issue('https://jira.corp.entaingroup.com/browse/OZONE-6868')
@vtest
class Test_C12834378_EDIT_MY_ACCA_button_during_Partial_Cash_Out_Journey(BaseCashOutTest):
    """
    TR_ID: C12834378
    NAME: 'EDIT MY ACCA' button during Partial Cash Out Journey
    DESCRIPTION:
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Login into App
    PRECONDITIONS: 3. Place single bet and multiple bet with more than 4 selection (e.g. ACCA 5) (selections should have cash out available)
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: 4. Navigate to My Bets page
    PRECONDITIONS: NOTE: Verifications should be done on Cash Out and on Open Bets tabs
    """
    keep_browser_open = True
    bet_amount = 1
    number_of_events = 4
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
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

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_acca_button_and_partial_cash_out_bar_are_shown(
            self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY ACCA' button and Partial Cash Out bar are shown
        EXPECTED: * 'EDIT MY ACCA' button is shown and enable
        EXPECTED: * Partial Cash Out bar is shown
        """
        self.site.open_my_bets_open_bets()
        sleep(2)
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_ACC4.upper(),
            event_names=self.event_names)
        self.assertTrue(self.bet, msg=f'"{self.bet}" is not displayed')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        self.__class__.partial_cashout_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_acca_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY ACCA' button is shown
        EXPECTED: * EDIT MY ACCA' button is shown and enable
        EXPECTED: * Partial Cash Out value is changing
        """
        try:
            self.bet.buttons_panel.move_partial_cashout_slider()
            sleep(2)
        except Exception:
            self.bet.buttons_panel.move_partial_cashout_slider()
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

    def test_003_tap_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_acca_buttons_are_show(self):
        """
        DESCRIPTION: Tap 'Cash Out' button
        DESCRIPTION: Verify that 'Confirm Cash Out' and 'EDIT MY ACCA' buttons are show
        EXPECTED: * 'EDIT MY ACCA' button is shown and enable
        EXPECTED: * 'Confirm Cash Out' button is shown and enabled
        EXPECTED: * 'Confirm Cash Out' button is flashing 3 times
        Note: colours flashing is not automated
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_004_tap_edit_my_acca_buttonverify_that_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened(
            self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA' button
        DESCRIPTION: Verify that Partial cash out journey is not shown and edit mode for ACCA is opened
        EXPECTED: * Partial Cash Out journey is closed and not shown
        EXPECTED: * Cash Out and Partial Cash Out button is not shown at all
        EXPECTED: * Edit mode for ACCA is opened
        """
        self.bet.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')
        self.assertFalse(self.bet.has_buttons_panel(expected_result=False),
                         msg=f'"{self.bet.has_buttons_panel()}" is displayed')

    def test_005_tap_cancel_editing_buttonverify_that_edit_mode_for_acca_is_closed_and_cash_out_and_partial_cash_out_button_is_shown(
            self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        DESCRIPTION: Verify that edit mode for ACCA is closed and Cash Out and Partial Cash Out button is shown
        EXPECTED: * Edit mode for ACCA is closed
        EXPECTED: * Cash Out and Partial Cash Out button is shown
        """
        self.bet.edit_my_acca_button.click()
        sleep(3)
        edit_my_acca_text = self.bet.edit_my_acca_button.name
        self.assertEqual(edit_my_acca_text, vec.EMA.EDIT_MY_BET,
                         msg=f'Actual text:"{vec.EMA.CANCEL}" is not changed to Expected text:"{vec.EMA.EDIT_MY_BET}".')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(),
                        msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}" button is not displayed')
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg=f'"{vec.bet_history.PARTIAL_CASH_OUT_BTN_TEXT}" button is not displayed')

    def test_006_run_1_3_step_one_more_time(self):
        """
        DESCRIPTION: Run 1-3 step one more time
        EXPECTED: Results are the same
        """
        self.test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_acca_button_and_partial_cash_out_bar_are_shown()
        self.test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_acca_button_is_shown()
        self.test_003_tap_cash_out_buttonverify_that_confirm_cash_out_and_edit_my_acca_buttons_are_show()

    def test_007_tap_confirm_cash_out_buttonverify_that_edit_my_acca_button_is_shown_and_disabled(self):
        """
        DESCRIPTION: Tap 'Confirm Cash Out' button
        DESCRIPTION: Verify that 'EDIT MY ACCA' button is shown and disabled
        EXPECTED: * 'EDIT MY ACCA' button is shown and disabled
        EXPECTED: * Spiner for partial cash out is shown
        EXPECTED: * 'Successful cash out' is shown
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        success_message = self.bet.cash_out_successful_message
        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertEqual(success_message, expected_message,
                         msg=f'Success message "{success_message}" is not the same as expected: "{expected_message}"')

    def test_008_verify_that_successful_cash_out_message_is_shown__and_edit_my_acca_button_is_shown_and_enabled(self):
        """
        DESCRIPTION: Verify that 'Successful cash out' message is shown  and 'EDIT MY ACCA' button is shown and enabled
        EXPECTED: * 'EDIT MY ACCA' button is shown and enabled
        EXPECTED: * On Open Bets tab: 'Show Partial Cash Out History' drop down is shown with cashed out value in the table
        """
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.partial_cash_out_history.header.click()
        content = self.bet.partial_cash_out_history.content
        table = content.table
        cashout_value = list(table.items_as_ordered_dict.keys())
        self.assertTrue(cashout_value, msg='cashed out value is not displayed')
