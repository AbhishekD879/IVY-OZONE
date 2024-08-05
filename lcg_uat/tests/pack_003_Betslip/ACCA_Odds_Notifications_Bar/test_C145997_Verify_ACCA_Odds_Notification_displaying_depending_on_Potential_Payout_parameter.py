import pytest
import tests
import voltron.environments.constants as vec
from collections import OrderedDict
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C145997_Verify_ACCA_Odds_Notification_displaying_depending_on_Potential_Payout_parameter(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C145997
    NAME: Verify ACCA Odds Notification displaying depending on Potential Payout parameter
    DESCRIPTION: This test case verifies ACCA Odds Notification displaying depending on Potential Payout parameter when Multiples are available in the Betslip
    DESCRIPTION: Odds calculation on ACCA notification instruction: https://confluence.egalacoral.com/display/SPI/Odds+calculation+on+ACCA+notification
    PRECONDITIONS: - Application is loaded
    PRECONDITIONS: - Any <Sport> landing page is opened
    """
    keep_browser_open = True
    events = OrderedDict()

    def click_on_bet_buttons(self, deselect=False):
        events_values = list(self.events.values())

        event = self.get_event_from_league(event_id=events_values[0],
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices, msg=f'Could not find output prices for created event "{events_values[0]}"')
        name, price = list(output_prices.items())[0]
        price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)

        event2 = self.get_event_from_league(event_id=events_values[1],
                                            section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2, msg=f'Could not find output prices for created event "{events_values[1]}"')
        name2, price2 = list(output_prices2.items())[1]
        price2.click()
        if deselect:
            self.assertFalse(price2.is_selected(expected_result=False, timeout=2), msg=f'Price "{name2}" was not deselected after click')
        else:
            self.assertTrue(price2.is_selected(timeout=2), msg=f'Price "{name2}" was not selected after click')

    def verify_acca_notification(self):
        self.assertTrue(self.site.wait_for_acca_notification_present(expected_result=True),
                        msg='Acca notification is not displayed')
        acca = self.site.acca_notification
        self.assertTrue(acca.odds_value, msg='Odds text is not displayed in Acca notification')
        odds = self.site.acca_notification.odds_value
        self.assertRegexpMatches(odds, self.acca_fractional_pattern,
                                 msg=f'Odds format "{odds}" not matching pattern "{self.acca_fractional_pattern}"')
        # self.assertTrue(acca.arrow.is_displayed(), msg='An arrow is not displayed in Acca notification')
        self.assertEqual(acca.bet_type, vec.betslip.DBL,
                         msg=f'Bet Type "{acca.bet_type}" is not the same as expected "{vec.betslip.DBL}"')

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
            football_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id, number_of_events=2)
            # event 1
            self.__class__.created_event_name = football_events[0]['event']['name']
            event_id = football_events[0]['event']['id']
            self.events[self.created_event_name] = event_id
            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=football_events[0])

            # event 2
            self.__class__.created_event2_name = football_events[1]['event']['name']
            event2_id = football_events[1]['event']['id']
            self.events[self.created_event2_name] = event2_id
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=football_events[1])

            # racing
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'LP'))
            racing_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                                additional_filters=additional_filter,
                                                                all_available_events=True)
            self.__class__.eventID1 = self.find_lp_hr_events(racing_events)['event']['id']
            self.__class__.eventID2 = self.find_lp_hr_events(racing_events)['event']['id']

        else:
            # football
            for i in range(0, 2):
                event_params = self.ob_config.add_autotest_premier_league_football_event()
                self.events[f'{event_params.team1} v {event_params.team2}'] = event_params.event_id
            self.assertTrue(len(self.events.items()) == 2,
                            msg=f'Actual number of created events {len(self.events.items())} is not the same as expected 2')
            self.__class__.league1 = self.__class__.league2 = tests.settings.football_autotest_league
            # racing
            prices = {0: '1/2', 1: '2/3'}

            event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=prices)
            self.__class__.eventID1 = event_params1.event_id
            self._logger.info(f'*** Racing event id: {self.eventID1}')

            event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=prices)
            self.__class__.eventID2 = event_params2.event_id

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        EXPECTED: * Odds value is shown:
        EXPECTED: a) For Double (1 Bets) in Multiples section
        EXPECTED: b) In case of more than 2 selections in 'Place your ACCA' section
        """
        self.click_on_bet_buttons()
        self.verify_acca_notification()

    def test_002_verify_that_potential_payout_parameter_from_the_buildbet_response_is_displayed_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Verify that potential payout parameter from the buildBet response is displayed on ACCA Odds Notification message
        EXPECTED: Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds
        """
        # TODO cannot check payout from response from buildBet request
        if self.brand == 'ladbrokes':
            payout = self.site.acca_notification.payout
            self.assertTrue(payout, msg='Payout string is empty')

    def test_003_repeat_steps_1_2_for_races_lp_price_type_only(self):
        """
        DESCRIPTION: Repeat steps 1-2 for Races (LP price type only)
        EXPECTED:
        """
        self.click_on_bet_buttons(deselect=True)  # deselect sports selections
        try:
            self.navigate_to_edp(event_id=self.eventID1, sport_name='horse-racing', timeout=5)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RacingEventDetails')
        # Win or each way tab is not displaying by default sometimes
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.add_selection_to_quick_bet()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        try:
            self.navigate_to_edp(event_id=self.eventID2, sport_name='horse-racing', timeout=5)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RacingEventDetails')
        # Win or each way tab is not displaying by default sometimes
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')

        outcome = list(outcomes.values())[0]
        outcome.bet_button.click()

        self.verify_acca_notification()
        self.test_002_verify_that_potential_payout_parameter_from_the_buildbet_response_is_displayed_on_acca_odds_notification_message()
