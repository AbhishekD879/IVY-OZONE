import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.quick_bet
@vtest
class Test_C852692_Verify_Quick_Deposit_section_for_users_without_credit_card(BaseSportTest):
    """
    TR_ID: C852692
    NAME: Verify Quick Deposit section for users without credit card
    DESCRIPTION: This test case verifies Quick Deposit section  within Quick Bet for users without credit card
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Log in with a user that has 0 on his balance and no credit card added to his account
    PRECONDITIONS: 3. Click/Tap 'Close' on 'Quick Deposit' pop-up
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: **NOTE** Steps 5-6 (Paypal, Neteller) are NOT supported anymore
    """
    keep_browser_open = True
    bet_amount = 1.00

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the application
        PRECONDITIONS: 2. Log in with a user that has 0 on his balance and no credit card added to his account
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes, expected_market = next(((market['market']['children'],market['market']['name']) for market in event['event']['children']
                             if market['market'].get('children') if market['market']['templateMarketName']=='Match Betting'), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            team1 = next((outcome['outcome']['name'] for outcome in outcomes
                          if outcome['outcome'].get('outcomeMeaningMinorCode') and
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not team1:
                raise SiteServeException('No Home team found')
            self.__class__.team1 = normalize_name(team1)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.__class__.team1 = event_params.team1
            expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)
        self._logger.info(f'*** Football event with event id "{self.eventID}" and team "{self.team1}" and market "{self.expected_market}"')
        self.site.login(username=tests.settings.username_without_credit_card)
        self.site.wait_content_state("Homepage")
        self.navigate_to_page(name='settings')
        self.site.wait_content_state('Settings')
        result = self.site.settings.allow_quick_bet.is_enabled()
        if not result:
            self.site.settings.allow_quick_bet.click()
        self.assertTrue(self.site.settings.allow_quick_bet.is_enabled(), msg='"Allow Quick Bet" option is not enabled')

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Added selection and all data are displayed in Quick Bet
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.team1, market_name=self.expected_market)

        self.__class__.quick_bet_panel = self.site.quick_bet_panel
        self.assertTrue(self.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='Add to betslip button is not disabled')
        self.assertTrue(self.quick_bet_panel.has_make_quick_deposit_button(),
                        msg='Make a deposit button is not displayed')
        quick_bet = self.quick_bet_panel.selection
        self.assertTrue(quick_bet.quick_stakes.items_names, msg='Quick stakes are not displayed')
        amount = quick_bet.content.amount_form.input
        self.assertTrue(amount.is_displayed(timeout=3), msg='Amount field is not displayed')
        amount.click()
        self.assertTrue(amount.is_enabled(timeout=1), msg='Amount field is not enabled.')
        amount.value = self.bet_amount
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')

    def test_002_enter_some_value_in_stake_field_manually_or_use_quick_stake__buttons(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field manually or use 'Quick Stake ' buttons
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Please deposit a min of £X.XX to continue placing your bet' message is displayed
        """
        if self.brand == 'ladbrokes':
            result = self.site.quick_bet_panel.wait_for_deposit_info_panel()
            self.assertTrue(result, msg=f'"Min Deposit" message is not shown')
            message = self.site.quick_bet_panel.deposit_info_message.text
        else:
            self.assertTrue(self.quick_bet_panel.info_panels.is_displayed(), msg=f'"Min Deposit" message is not shown')
            message = self.quick_bet_panel.info_panels.text
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(message, expected_message, msg=f'Actual message: "{message}" on the quick bet pannel is not '
                                                        f'same as Expected message: "{expected_message}"')

    def test_003_clicktap_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'Make a Deposit' button
        EXPECTED: * 'QUICK DEPOSIT' section is not displayed
        EXPECTED: * Quick Bet is closed
        EXPECTED: * User is navigated to 'Deposit' page
        EXPECTED: * 'Select a deposit method' title is displayed (an item 'Debit Cards' ( **LADBROKES** ) / items 'Visa'/'Matercard'/'Maestro' ( **CORAL** )
        """
        self.assertTrue(self.quick_bet_panel.make_quick_deposit_button.is_enabled(),
                        msg='Make a deposit button is not enabled')
        self.quick_bet_panel.make_quick_deposit_button.click()
        wait_for_result(lambda: self.site.deposit.is_displayed(),
                        name='Deposit page is not loaded',
                        timeout=20)
        self.assertTrue(self.site.deposit.deposit_sub_title.is_displayed(),
                        msg='Deposit page sus title text is not displayed')
        self._logger.info('As "Deposit Page" is opened, "QUICK DEPOSIT" section is not displayed and "Quick Bet" is closed')
        actual_text = self.site.deposit.deposit_sub_title.text
        self.assertEqual(actual_text, vec.bma.POPULAR_PAYMENT_METHODS,
                         msg=f'Actual sub title text: "{actual_text}" is not same as Expected sub title text: "{vec.bma.SELECT_A_DEPOSIT_METHOD}"')
        if self.brand == 'ladbrokes' and tests.settings.backend_env == 'tst2':
            self.assertTrue(self.site.select_deposit_method.debit_card_button.is_displayed(),
                            msg='"Master Card" button is not displayed"')
        else:
            self.assertTrue(self.site.select_deposit_method.master_card_button.is_displayed(),
                            msg='"Master Card" button is not displayed"')
            self.assertTrue(self.site.select_deposit_method.visa_button.is_displayed(),
                            msg='"Visa Card" button is not displayed')
            self.assertTrue(self.site.select_deposit_method.maestro_button.is_displayed(),
                            msg='"Maestro Card" button is not displayed')
