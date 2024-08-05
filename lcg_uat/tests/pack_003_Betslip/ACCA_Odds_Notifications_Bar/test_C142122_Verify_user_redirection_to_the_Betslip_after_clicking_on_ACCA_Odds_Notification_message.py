import pytest
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.acca
@pytest.mark.betslip
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
class Test_C142122_Verify_user_redirection_to_the_Betslip_after_clicking_on_ACCA_Odds_Notification_message(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C142122
    VOL_ID: C9690002
    NAME: Verify user redirection to the Betslip after clicking on ACCA Odds Notification message (Mobile)
    DESCRIPTION: This test case verifies user redirection to the Betslip after clicking on
    DESCRIPTION: ACCA Odds Notification message (Mobile)
    PRECONDITIONS: - Application is loaded
    PRECONDITIONS: - There are <Sport> events and <Race> events with LP prices
    """
    keep_browser_open = True
    league = tests.settings.football_autotest_league
    prices = {0: '1/2', 1: '2/3'}
    events = {}

    def find_lp_hr_events(self, events):
        for event in events:
            market = next((market for market in event['event']['children']
                           if market['market']['templateMarketName'] == 'Win or Each Way'), None)
            if not market:
                continue
            outcomes_resp = market['market']['children']
            for outcome in outcomes_resp:
                if outcome['outcome'].get('children'):
                    for child in outcome['outcome']['children']:
                        if child.get('price'):
                            if 'LP' in child.get('price').get('priceType'):
                                events.remove(event)
                                return event
                    break
        raise SiteServeException('There are no selections with LP prices')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create Football and Racing LP events, PROD: Find Football and Racing events
        """
        if tests.settings.backend_env == 'prod':
            # football
            football_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                                  number_of_events=3)
            # event 1
            self.__class__.created_event_name = normalize_name(football_events[0]['event']['name'])
            event_id = football_events[0]['event']['id']
            self.events[self.created_event_name] = event_id
            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=football_events[0])
            self._logger.info(f'*** Found Football event "{self.created_event_name}" with id "{event_id}", league "{self.league1}"')

            # event 2
            self.__class__.created_event2_name = normalize_name(football_events[1]['event']['name'])
            event2_id = football_events[1]['event']['id']
            self.events[self.created_event2_name] = event2_id
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=football_events[1])
            self._logger.info(
                f'*** Found Football event "{self.created_event2_name}" with id "{event2_id}", league "{self.league2}"')

            # event 3
            self.__class__.created_event3_name = normalize_name(football_events[2]['event']['name'])
            event3_id = football_events[2]['event']['id']
            self.events[self.created_event3_name] = event3_id
            self.__class__.league3 = self.get_accordion_name_for_event_from_ss(event=football_events[2])
            self._logger.info(
                f'*** Found Football event "{self.created_event3_name}" with id "{event3_id}", league "{self.league3}"')

            # racing
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'LP'))
            racing_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                                additional_filters=additional_filter,
                                                                all_available_events=True)
            self.__class__.eventID1 = self.find_lp_hr_events(racing_events)['event']['id']
            self._logger.info(f'*** Found Racing event id: {self.eventID1}')

            self.__class__.eventID2 = self.find_lp_hr_events(racing_events)['event']['id']
            self._logger.info(f'*** Found Racing event2 id: {self.eventID2}')
        else:
            # football
            for i in range(0, 3):
                event_params = self.ob_config.add_autotest_premier_league_football_event()
                self.events[f'{event_params.team1} v {event_params.team2}'] = event_params.event_id
            self.assertTrue(len(self.events.items()) == 3,
                            msg=f'Actual number of created events {len(self.events.items())} '
                            f'is not the same as expected 3')
            self.__class__.league1 = self.__class__.league2 = self.__class__.league3 = tests.settings.football_autotest_league

            # racing
            prices = {0: '1/2', 1: '2/3'}
            event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=prices)
            self.__class__.eventID1 = event_params1.event_id
            self._logger.info(f'*** Racing event id: {self.eventID1}')

            event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=prices)
            self.__class__.eventID2 = event_params2.event_id
            self._logger.info(f'*** Racing event2 id: {self.eventID2}')

    def test_001_open_sport_landing_page(self):
        """
        DESCRIPTION: Open <Sport> Landing page
        EXPECTED: <Sport> Landing page is shown
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_002_add_two_selections_from_different_sport_events_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections from different <Sport> events to the Betslip
        EXPECTED: * ACCA Odds Notification message appears (yellow bar)
        """
        events_values = list(self.events.values())

        event = self.get_event_from_league(event_id=events_values[0],
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(all(output_prices), msg=f'Could not find output prices for event "{events_values[0]}"')
        name, price = list(output_prices.items())[0]
        price.scroll_to()
        price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=10)

        event2 = self.get_event_from_league(event_id=events_values[1],
                                            section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(all(output_prices2), msg=f'Could not find output prices for event "{events_values[1]}"')
        name2, price2 = list(output_prices2.items())[1]
        price2.scroll_to()
        price2.click()
        self.assertTrue(price2.is_selected(timeout=2), msg=f'Price "{name2}" was not selected after click')

    def test_003_tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Tap on ACCA Odds Notification message
        EXPECTED: * User is redirected to the Betslip
        EXPECTED: * Betslip is scrolled up so relevant Multiple is visible for the User  # cannot check, all sections are autoscrolled
        """
        self.site.acca_notification.click()
        self.assertTrue(self.get_betslip_content(), msg='Betslip is not opened')

    def test_004_add_more_selections_from_different_sport_events_to_the_betslip_and_tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Add more selections from different <Sport> events to the Betslip
        DESCRIPTION: Tap on ACCA Odds Notification message
        EXPECTED: * User is redirected to the Betslip
        EXPECTED: * Betslip is scrolled up so relevant Multiple is visible for the User  # cannot check, all sections are autoscrolled
        """
        self.site.close_betslip()
        self.assertFalse(self.site.has_betslip_opened(expected_result=False),
                         msg='Betslip is not closed')
        events_values = list(self.events.values())

        event3 = self.get_event_from_league(event_id=events_values[2],
                                            section_name=self.league3)
        output_prices3 = event3.get_active_prices()

        name3, price3 = list(output_prices3.items())[1]
        price3.click()
        self.assertTrue(price3.is_selected(timeout=2), msg=f'Price "{name3}" was not selected after click')
        self.site.acca_notification.click()
        self.assertTrue(self.get_betslip_content(), msg='Betslip is not opened')

    def test_005_repeat_steps_1_3_for_race_events_with_lp_selections(self):
        """
        DESCRIPTION: Repeat steps 1-3 for <Race> events with LP selections
        """
        self.clear_betslip()
        self.navigate_to_edp(event_id=self.eventID1, sport_name='horse-racing')
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.add_selection_to_quick_bet()
        if self.site.wait_for_quick_bet_panel(timeout=2):
            self.site.quick_bet_panel.add_to_betslip_button.click()
            sleep(2)
            self.site.wait_for_quick_bet_panel(expected_result=False, timeout=5)
            self.site.wait_quick_bet_overlay_to_hide()
        self.navigate_to_edp(event_id=self.eventID2, sport_name='horse-racing')
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        outcome = list(outcomes.values())[0]
        outcome.bet_button.click()
        self.site.acca_notification.wait_for_odds_change()
        self.site.acca_notification.click()
        self.assertTrue(self.get_betslip_content(), msg='Betslip is not opened')
