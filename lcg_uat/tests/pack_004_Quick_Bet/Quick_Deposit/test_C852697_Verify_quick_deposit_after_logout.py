import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.quick_deposit
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.login
@pytest.mark.reg156_fix
@vtest
class Test_C852697_Verify_quick_deposit_after_logout(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C852697
    VOL_ID: C9698130
    NAME: Verify Quick Deposit after logout
    DESCRIPTION: This test case verifies Quick Deposit section within Quick Bet after logout
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User has positive balance and credit cards added to his account
    PRECONDITIONS: 4. In order to trigger case when the session is over, perform the next steps:
    PRECONDITIONS: * Log in to one browser tab
    PRECONDITIONS: * Duplicate tab
    PRECONDITIONS: * Log out from the second tab -> session is over in both tabs
    """
    keep_browser_open = True
    quick_bet = None
    over_balance = None
    username = None
    card_type = None
    currency = u'£'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Invictus application, create event
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            event = self.get_active_events_for_category(category_id=category_id)[0]

            self.__class__.market_name = next((market['market']['name'] for market in event['event']['children']
                                               if market.get('market').get('templateMarketName') == 'Match Betting'), None)

            outcomes = next((market['market']['children'] for market in event['event']['children']
                             if market['market']['templateMarketName'] == 'Match Betting' and
                             market['market'].get('children')), None)

            if not outcomes:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self.__class__.team2 = list(self.selection_ids.keys())[1]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.team2, self.__class__.selection_ids, self.__class__.eventID = \
                event_params.team1, event_params.team2, event_params.selection_ids, event_params.event_id
            self.__class__.event_name = f'{self.team1} v {self.team2}'
            self.__class__.market_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '')

        self._logger.info(f'*** Football event with id "{self.eventID}", name "{self.event_name}",'
                          f'first team "{self.team1}", second team "{self.team2}" and selection ids "{self.selection_ids}"')

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is successfully logged in
        """
        self.site.login(username=tests.settings.quick_deposit_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_navigate_to_football_event_details_page(self):
        """
        DESCRIPTION: Navigate to Event Details page
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_click_on_football_event_bet_button(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick Bet is displayed
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        markets_list = wait_for_result(lambda : self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict, timeout=15)
        self.assertTrue(markets_list, msg='No markets found')

        market_name = self.market_name if self.brand == 'ladbrokes' or self.device_type == 'desktop' \
            else self.market_name.upper()
        section = markets_list.get(market_name)
        self.assertTrue(section, msg=f'{market_name} section is not found')

        output_prices_list = section.outcomes.items_as_ordered_dict
        self.assertTrue(output_prices_list, msg='Match result output prices were not found on Event Details page')

        outcome_title = self.team1 if self.brand != 'ladbrokes' else self.team1.upper()
        outcome = output_prices_list.get(outcome_title)
        self.assertTrue(outcome, msg=f'"{outcome_title}" not found in {list(output_prices_list.keys())}')
        outcome.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')

        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.assertEqual(self.quick_bet.content.event_name, self.event_name,
                         msg=f'Actual event name "{self.quick_bet.content.event_name}" '
                             f'does not match expected "{self.event_name}"')

    def test_004_enter_numeric_value_to_stake(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance and select E/W option (if available)
        EXPECTED: * 'Please deposit a min <currency symbol>XX.XX to continue placing your bet' error message is displayed below 'QUICK BET' header
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        """
        self.__class__.over_balance = 10.50
        self.__class__.quick_bet = self.site.quick_bet_panel.selection

        self.quick_bet.content.amount_form.input.value = self.user_balance + self.over_balance

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance)
        result = self.site.quick_bet_panel.wait_for_quick_bet_info_panel() if self.brand == 'bma' \
            else self.site.quick_bet_panel.wait_for_deposit_info_panel()
        self.assertTrue(result, msg='Quick Bet Info Panel is not present')

        actual_message = self.site.quick_bet_panel.info_panels_text[0] if self.brand != 'ladbrokes' \
            else self.site.quick_bet_panel.deposit_info_message.text
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

    def test_005_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: 'Quick Deposit' section is expanded
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='Quick Deposit section is not shown')

    def test_006_log_out_from_second_tab(self):
        """
        DESCRIPTION: Log out from the second tab
        """
        self.device.open_new_tab()
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(timeout=5), msg='User is not logged in')
        self.site.logout()
        self.site.wait_content_state(state_name='HomePage')
        self.device.close_current_tab()
        self.device.open_tab(tab_index=0)

    def test_007_Verify_Quick_Deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: * Quick Deposit section is NOT displayed anymore
        EXPECTED: * 'Please deposit a min <currency symbol>XX.XX to continue placing your bet' error message is NOT displayed
        EXPECTED: * 'Log out' pop-up is displayed
        EXPECTED: * Quick Bet section stays opened
        EXPECTED: * 'Stake' field is populated with value entered on step #4
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=60)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not shown')

        dialog.close_dialog()
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog was not closed')

        self.assertTrue(self.site.wait_for_quick_bet_panel(),
                        msg='Quick Bet is not present')
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=False),
                         msg='Quick Bet Info Panel is present')
