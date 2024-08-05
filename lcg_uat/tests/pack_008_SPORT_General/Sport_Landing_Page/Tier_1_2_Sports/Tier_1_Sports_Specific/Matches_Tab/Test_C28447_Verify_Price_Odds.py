import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28447_Verify_Price_Odds(BaseBetSlipTest):
    """
    TR_ID: C28447
    NAME: Verify Price/Odds
    DESCRIPTION: This test case verifies Price/Odds buttons of event.
    DESCRIPTION: Need to run the tesVerify Odds/Price display for Suspended Markets/Selectionst case on Mobile/Tablet/Desktop.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * For DESKTOP: 'Price/Odds' button size depends on screen resolution (see https://ladbrokescoral.testrail.com/index.php?/cases/view/1474609 test case).
    """
    keep_browser_open = True
    currency = '£'

    def verify_price_odd_format(self, format=None):

        self.get_price_button_values()
        for selection_name, price_button in self.price_buttons:

            if price_button is not None:
                if format == 'fractional':
                    self.assertRegexpMatches(price_button.name, self.fractional_pattern,
                                             msg=f'Stake odds value "{price_button.name}" not match decimal pattern: "{self.fractional_pattern}"')
                else:
                    if format == 'decimal':
                        self.assertRegexpMatches(price_button.name, self.decimal_pattern,
                                                 msg=f'Stake odds value "{price_button.name}"not match decimal pattern: "{self.decimal_pattern}"')

        self.ob_config.change_market_state(self.event_id, self.market_id, displayed=True)

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')
        self.get_price_button_values()

        for selection_name, price_button in self.price_buttons:
            if price_button is not None:
                self.assertFalse(price_button.is_enabled(expected_result=False, timeout=30, poll_interval=1),
                                 msg='Bet button is not disabled, but was expected to be disabled')

        self.ob_config.change_market_state(self.event_id, self.market_id, displayed=True, active=True)

    def get_price_button_values(self):

        event_name = self.event.team1 + ' v ' + self.event.team2
        league_name = self.get_accordion_name_for_event_from_ss(event=self.event_resp[0])
        event = self.site.sports_page.tab_content.accordions_list.get_event_from_league_by_event_id(league=league_name,
                                                                                                    event_id=self.event_id)
        self.assertTrue(event, msg=f'Event with name "{event_name}" not found')
        self.__class__.price_buttons = list(event.get_all_prices().items())
        self.assertTrue(self.price_buttons, msg='Price buttons are not displayed')

    def test_000_pre_conditions(self):

        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = self.event.event_id
        self.__class__.market_id = self.event.default_market_id
        self.__class__.selection_name = self.__class__.selection_name = self.event.team1
        self.__class__.event_name = self.__class__.event.team1 + ' v ' + self.__class__.event.team2
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id,
                                                                              query_builder=self.ss_query_builder)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.assertTrue(self.site.wait_content_state('homepage'), msg='User has not re-directed to homepage')
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page
        EXPECTED: *Desktop*:
        EXPECTED: *    <Sport> Landing Page is opened
        EXPECTED: *   'Matches'->'Today' sub tab is opened by default
        EXPECTED: *Mobile*:
        EXPECTED: *    <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is opened by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current
        matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                   self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, matches_tab_name,
                         msg=f'Current active tab: "{current_tab_name}", instead of "{matches_tab_name}"')

    def test_003_verify_data_of_priceodds_for_verified_event_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **<price>** button is displayed instead of prices if **eventStatusCode="S"**
        """
        self.verify_price_odd_format(format='fractional')

    def test_004_verify_data_of_priceodds_for_verified_event_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **<price>** button is displayed instead of prices if **eventStatusCode="S"**
        """
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')
        self.verify_price_odd_format(format='decimal')

    def test_005_add_selection_to_the_betslip_from_sport_landing_page(self):
        """
        DESCRIPTION: Add selection to the Betslip from <Sport> Landing Page
        EXPECTED: Bet indicator displays 1.
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')
        self.get_price_button_values()
        self.price_buttons[0][1].click()
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel(timeout=20)
            self.site.quick_bet_panel.header.close_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')
        self.verify_betslip_counter_change(expected_value=1)

    def test_006_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertEqual(self.stake_name, self.selection_name,
                         msg=f'Selection "{self.selection_name}" should be present in betslip')
        self.assertEqual(len(singles_section.items()), 1,
                         msg='Only one selection should be present in betslip')
        event_name = self.stake.event_name
        self.assertEqual(event_name, self.event_name,
                         msg=f'Selection name "{event_name}" is not the same as expected "{self.event_name}"')

        odd = self.stake.odds
        self.__class__.odd = \
            self.event_resp[0]['event']['children'][0]['market']['children'][0]['outcome']['children'][0]['price'][
                'priceDec']
        self.assertEqual(odd, self.odd, msg=f'Market name "{odd}" is not the same as expected "{self.odd}"')
        est_returns = self.stake.est_returns
        expected_est_returns = '£0.00'
        self.assertEqual(self.currency + str(est_returns), expected_est_returns, msg='Est. Returns field: "%s" is not as expected: "%s"' %
                                                                                     (self.currency + str(est_returns), expected_est_returns))
        total_stake = self.get_betslip_content().total_stake
        self.assertEqual(self.currency + str(total_stake), expected_est_returns, msg='Totals Stake value: "%s" is not as expected: "%s"' %
                                                                                     (self.currency + str(total_stake), expected_est_returns))

    def test_007_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        user_balance = self.site.header.user_balance
        self.place_single_bet()
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=0.5)
        expected_user_balance = user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=float(expected_user_balance), timeout=10)
