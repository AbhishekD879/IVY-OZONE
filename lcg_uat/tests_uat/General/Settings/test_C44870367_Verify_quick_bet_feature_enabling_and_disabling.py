import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870367_Verify_quick_bet_feature_enabling_and_disabling(BaseSportTest):
    """
    TR_ID: C44870367
    NAME: Verify quick bet feature enabling and disabling
    DESCRIPTION: Note: Quick Bet will not be displayed for Football -> Coupons page. It is disabled by default as per requirement.
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in the application.
        """
        self.site.login()
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children']), None)
            self.__class__.expected_market = normalize_name(event['event']['children'][0].get('market').get('name'))
            outcomes_resp = market['market']['children']
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id']
                                            for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            self.__class__.event_id = event['event']['id']
            self.__class__.team1 = list(self.selection_ids.keys())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_id = event.event_id
            self.__class__.team1 = event.team1
            expected_market = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)

    def test_001_navigate_to_settings_from_the_my_accountright_menu(self):
        """
        DESCRIPTION: Navigate to Settings from the My Account/Right menu.
        EXPECTED: 1. Settings page is displayed.
        EXPECTED: 2. Quick bet is enabled by default.
        """
        self.site.navigate_to_my_account_page(name='Settings')
        self.site.right_menu.click_item('Betting Settings')
        self.__class__.quick_bet = self.site.settings.allow_quick_bet
        self.assertTrue(self.quick_bet.is_displayed(), msg='"Allow Quick Bet" option is not shown')
        self.assertTrue(self.quick_bet.is_enabled(), msg='"Allow Quick Bet" option is not enabled')

    def test_002_disable_quick_bet_click_on_back_and_close_the_my_account_menu_select_any_selection_on_home_page_and_verify(self):
        """
        DESCRIPTION: Disable Quick Bet. Click on Back and close the My Account menu. Select any selection on Home page and verify.
        EXPECTED: 1. The selection is added directly to the bet slip, i.e. the bet slip counter displays the value as 1.
        EXPECTED: 2. Quick Bet is not displayed.
        """
        self.quick_bet.click()
        self.assertTrue(self.quick_bet.is_enabled(expected_result=False), msg='"Allow Quick Bet" option is not disabled')
        self.site.back_button.click()
        self.navigate_to_edp(event_id=self.event_id)
        self.site.wait_content_state(state_name='EventDetails')
        if self.site.brand == 'bma':
            self.expected_market = self.expected_market.upper()
        selection_button = self.get_selection_bet_button(selection_name=self.team1, market_name=self.expected_market)
        selection_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                         msg='"Quick Bet" section still displayed at the bottom of the page')
        self.site.wait_splash_to_hide(3)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        expected_betslip_counter_value = 1
        self.assertEqual(int(betslip_counter), expected_betslip_counter_value,
                         msg=f'Betslip counter "{betslip_counter}" is not the same '
                             f'as number of added selections "{expected_betslip_counter_value}"')
        selection_button.click()

    def test_003_navigate_to_settings_from_the_my_accountright_menu_and_enable_quick_bet_click_on_back_and_close_the_my_account_menu_select_any_selection_on_home_page_and_verify(self):
        """
        DESCRIPTION: Navigate to Settings from the My Account/Right menu and enable Quick Bet. Click on Back and close the My Account menu. Select any selection on Home page and verify.
        EXPECTED: 1. Quick Bet is displayed with the selection details.
        EXPECTED: 2. The selection should added to the bet slip, i.e. the bet slip counter displays the value as 1.
        """
        self.site.navigate_to_my_account_page(name='Settings')
        self.site.right_menu.click_item('Betting Settings')
        quick_bet = self.site.settings.allow_quick_bet
        quick_bet.click()
        self.assertTrue(quick_bet.is_enabled(), msg='"Allow Quick Bet" option is not enabled')
        self.site.back_button.click()
        self.navigate_to_edp(event_id=self.event_id)
        self.site.wait_content_state(state_name='EventDetails')
        if self.site.brand == 'bma':
            self.expected_market = self.expected_market.upper()
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                         msg='"Quick Bet" section is not closed')
        self.site.wait_splash_to_hide(3)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        expected_betslip_counter_value = 1
        self.assertEqual(int(betslip_counter), expected_betslip_counter_value,
                         msg=f'Betslip counter "{betslip_counter}" is not the same '
                             f'as number of added selections "{expected_betslip_counter_value}"')
