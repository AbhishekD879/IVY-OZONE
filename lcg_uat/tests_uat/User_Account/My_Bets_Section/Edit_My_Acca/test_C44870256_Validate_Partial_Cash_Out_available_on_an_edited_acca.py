import pytest
import tests
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870256_Validate_Partial_Cash_Out_available_on_an_edited_acca(BaseCashOutTest):
    """
    TR_ID: C44870256
    NAME: Validate  Partial Cash Out available on an edited acca
    """
    keep_browser_open = True
    bet_amount = 1
    number_of_events = 4
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMB -> Enabled
        PRECONDITIONS: Login and place a multiple bet with Partial Cash Out available
        PRECONDITIONS: Navigate to My Bets page
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in cms')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_bet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY BET' button and Partial Cash Out bar are shown
        EXPECTED: 'EDIT MY BET' button is shown and enable
        EXPECTED: Partial Cash Out bar is shown
        """
        self.site.open_my_bets_open_bets()
        self.__class__.bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bet, msg=f'"{self.bet}" is not displayed')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg=f'"{self.bet.buttons_panel.has_partial_cashout_slider}" was not appeared')

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_bet_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY BET' button is shown
        EXPECTED: 'EDIT MY BET' button is shown and enable
        EXPECTED: Partial Cash Out value is changing
        """
        partial_cashout_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        right_slider_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        self.assertEqual(right_slider_value, partial_cashout_value,
                         msg=f'Actual value:"{partial_cashout_value}"is not changed to Expected value:"{right_slider_value}"')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')

    def test_003_tap_edit_my_bet_buttonthat_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' button
        DESCRIPTION: that Partial cash out journey is not shown and edit mode for ACCA is opened
        EXPECTED: Partial Cash Out journey is closed and not shown
        EXPECTED: Cash Out and Partial Cash Out button is not shown at all
        EXPECTED: Edit mode for ACCA is opened
        """
        self.bet.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        wait_for_result(lambda: self.bet.edit_my_acca_button.name,
                        name=f'"{vec.EMA.CANCEL}" to be displayed', timeout=30)
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')
        self.assertFalse(self.bet.has_buttons_panel(expected_result=False), msg=f'"{self.bet.has_buttons_panel()}" is displayed')

    def test_004_tap_cancel_editing_buttonverify_that_edit_mode_for_acca_is_closed_and_cash_out_and_partial_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        DESCRIPTION: Verify that edit mode for ACCA is closed and Cash Out and Partial Cash Out button is shown
        EXPECTED: Edit mode for ACCA is closed
        EXPECTED: Cash Out and Partial Cash Out button is shown
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
