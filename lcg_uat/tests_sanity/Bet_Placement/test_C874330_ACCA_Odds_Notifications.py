import pytest
import tests
import voltron.environments.constants as vec
from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.voltron_exception import VoltronException
from random import choice
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.in_play
@pytest.mark.homepage
@pytest.mark.mobile_only
@pytest.mark.safari
@pytest.mark.sanity
@vtest
class Test_C874330_ACCA_Odds_Notifications(BaseBetSlipTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C874330
    VOL_ID: C48981671
    NAME: ACCA Odds Notifications
    DESCRIPTION: This test case verifies ACCA Odds Notification displaying after adding selections to the Betslip
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL
    racing_event_id1 = None
    racing_event_id2 = None

    def find_create_live_events(self):
        # football in play
        live_event_params1 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.live_event_name1 = f'{live_event_params1.team1} v {live_event_params1.team2}'
        self.__class__.live_event_id1 = live_event_params1.event_id

        live_event_params2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.live_event_name2 = f'{live_event_params2.team1} v {live_event_params2.team2}'
        self.__class__.live_event_id2 = live_event_params2.event_id

        self.__class__.live_league1 = self.__class__.live_league2 = \
            tests.settings.football_autotest_competition_league
        self.__class__.live_league1_homepage = self.__class__.live_league2_homepage = \
            tests.settings.football_autotest_competition_league if self.brand == 'ladbrokes' else \
            tests.settings.football_autotest_competition_league.title()

        self._logger.info(f'*** Created Football event #1 "{self.live_event_name1}" '
                          f'with ID "{self.live_event_id1}", league "{self.live_league1}"')
        self._logger.info(f'*** Created Football event #2 "{self.live_event_name2}" '
                          f'with ID "{self.live_event_id2}", league "{self.live_league2}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create Football events, PROD: Find Football events
        """
        number_of_events = 2
        self.__class__.sport_name = self.sport_name
        if tests.settings.backend_env == 'prod':
            # racing
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP'))
            racing_events = self.get_active_events_for_category(
                category_id=self.ob_config.horseracing_config.category_id,
                additional_filters=additional_filter,
                all_available_events=True)
            self.__class__.racing_event_id1 = None
            for event in racing_events:
                market = next((market for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Win or Each Way' and
                               market['market'].get('children')), None)
                if not market:
                    continue
                outcomes_resp = market['market']['children']
                for outcome in outcomes_resp:
                    for child in outcome.get('outcome', {}).get('children', []):
                        if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                            self.__class__.racing_event_id1 = event['event']['id']
                            racing_events.remove(event)
                            break
                    if self.racing_event_id1:
                        break
                if self.racing_event_id1:
                    break

            if not self.racing_event_id1:
                raise SiteServeException('There are no selections with LP prices')
            self._logger.info(f'*** Found Racing event #1 with ID: {self.racing_event_id1}')

            self.__class__.racing_event_id2 = None
            for event in racing_events:
                market = next((market for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Win or Each Way' and
                               market['market'].get('children')), None)
                if not market:
                    continue
                outcomes_resp = market['market']['children']
                for outcome in outcomes_resp:
                    for child in outcome.get('outcome', {}).get('children', []):
                        if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                            self.__class__.racing_event_id2 = event['event']['id']
                            racing_events.remove(event)
                            break
                    if self.racing_event_id2:
                        break
                if self.racing_event_id2:
                    break

            if not self.racing_event_id2:
                raise SiteServeException('There are no selections with LP prices')
            self._logger.info(f'*** Found Racing event #2 with ID: {self.racing_event_id2}')

            # football
            # setting start_date this is needed because start date in BaseRacing add +1h delta, which breaks finding live events on Football
            self.__class__.start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
            football_events = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id,
                number_of_events=number_of_events)

            self.__class__.event_name1 = normalize_name(football_events[0]['event']['name'])
            self.__class__.event_id1 = football_events[0]['event']['id']
            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=football_events[0])
            self._logger.info(
                f'*** Found Football event #1 "{self.event_name1}" '
                f'with ID "{self.event_id1}", league "{self.league1}"')

            self.__class__.event_name2 = normalize_name(football_events[1]['event']['name'])
            self.__class__.event_id2 = football_events[1]['event']['id']
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=football_events[1])
            self._logger.info(
                f'*** Found Football event #2 "{self.event_name2}" '
                f'with ID "{self.event_id2}", league "{self.league2}"')
        else:
            # football
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name1 = f'{event_params1.team1} v {event_params1.team2}'
            self.__class__.event_id1 = event_params1.event_id

            event_params2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name2 = f'{event_params2.team1} v {event_params2.team2}'
            self.__class__.event_id2 = event_params2.event_id

            self.__class__.league1 = self.__class__.league2 = tests.settings.football_autotest_league

            self._logger.info(f'*** Created Football event #1 "{self.event_name1}" '
                              f'with ID "{self.event_id1}", league "{self.league1}"')
            self._logger.info(f'*** Created Football event #2 "{self.event_name2}" '
                              f'with ID "{self.event_id2}", league "{self.league2}"')
            # racing
            lp_prices = {0: '1/2', 1: '2/3'}

            event_params1 = self.ob_config.add_UK_racing_event(
                number_of_runners=2, time_to_start=1, lp_prices=lp_prices)
            self.__class__.racing_event_id1 = event_params1.event_id
            self._logger.info(f'*** Created Racing event #1 with ID: {self.racing_event_id1}')

            event_params2 = self.ob_config.add_UK_racing_event(
                number_of_runners=2, time_to_start=1, lp_prices=lp_prices)
            self.__class__.racing_event_id2 = event_params2.event_id
            self._logger.info(f'*** Created Racing event #2 with ID: {self.racing_event_id2}')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_go_to_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports Landing page
        EXPECTED: Sports Landing page is opened
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state_changed(timeout=20)

    def test_003_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: ACCA Odds Notification appears
        """
        event1 = self.get_event_from_league(event_id=self.event_id1,
                                            section_name=self.league1)
        output_prices = event1.get_active_prices()

        self.assertTrue(output_prices, msg=f'Could not find output prices for event "{self.event_name1}"')

        price_name, price = choice(list(output_prices.items()))
        price.click()
        self._logger.info(f'*** Clicking on "{price_name}" bet button from event "{self.event_name1}')
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(price.is_selected(), msg=f'"{price_name}" is not selected')

        event2 = self.get_event_from_league(event_id=self.event_id2,
                                            section_name=self.league2)
        output_prices = event2.get_active_prices()

        self.assertTrue(output_prices, msg=f'Could not find output prices for event "{self.event_name2}"')

        price2_name, price2 = choice(list(output_prices.items()))
        price2.click()
        self._logger.info(f'*** Clicking on "{price2_name}" bet button from event "{self.event_name2}')
        acc_odds_notification_status = self.site.wait_for_acca_notification_present(expected_result=True)
        self.assertTrue(acc_odds_notification_status, f'ACCA Odds notification not displayed')

    def test_004_verify_acca_odds_notification_content(self):
        """
        DESCRIPTION: Verify ACCA Odds Notification content
        EXPECTED: ACCA Odds Notification contains the following information:
        EXPECTED: * Multiples name (Double, Treble, Accumulator (4), etc.) and Odds are displayed
        EXPECTED: * The odds are displayed in fractional format as default for logged OUT in user
        EXPECTED: * The odds are displayed in appropriate format depending on user preference i.e. decimal / fractional for logged IN user
        EXPECTED: * An arrow is displayed to the right of the message bar for mobile only
        """
        acca_notification = self.site.acca_notification
        self.assertEqual(acca_notification.bet_type, vec.betslip.DBL,
                         msg=f'ActualBet Type "{acca_notification.bet_type}" '
                             f'is not the same as expected "{vec.betslip.DBL}"')
        odds_value = acca_notification.payout.split(' @ ')[1]
        self.assertRegexpMatches(odds_value, self.acca_fractional_pattern,
                                 msg=f'Actual odds format: "{odds_value}" '
                                     f'is not as expected: "{self.acca_fractional_pattern}"')

    def test_005_verify_potential_payout(self):
        """
        DESCRIPTION: Verify potential payout
        EXPECTED: Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds
        """
        self._logger.info('*** Cannot check payout from response from buildBet request')
        if self.brand == 'ladbrokes':
            potential_payout = self.site.acca_notification.payout.split(' @ ')[0]
            self.assertTrue(potential_payout, msg='Payout string is empty')

    def test_006_click_or_tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Click/Tap on ACCA Odds Notification message
        EXPECTED: User is redirected to the Betslip
        EXPECTED: User is focused directly on the relevant input field
        """
        self.site.acca_notification.click()
        sleep(1)
        self.assertTrue(self.get_betslip_content(), msg='Betslip is not opened')

        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake_name, stake = list(multiples_section.items())[0]
        self.assertTrue(stake.amount_form.input, msg=f'Input for "{stake_name}" is not displayed')

        self.clear_betslip()

    def test_007_repeat_steps_2_6_for_races_lp_price_type_only(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Races (LP price type only)
        """
        self.navigate_to_edp(event_id=self.racing_event_id1, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)

        self.add_selection_to_quick_bet()
        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.navigate_to_edp(event_id=self.racing_event_id2, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)

        selections = self.get_edp_market_selections(market_name=vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

        selection = list(selections.values())[0]
        selection.bet_button.click()
        sleep(2)
        result = self.site.wait_for_acca_notification_present(expected_result=True)
        self.assertTrue(result or self.site.betslip_notification, msg=f'Acca Odds notification has not appeared')

        self.test_004_verify_acca_odds_notification_content()
        self.test_005_verify_potential_payout()
        self.test_006_click_or_tap_on_acca_odds_notification_message()

    def test_008_repeat_steps_3_6_on_homepage(self):
        """
        DESCRIPTION: Repeat steps 3-6 on Homepage
        """
        if tests.settings.backend_env != 'prod':
            self.find_create_live_events()
        self.navigate_to_page(name='home/in-play')
        self.site.wait_content_state(state_name='Homepage')
        sports = self.site.home.tab_content.live_now.items_as_ordered_dict
        count = 0
        for sport_name, sport in sports.items():
            if not sport.is_expanded(timeout=2):
                sport.expand()
            leagues = sport.items_as_ordered_dict
            for league_name, league in leagues.items():
                if not league.is_expanded(timeout=2):
                    league.expand()
                events = league.items_as_ordered_dict
                for event_name, event in events.items():
                    prices = event.template.get_active_prices()
                    for price in list(prices.values()):
                        if price.is_enabled():
                            price.click()
                            sleep(1)
                            if count == 0:
                                self.site.add_first_selection_from_quick_bet_to_betslip()
                            count += 1
                            break
                    if count == 2:
                        break
                if count == 2:
                    break
            if count == 2:
                break
        if count != 2:
            raise VoltronException(f'cannot find more than "{count}"  event')
        sleep(2)
        result = self.site.wait_for_acca_notification_present(expected_result=True)
        self.assertTrue(result or self.site.betslip_notification, msg=f'Acca Odds notification has not appeared')

        self.test_004_verify_acca_odds_notification_content()
        self.test_005_verify_potential_payout()
        self.test_006_click_or_tap_on_acca_odds_notification_message()

    def test_009_repeat_steps_3_6_on_in_play_page(self):
        """
        DESCRIPTION: Repeat steps 3-6 on In-Play page
        """
        self.__class__.count = 0

        def select_prices(leagues):
            for league_name, league in leagues.items():
                if not league.is_expanded(timeout=2):
                    league.expand()
                events = list(league.items_as_ordered_dict.values())
                for event in events:
                    prices = event.get_active_prices()
                    for price in list(prices.values()):
                        if price.is_enabled():
                            price.click()
                            if self.count == 0:
                                self.site.add_first_selection_from_quick_bet_to_betslip()
                            self.count += 1
                            break
                    if self.count == 2:
                        break
                if self.count == 2:
                    break

        if tests.settings.backend_env != 'prod':
            self.find_create_live_events()
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        in_play_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        self.assertTrue(in_play_events, msg='No inplay events found')
        select_prices(leagues=in_play_events)
        if self.count != 2:
            upcoming_events = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
            self.assertTrue(upcoming_events, msg='No upcoming events found')
            select_prices(leagues=upcoming_events)
        self.test_004_verify_acca_odds_notification_content()
        self.test_005_verify_potential_payout()
        self.test_006_click_or_tap_on_acca_odds_notification_message()