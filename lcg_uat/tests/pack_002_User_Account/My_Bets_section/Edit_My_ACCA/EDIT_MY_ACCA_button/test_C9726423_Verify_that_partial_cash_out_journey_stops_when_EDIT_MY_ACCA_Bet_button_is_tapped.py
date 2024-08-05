import pytest
import tests
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from time import sleep
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C9726423_Verify_that_partial_cash_out_journey_stops_when_EDIT_MY_ACCA_Bet_button_is_tapped(BaseCashOutTest):
    """
    TR_ID: C9726423
    NAME: Verify that partial cash out journey stops when 'EDIT MY ACCA/Bet' button is tapped
    DESCRIPTION: This test case verifies that Partial cash out journey stops and not shown when 'EDIT MY ACCA' button is tapped
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login and place a multiple bet with Partial Cash Out available
    PRECONDITIONS: Navigate to My Bets page
    PRECONDITIONS: NOTE: Verifications should be done on Cash Out and on Open Bets tabs
    """
    keep_browser_open = True
    number_of_events = 3
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS: Login and place a multiple bet with Partial Cash Out available
        PRECONDITIONS: Navigate to My Bets page
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
        sleep(2)
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
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_003_tap_edit_my_accabet_buttonthat_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA/Bet' button
        DESCRIPTION: that Partial cash out journey is not shown and edit mode for ACCA is opened
        EXPECTED: - Partial Cash Out journey is closed and not shown
        EXPECTED: - Cash Out and Partial Cash Out button is not shown at all
        EXPECTED: - Edit mode for ACCA is opened
        """
        self.bet.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(10)
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')
        self.assertFalse(self.bet.has_buttons_panel(expected_result=False),
                         msg=f'"{self.bet.has_buttons_panel()}" is displayed')

    def test_004_tap_cancel_editing_buttonverify_that_edit_mode_for_acca_is_closed_and_cash_out_and_partial_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        DESCRIPTION: Verify that edit mode for ACCA is closed and Cash Out and Partial Cash Out button is shown
        EXPECTED: - Edit mode for ACCA is closed
        EXPECTED: - Cash Out and Partial Cash Out button is shown
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

        # below code for cashout
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            sleep(2)
            _, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE,
                event_names=self.event_names)
            self.assertTrue(self.bet, msg=f'"{self.bet}" is not displayed')
            self.test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown()
            self.test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_accabet_button_is_shown()
            self.test_003_tap_edit_my_accabet_buttonthat_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened()
            self.bet.edit_my_acca_button.click()
            sleep(3)
            edit_my_acca_text = self.bet.edit_my_acca_button.name
            self.assertEqual(edit_my_acca_text, vec.EMA.EDIT_MY_BET,
                             msg=f'Actual text:"{vec.EMA.CANCEL}" is not changed to Expected text:"{vec.EMA.EDIT_MY_BET}".')
            self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(),
                            msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}" button is not displayed')
            self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                            msg=f'"{vec.bet_history.PARTIAL_CASH_OUT_BTN_TEXT}" button is not displayed')
