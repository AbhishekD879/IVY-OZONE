import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from random import choice
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.event_details
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.bet_history
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C35238873_Price_Formats(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C35238873
    NAME: Price Formats
    DESCRIPTION: This test case verifies price format across the application according to selected option Decimal or Fractional
    """
    keep_browser_open = True
    bet_filter_cms_status = False
    decimal_checked = {'homepage_checked': None,
                       'sport_landing_page_checked': None,
                       'event_details_page_checked': None,
                       'betslip_checked': None,
                       'bet_receipt_checked': None,
                       'cashout_checked': None
                       }
    fractional_checked = {'homepage_checked': None,
                          'sport_landing_page_checked': None,
                          'event_details_page_checked': None,
                          'betslip_checked': None,
                          'bet_receipt_checked': None,
                          'cashout_checked': None
                          }

    def check_odds(self, events, expected_odds_format):
        checked = None
        for event_name, event in events.items():
            outcomes = event.get_all_prices()
            if not outcomes:
                continue
            for outcome_name, outcome in outcomes.items():
                if outcome is not None:
                    checked = self.check_odds_format(outcome.outcome_price_text, expected_odds_format=expected_odds_format, raise_exceptions=False)
                break
        return checked

    def create_or_find_events(self):
        if tests.settings.backend_env == 'prod':
            found_events = []
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

            events = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id,
                all_available_events=True,
                additional_filters=cashout_filter)

            for event in events:
                if len(found_events) >= 1:
                    break
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                if not match_result_market:
                    continue
                outcomes = match_result_market['children']
                team = next((outcome['outcome']['name'] for outcome in outcomes if
                             outcome.get('outcome', {}).get('outcomeMeaningMinorCode', '') == 'H'), None)
                if not team:
                    continue

                selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                if not selection_ids:
                    continue

                self.__class__.eventID = event['event']['id']
                found_events.append(self.eventID)
                self.__class__.selection_id = list(selection_ids.values())[0]
                self.__class__.event_name = normalize_name(event['event']['name'])

            self._logger.info(f'*** Found Football event "{self.event_name}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.eventID = event.event_id
            self.__class__.selection_id = list(event.selection_ids.values())[0]

            self._logger.info(f'*** Created Football event "{self.event_name}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event to verify price format
        """
        cms_config = self.get_initial_data_system_configuration().get('BetFilterHorseRacing', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
        if cms_config.get('enabled'):
            self.__class__.bet_filter_cms_status = True

        self.__class__.sport_name = 'Football' if self.brand == 'bma' else 'FOOTBALL'
        self.create_or_find_events()

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_click_on_user_account_icon_on_header_settings_betting_setting(self, odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC):
        """
        DESCRIPTION: Click on [User account] icon on Header > Settings > Betting Setting
        EXPECTED: Preference page is opened
        """
        # TODO revert once VANO-768 will be resolved
        format_changed = self.site.change_odds_format(odds_format=odds_format)
        self.assertTrue(format_changed,
                        msg=f'"{odds_format}" option is not active after selection')
        # TODO uncomment once VANO-768 will be resolved
        # settings = self.site.window_client_config.settings_menu_title
        # betting_setting = self.site.window_client_config.betting_settings_menu_title
        #
        # self.site.navigate_to_my_account_page(name=settings)
        # self.site.right_menu.click_item(item_name=betting_setting)

    def test_003_select_decimal(self):
        """
        DESCRIPTION: Select "Decimal"
        """
        # TODO uncomment once VANO-768 will be resolved
        # self.site.settings.decimal_btn.click()
        # self.assertTrue(self.site.settings.decimal_btn.is_selected(),
        #                 msg='Decimal option is not active after selection')

    def test_004_navigate_through_the_application_and_make_sure_prices_are_displayed_according_to_selected_format(
            self, expected_odds_format=None):
        """
        DESCRIPTION: Navigate through the application and make sure prices are displayed according to selected format
        EXPECTED: Prices are displayed according to selected format on:
        EXPECTED: - Homepage
        EXPECTED: - Sports/Races Landing pages
        EXPECTED: - Sport/Races Details pages
        EXPECTED: - Betslip
        EXPECTED: - Cash Out
        EXPECTED: - Bet History
        EXPECTED: - Horse Race -> BetFilter -> Bet Filter Results
        """
        expected_odds_format = expected_odds_format if expected_odds_format else 'decimal'

        # home page
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')
        if self.device_type == 'desktop':
            events = self.site.home.desktop_modules.inplay_live_stream_module.tab_content.get_events(number_of_events=10)
            if expected_odds_format == 'decimal':
                self.decimal_checked['homepage_checked'] = self.check_odds(events=events, expected_odds_format=expected_odds_format)
            else:
                self.fractional_checked['homepage_checked'] = self.check_odds(events=events, expected_odds_format=expected_odds_format)
        else:
            self.site.close_all_dialogs()
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict['IN-PLAY'].click()
            sport_name, sport = list(self.site.home.tab_content.live_now.items_as_ordered_dict.items())[0]
            for comp_name, comp in list(sport.items_as_ordered_dict.items()):
                events = comp.items_as_ordered_dict
                for event_name, event in events.items():
                    outcomes = event.get_all_prices()
                    if not outcomes:
                        continue
                    for outcome_name, outcome in outcomes.items():
                        if outcome is not None:
                            checked = self.check_odds_format(outcome.outcome_price_text, expected_odds_format=expected_odds_format,
                                                             raise_exceptions=False)
                            break
            if expected_odds_format == 'decimal':
                self.decimal_checked['homepage_checked'] = checked
            else:
                self.fractional_checked['homepage_checked'] = checked

        # sport landing page
        self.site.open_sport(name=self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)

        matches_tab = self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                              category_id=self.ob_config.football_config.category_id)

        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, matches_tab,
                         msg=f'"{matches_tab}" tab is not active, active is "{active_tab}"')

        events = self.site.football.tab_content.get_events(number_of_events=10)
        if expected_odds_format == 'decimal':
            self.decimal_checked['sport_landing_page_checked'] = self.check_odds(events=events,
                                                                                 expected_odds_format=expected_odds_format)
        else:
            self.fractional_checked['sport_landing_page_checked'] = self.check_odds(events=events,
                                                                                    expected_odds_format=expected_odds_format)

        # event details page
        self.navigate_to_edp(event_id=self.eventID, sport_name='sport/football')

        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg=f'No markets found')

        section = markets_list.get(list(markets_list.keys())[0])
        self.assertTrue(section, msg=f'Market "{list(markets_list.keys())[0]}" not found')

        outcomes = section.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes available for event "{self.event_name}"')

        event_details_page_checked = None
        for outcome_name, outcome in outcomes.items():
            event_details_page_checked = self.check_odds_format(outcome.output_price, expected_odds_format=expected_odds_format, raise_exceptions=False)
            if event_details_page_checked is not None:
                break
        if expected_odds_format == 'decimal':
            self.decimal_checked['event_details_page_checked'] = event_details_page_checked
        else:
            self.fractional_checked['event_details_page_checked'] = event_details_page_checked

        # betslip
        self.open_betslip_with_selections(selection_ids=self.selection_id)

        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

        stake_name, stake = list(singles_section.items())[0]
        odds = stake.odds
        self.assertTrue(odds, msg=f'Odds for "{stake_name}" is empty')
        betslip_checked = self.check_odds_format(odds, expected_odds_format=expected_odds_format, raise_exceptions=False)
        if expected_odds_format == 'decimal':
            self.decimal_checked['betslip_checked'] = betslip_checked
        else:
            self.fractional_checked['betslip_checked'] = betslip_checked
        self.__class__.expected_betslip_counter_value = 0

        # bet history
        self.place_single_bet(number_of_stakes=1)
        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed')

        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()

        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)

        for betleg_name, betleg in bet.items_as_ordered_dict.items():
            betreceipt_checked = self.check_odds_format(betleg.odds_value, expected_odds_format=expected_odds_format, raise_exceptions=False)
            if expected_odds_format == 'decimal':
                self.decimal_checked['bet_receipt_checked'] = betreceipt_checked
            else:
                self.fractional_checked['bet_receipt_checked'] = betreceipt_checked

        self.site.open_my_bets_cashout()

        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)

        for betleg_name, betleg in bet.items_as_ordered_dict.items():
            cashout_checked = self.check_odds_format(betleg.odds_value, expected_odds_format=expected_odds_format, raise_exceptions=False)
            if expected_odds_format == 'decimal':
                self.decimal_checked['cashout_checked'] = cashout_checked
            else:
                self.fractional_checked['cashout_checked'] = cashout_checked

        # bet filter
        if self.bet_filter_cms_status:
            self.navigate_to_page(name='horse-racing')
            self.site.wait_content_state(state_name='HorseRacing')

            self.site.horse_racing.bet_filter_link.click()
            self.site.wait_content_state(state_name='HorseRacingBetFilterPage')

            result = wait_for_result(lambda: vec.bet_finder.NO_SELECTION in self.site.horseracing_bet_filter.result_text,
                                     name=f'"{vec.bet_finder.NO_SELECTION}" in "{self.site.horseracing_bet_filter.result_text}"',
                                     timeout=5)
            if result:
                self._logger.warning(f'There is "{vec.bet_finder.NO_SELECTION}" ')
                return
            elif not self.site.horseracing_bet_filter.find_bets_button.is_enabled():
                filter_items_ui = self.site.horseracing_bet_filter.items_as_ordered_dict
                self.assertTrue(filter_items_ui, msg='No filters found')
                filter = choice(list(filter_items_ui.values()))
                filter.click()
                self.site.horseracing_bet_filter.find_bets_button.click()
            else:
                self.site.horseracing_bet_filter.find_bets_button.click()
            self.site.wait_content_state_changed()

            result = self.site.racing_bet_filter_results_page.items_as_ordered_dict
            self.assertTrue(result, msg=f'No Bet Filter results found on page')

            item = self.site.racing_bet_filter_results_page.items[0]
            bet_filter_checked = self.check_odds_format(item.odds.text, expected_odds_format=expected_odds_format, raise_exceptions=False)
            if expected_odds_format == 'decimal':
                self.decimal_checked['bet_filter_checked'] = bet_filter_checked
            else:
                self.fractional_checked['bet_filter_checked'] = bet_filter_checked
        else:
            self._logger.warning(f'*** Skipping bet filter verification as it is disabled in CMS')

    def test_005_repeat_step_2_and_select_fractional(self):
        """
        DESCRIPTION: Repeat step 2 and select "Fractional"
        """
        self.test_002_click_on_user_account_icon_on_header_settings_betting_setting(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        if self.site.cookie_banner:
            self.site.cookie_banner.ok_button.click()

        self.site.settings.fractional_btn.click()
        self.assertTrue(self.site.settings.fractional_btn.is_selected(),
                        msg='Fractional option is not active after selection')

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        """
        self.create_or_find_events()
        self.test_004_navigate_through_the_application_and_make_sure_prices_are_displayed_according_to_selected_format(
            expected_odds_format='fraction')

    def test_007_check_status_of_decimal_verification(self):
        """
        DESCRIPTION: Check all decimal verifications are pass
        """
        statuses_decimal = all((value for value in self.decimal_checked.values()))
        self._logger.info(f'Verification statuses for Decimal format: \n{self.fractional_checked}')
        self.softAssert(self.assertTrue, statuses_decimal,
                        msg=f'Decimal format verification status is not PASSED. Statuses are: {self.decimal_checked}')

    def test_008_check_status_of_fractional_verification(self):
        """
        DESCRIPTION: Check all fractional verifications are pass
        """
        statuses_fractional = all((value for value in self.fractional_checked.values()))
        self._logger.info(f'Verification statuses for Fractional format: \n{self.decimal_checked}')
        self.softAssert(self.assertTrue, statuses_fractional,
                        msg=f'Fractional format verification status is not PASSED. Statuses are: {self.fractional_checked}')
