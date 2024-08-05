import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.deeplink
@pytest.mark.betslip
@pytest.mark.numeric_keyboard
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.timeout(1000)
@pytest.mark.login
@vtest
class Test_C29019_Verify_Currency_Symbol_on_the_Betslip(BaseBetSlipTest):
    """
    TR_ID: C29019
    NAME: Verify Currency Symbol on the Betslip
    DESCRIPTION: This test case verifies Verify Currency on the Betslip page
    PRECONDITIONS: *   Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**
    """
    device_name = 'Nexus 5X' if not tests.use_browser_stack else tests.default_pixel
    keep_browser_open = True
    selection_ids_2 = selection_ids_3 = None
    multiples_section = None
    singles_stake = multiples_stake = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Prepare 3 different events (football, basketball, volleyball)
        EXPECTED: User should be able to use previously generated events.
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections "{self.selection_ids}"')

            self.__class__.selection_ids_2 = self.get_active_event_selections_for_category(category_id=self.ob_config.backend.ti.basketball.category_id)
            self.__class__.team1 = list(self.selection_ids_2.keys())[0]
            self._logger.info(f'*** Found Basketball event with selections "{self.selection_ids_2}"')

            self.__class__.selection_ids_3 = self.get_active_event_selections_for_category(
                category_id=self.ob_config.backend.ti.volleyball.category_id)
            self.__class__.team2 = list(self.selection_ids_3.keys())[0]
            self._logger.info(f'*** Found Volleyball event with selections "{self.selection_ids_2}"')

        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
            event_params = self.ob_config.add_basketball_event_to_autotest_league()
            self.__class__.team1, self.__class__.selection_ids_2 = event_params.team1, event_params.selection_ids
            event_params = self.ob_config.add_volleyball_event_to_austrian_league()
            self.__class__.team2, self.__class__.selection_ids_3 = event_params.team2, event_params.selection_ids

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        self.site.login(async_close_dialogs=False)

    def test_002_add_one_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one selection to the BetSlip
        EXPECTED: BetSlip should contain one sport event (football)
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_003_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: *   Betslip is shown
        EXPECTED: *   'Singles' section is present
        """
        singles_section = self.get_betslip_sections().Singles
        singles_name = singles_section.name
        stake_title, self.__class__.singles_stake = singles_section.items()[0]

        self.assertEqual(singles_name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg='Section title "%s" is not the same as expected "%s"' %
                             (singles_name, vec.betslip.BETSLIP_SINGLES_NAME))

    def test_004_verify_currency_symbol_next_to_the_est_returns_value(self, currency='£'):
        """
        DESCRIPTION: Verify currency symbol next to the **'Est. Returns'** value
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        actual_currency = self.singles_stake.est_returns_currency
        self.assertEqual(actual_currency, currency,
                         msg='Currency symbol next to \'Est. Returns\' value "%s" is not the same as expected "%s"' %
                             (actual_currency, currency))

    def test_005_verify_currency_symbol_next_to_the_total_stake_and_total_est_returns_values(self, currency='£'):
        """
        DESCRIPTION: Verify currency symbol next to the ** Total Stake ** and **Total Est. Returns** values
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        actual_total_stake_currency = self.get_betslip_content().total_stake_currency
        self.assertEqual(actual_total_stake_currency, currency,
                         msg='Currency symbol next to \'Total Stake\' "%s" is not the same as expected "%s"' %
                             (actual_total_stake_currency, currency))
        actual_total_est_returns_currency = self.get_betslip_content().total_estimate_returns_currency
        self.assertEqual(actual_total_est_returns_currency, currency,
                         msg='Currency symbol next to \'Total Est. Returns\' "%s" is not the same as expected "%s"' %
                             (actual_total_est_returns_currency, currency))

    def test_006_add_two_or_more_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from different events to the Bet Slip
        EXPECTED: * Selections are added
        EXPECTED: * 'All single stakes' field is present
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids_2[self.team1],
                                                         self.selection_ids_3[self.team2]))

    def test_007_verify_currency_symbol_within_quick_stake_buttons_on_the_numeric_keyboard(self, currency='£'):
        """
        DESCRIPTION: Verify currency symbol within Quick stake buttons on the numeric keyboard
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        if self.brand != 'ladbrokes' and self.device_type == 'mobile':
            singles_section = self.get_betslip_sections().Singles
            stake_title, self.__class__.singles_stake = singles_section.items()[0]
            self.singles_stake.amount_form.input.click()
            try:
                quick_stake_buttons = self.get_betslip_content().betnow_section.quick_stake_panel.items_as_ordered_dict
                self.assertTrue(quick_stake_buttons, msg='Quick stake buttons not found')
                for button_name, button in quick_stake_buttons.items():
                    self.assertIn(currency, button_name,
                                  msg='Currency symbol within "%s" is not the same as expected "%s"' % (button_name, currency))

            except VoltronException:
                self._logger.warning('*** Skipping step as Quick Stakes buttons are not shown')
        else:
            self._logger.warning('*** Skipping step as Quick Stakes buttons are not relevant for Ladbrokes')

    def test_008_go_to_bet_slip_multiples_section(self):
        """
        DESCRIPTION: Go to Bet Slip, 'Multiples' section
        EXPECTED: 'Multiples' section is selected
        """
        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake_title, self.__class__.multiples_stake = self.multiples_section.items()[0]
        self.multiples_stake.scroll_to()

    def test_009_repeat_steps_4_5(self, currency='£'):
        """
        DESCRIPTION: Repeat steps # 4 - 5
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        actual_est_returns_currency = self.multiples_stake.est_returns_currency
        self.assertEqual(actual_est_returns_currency, currency,
                         msg='Currency symbol next to \'Est. Returns\' value "%s" is not the same as expected "%s"' %
                             (actual_est_returns_currency, currency))

    def test_010_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        self.clear_betslip()
        self.site.wait_content_state('Homepage')
        self.site.logout(timeout=15)

    def test_011_log_in_user_with_eur_currency(self):
        """
        DESCRIPTION: Log in user with **EUR** currency
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=tests.settings.user_with_euro_currency_and_card, async_close_dialogs=False)

    def test_012_repeat_steps_2_10(self):
        """
        DESCRIPTION: Repeat steps #2-10
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        self.test_002_add_one_selection_to_the_betslip()
        self.test_003_go_to_betslip()
        self.test_004_verify_currency_symbol_next_to_the_est_returns_value(currency='€')
        self.test_005_verify_currency_symbol_next_to_the_total_stake_and_total_est_returns_values(currency='€')
        self.test_006_add_two_or_more_selections_from_different_events_to_the_bet_slip()
        self.test_007_verify_currency_symbol_within_quick_stake_buttons_on_the_numeric_keyboard(currency='€')
        self.test_008_go_to_bet_slip_multiples_section()
        self.test_009_repeat_steps_4_5(currency='€')
        self.test_010_tap_logout_menu_item()

    def test_015_log_in_user_with_usd_currency(self):
        """
        DESCRIPTION: Log in user with **USD** currency
        EXPECTED: User is logged out successfully
        """
        self.site.login(username=tests.settings.user_with_usd_currency_and_card, async_close_dialogs=False)

    def test_016_repeat_steps_2_10(self):
        """
        DESCRIPTION: Repeat steps #2-10
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        self.test_002_add_one_selection_to_the_betslip()
        self.test_003_go_to_betslip()
        self.test_004_verify_currency_symbol_next_to_the_est_returns_value(currency='$')
        self.test_005_verify_currency_symbol_next_to_the_total_stake_and_total_est_returns_values(currency='$')
        self.test_006_add_two_or_more_selections_from_different_events_to_the_bet_slip()
        self.test_007_verify_currency_symbol_within_quick_stake_buttons_on_the_numeric_keyboard(currency='$')
        self.test_008_go_to_bet_slip_multiples_section()
        self.test_009_repeat_steps_4_5(currency='$')
        self.test_010_tap_logout_menu_item()
