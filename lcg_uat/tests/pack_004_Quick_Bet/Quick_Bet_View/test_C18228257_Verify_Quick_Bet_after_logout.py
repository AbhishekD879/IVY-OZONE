import pytest
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.user_account
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.each_way
@pytest.mark.mobile_only
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.medium
@vtest
class Test_C18228257_Verify_Quick_Bet_after_logout(BaseBetSlipTest, BaseRacing, BaseUserAccountTest):
    """
    TR_ID: C18228257
    VOL_ID: C9697669
    NAME: Verify Quick Bet after logout
    DESCRIPTION: This test case verifies Quick Bet after logout
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. In order to trigger case when the session is over, perform the next steps:
    PRECONDITIONS: * Log in to one browser tab
    PRECONDITIONS: * Duplicate tab
    PRECONDITIONS: * Log out from the second tab -> session is over in both tabs
    PRECONDITIONS: 4. Application is loaded
    PRECONDITIONS: 5. User is logged in
    """
    keep_browser_open = True
    bet_amount = 0.03

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event
        DESCRIPTION: Open EDP
        DESCRIPTION: Login
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'LP'))
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=additional_filter)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.created_event_name = normalize_name(event['event']['name'])
            market = next((market for market in event['event']['children']
                           if market['market']['name'] == 'Win or Each Way'), None)
            self.assertTrue(market, msg='Win or Each Way market is not found')
            self.__class__.market_name = market['market']['name']
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            self.__class__.eventID = event.event_id
            self.__class__.created_event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            self.__class__.market_name = \
                self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.replace('|', '')
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')

    def test_001_add_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        self.add_selection_to_quick_bet()

    def test_002_enter_value_in_stake_field_and_select_ew_checkbox_if_available(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and select 'E/W' checkbox (if available)
        EXPECTED: 'Stake' field is populated with entered value
        EXPECTED: 'E/W' checkbox is selected
        """
        try:
            quick_bet = self.site.quick_bet_panel.selection.content
        except StaleElementReferenceException:
            quick_bet = self.site.quick_bet_panel.selection.content

        quick_bet.amount_form.input.value = self.bet_amount
        quick_bet.each_way_checkbox.click()
        expected_bet_amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(quick_bet.amount_form.input.value, str(expected_bet_amount),
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not '
                             f'match expected "{expected_bet_amount}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        button_name = self.site.quick_bet_panel.place_bet.name
        self.assertEqual(button_name, vec.betslip.BET_NOW,
                         msg=f'Actual button name "{button_name}" does not match expected "{vec.betslip.BET_NOW}"')

    def test_003_make_steps_listed_in_preconditions(self):
        """
        DESCRIPTION: Make steps listed in preconditions
        EXPECTED: User session is over
        """
        self.device.open_new_tab()
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(timeout=5), msg='User is not logged in')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        # Quick bet is shown immediately only in browser window which is created by the test
        try:
            self.navigate_to_page('logout')
        except StaleElementReferenceException:
            self.site.wait_splash_to_hide()
        if self.device_type == 'bma':
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=15)
            if dialog is None:
                raise VoltronException(f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not present on page')
            dialog.close_dialog()
            dialog_closed = dialog.wait_dialog_closed(timeout=self.site._wait_login_dialog_closed)
            if not dialog_closed:
                raise VoltronException('Login Dialog is not closed')
        self.navigate_to_page("Homepage")
        self.site.wait_content_state(state_name='HomePage')
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')

        self.device.close_current_tab()
        self.device.open_tab(tab_index=0)

    def test_004_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * 'Log out' pop-up is displayed
        EXPECTED: * Quick Bet stays opened
        EXPECTED: * 'BET NOW' button becomes 'LOG IN & BET NOW'
        EXPECTED: * Entered on step #4 value is remembered
        EXPECTED: * 'E/W' checkbox stays selected
        """
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=50)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not shown')
        self.dialog.wait_error_message()
        self.dialog.close_dialog()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog was not closed')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        quick_bet = self.site.quick_bet_panel.selection.content
        self.assertEqual(float(quick_bet.amount_form.input.value), float(self.bet_amount),
                         msg=f'Actual amount "{float(quick_bet.amount_form.input.value)}" does not '
                             f'match expected "{float(self.bet_amount)}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')

        button_name = self.site.quick_bet_panel.place_bet.name
        self.assertEqual(button_name, vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET,
                         msg=f'Actual button name "{button_name}" does not match '
                         f'expected "{vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET}"')

    def test_005_tap_x_button_on_log_out_pop_up(self):
        """
        DESCRIPTION: Tap 'X' button on 'Log out' pop-up
        EXPECTED: * 'Log out' pop-up is closed
        EXPECTED: * Quick Bet stays opened
        """
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
