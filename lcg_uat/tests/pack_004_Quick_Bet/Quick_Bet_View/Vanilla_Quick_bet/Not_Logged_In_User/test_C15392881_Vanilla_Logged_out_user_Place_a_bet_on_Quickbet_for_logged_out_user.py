import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.quick_bet
@pytest.mark.reg165_fix
@vtest
class Test_C15392881_Vanilla_Logged_out_user_Place_a_bet_on_Quickbet_for_logged_out_user(BaseBetSlipTest, BaseSportTest,
                                                                                         ComponentBase):
    """
    TR_ID: C15392881
    NAME: [Vanilla] [Logged out user] Place a bet on Quickbet for logged out user
    DESCRIPTION: Verify that logged out user is able to place bet from Quickbet
    DESCRIPTION: NEED TO UPDATE!!!!
    DESCRIPTION: bet will not be placed automatically when there are pop-ups after login
    """
    keep_browser_open = True
    number_of_events = 1
    lp = {0: '1/2'}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: *Quickbet should be enabled in CMS
        PRECONDITIONS: *Make sure that that user is logged out
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is not logged off')
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.expected_market = normalize_name(event['event']['children'][0].get('market').get('name'))
            # match_result_market = next((market['market'] for market in event['event']['children'] if
            #                           market.get('market').get('templateMarketName') == 'Match Betting'), None)
            self.__class__.event_id = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.market_name = event['event']['children'][0]['market']['name']
            outcomes_resp = event['event']['children'][0]['market']['children']
            for outcome in outcomes_resp:
                for child in outcome.get('outcome', {}).get('children', []):
                    if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                        priceNum, priceDen = child['price']['priceNum'], child['price']['priceDen']
                        self.lp[0] = f'{priceNum}/{priceDen}'
                        self.__class__.selection_name = outcome['outcome']['name']
                        break
                if self.selection_name:
                    break
            if not self.selection_name:
                raise SiteServeException('There are no selections with LP prices')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_ids = event.selection_ids
            self.__class__.event_id = event.event_id
            self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
            self.__class__.market_name = self.expected_market_sections.match_result.title()
            expected_market = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)
            self.__class__.selection_name = list(self.selection_ids.keys())[0]

    def test_001_open_vanilla(self):
        """
        DESCRIPTION: Open Vanilla
        EXPECTED: The application is successfully loaded
        """
        self.site.wait_content_state('homepage')

    def test_002_go_to_any_sport_eg_football___select_any_odd(self):
        """
        DESCRIPTION: Go to any Sport (e.g Football)--> Select any odd
        EXPECTED: Quick Bet appears in the bottom of the screen
        EXPECTED: "Login & Place Bet" button is disabled by default
        """
        self.navigate_to_edp(event_id=self.event_id)
        if self.site.brand == 'bma':
            self.expected_market = self.expected_market.upper()
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market, selection_name=self.selection_name)
        quick_bet = wait_for_result(lambda: self.site.quick_bet_panel, timeout=60)
        self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                         msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='The button "Login & Place Bet" is active')

    def test_003_specify_any_quickstake_eg_5_(self):
        """
        DESCRIPTION: Specify any QuickStake (e.g. 5 )
        EXPECTED: "Login & Place Bet" button becomes enabled
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                        msg='The button "Login & Place Bet" is not active')

    def test_004_click_on_login__place_bet_button(self):
        """
        DESCRIPTION: Click on "Login & Place Bet" button
        EXPECTED: 'Log In' pop-up opens
        EXPECTED: Username and Password fields are available
        """
        self.site.quick_bet_panel.place_bet.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.assertTrue(self.dialog.username_field.is_displayed(),
                        msg='"username field" is not present in login dialog')
        self.assertTrue(self.dialog.password.is_displayed(),
                        msg='"password field" is not present in login dailog')

    def test_005_enter_valid_credentials_of_users_account_for_which_balance_is_positive____tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive -> Tap 'Log in' button
        EXPECTED: Bet is placed automatically
        EXPECTED: Bet Receipt with all betting details appears
        """
        self.dialog.username = tests.settings.default_username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=5)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        try:
            bet_receipt = self.site.quick_bet_panel.bet_receipt
        except Exception:
            self.site.close_all_dialogs(async_close=False, timeout=3)
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt = self.site.quick_bet_panel.bet_receipt
        actual_date_time = bet_receipt.header.receipt_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        self.assertTrue(bet_receipt.bet_id, msg='Bet Receipt number is not shown')
        self.assertEqual(bet_receipt.name, self.selection_name,
                         msg=f'Actual Selection Name "{bet_receipt.name}" does not match '
                             f'expected "{self.selection_name}"')
        self.event_name = self.event_name.replace(',', '')
        self.assertEqual(bet_receipt.event_name, self.event_name,
                         msg=f'Actual Event Name "{bet_receipt.event_name}" does not match '
                             f'expected "{self.event_name}"')
        self.assertEqual(bet_receipt.event_market, self.market_name,
                         msg=f'Actual market name: "{bet_receipt.event_market}" '
                             f'is not as expected: "{self.market_name}"')
        actual_total_stake = bet_receipt.total_stake
        expected_total_stake = f'{(self.bet_amount):.2f}'
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Actual total stake value: "{actual_total_stake}" doesn\'t match '
                             f'with expected: "{expected_total_stake}"')
        actual_estimate_returns = bet_receipt.estimate_returns
        self.verify_estimated_returns(est_returns=actual_estimate_returns,
                                      odds=self.lp[0],
                                      bet_amount=self.bet_amount)

    def test_006_click_on_close_button(self):
        """
        DESCRIPTION: Click on "Close" button
        EXPECTED: Quick Bet is closed
        """
        self.site.close_all_dialogs(async_close=False)
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_007_open_my_bets(self):
        """
        DESCRIPTION: Open "My Bets"
        EXPECTED: Just placed bet is displayed in Open Bets
        """
        self.device.refresh_page()
        current_url = self.device.get_current_url()
        self.device.navigate_to(url=current_url)
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, selection_name=self.selection_name)
        selection_name = bet.outcome_name
        self.assertEqual(selection_name, self.selection_name,
                         msg=f' Actual text "{selection_name}" is not same as Expected text "{self.selection_name}"')
