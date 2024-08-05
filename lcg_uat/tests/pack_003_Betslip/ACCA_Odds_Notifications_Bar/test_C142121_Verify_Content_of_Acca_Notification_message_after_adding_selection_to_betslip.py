from collections import OrderedDict
import pytest
import re
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_journey_build_your_bet
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.back_button
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.timeout(800)
@pytest.mark.mobile_only
@vtest
class Test_C142121_Verify_Content_of_Acca_Notification_message_after_adding_selection_to_the_betslip(BaseBetSlipTest,
                                                                                                     BaseRacing):

    """
    TR_ID: C142121
    VOL_ID: C9697927
    NAME: Verify content of ACCA Odds Notification message after adding selections to the Betslip
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
        try:
            price2.click()
            if deselect:
                self.assertFalse(price2.is_selected(expected_result=False, timeout=2), msg=f'Price "{name2}" was not deselected after click')
            else:
                self.assertTrue(price2.is_selected(timeout=2), msg=f'Price "{name2}" was not selected after click')
        except Exception:
            price2.click()
            if deselect:
                self.assertFalse(price2.is_selected(expected_result=False, timeout=2), msg=f'Price "{name2}" was not deselected after click')
            else:
                self.assertTrue(price2.is_selected(timeout=2), msg=f'Price "{name2}" was not selected after click')
    def verify_acca_bar(self, decimal=False):

        self.assertTrue(self.site.has_betslip_notification(expected_result=True),
                        msg='ACCA Bar is not displayed')

        self.site.betslip_notification.click()
        sections = self.get_betslip_sections()
        singles_section, multiples_section = sections.Singles, sections.Multiples
        selection_names_list = singles_section.keys()
        expected_selection_names = ', '.join(selection_names_list)
        # Use regular expression to find all alphanumeric sequences
        output = re.findall(r'\w+', expected_selection_names)
        expected_selection_names = ' '.join(output)
        self.site.close_betslip()

        acca = self.site.betslip_notification

        self.assertEqual(acca.counter_value, '2', msg='counter value is not displayed in ACCA Bar')

        self.assertEqual(acca.bet_type, vec.betslip.DBL,
                         msg=f'Bet Type "{acca.bet_type}" is not the same as expected "{vec.betslip.DBL}"')

        self.assertTrue(acca.payout, msg='payout value is not displayed in ACCA Bar')

        odds = acca.odds_value
        self.assertTrue(odds, msg='Odds text is not displayed in ACCA Bar')
        if decimal:
            self.assertRegexpMatches(odds, self.decimal_pattern,
                                     msg=f'Odds format "{odds}" not matching pattern "{self.decimal_pattern}"')
        else:
            self.assertRegexpMatches(odds, self.acca_fractional_pattern,
                                     msg=f'Odds format "{odds}" not matching pattern "{self.acca_fractional_pattern}"')

        # Use regular expression to find all alphanumeric sequences
        output = re.findall(r'\w+', acca.selection_name)
        actual_selection_names = ' '.join(output)
        self.assertEqual(actual_selection_names, expected_selection_names, msg=f'selection name is not as expected in ACCA Bar, actual: "{actual_selection_names}" and expected "{expected_selection_names}"')

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
            self._logger.info(
                f'*** Found Football event "{self.created_event_name}" with id "{event_id}", league "{self.league1}"')
            # event 2
            self.__class__.created_event2_name = football_events[1]['event']['name']
            event2_id = football_events[1]['event']['id']
            self.events[self.created_event2_name] = event2_id
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=football_events[1])
            self._logger.info(
                f'*** Found Football event "{self.created_event2_name}" with id "{event2_id}", league "{self.league2}"')
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
            self._logger.info(f'*** Racing event2 id: {self.eventID2}')

    def test_001_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_add_at_least_two_selections_from_diff_events_to_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        """
        self.click_on_bet_buttons()

    def test_003_scroll_page_down_and_up(self):
        """
        DESCRIPTION: Scroll page down and up
        EXPECTED: ACCA Odds Notification message is sticky
        EXPECTED: ACCA Odds Notification message remains in the same place
        """
        pass  # cannot verify that it is sticky

    def test_004_verify_acca_odds_notification_content(self):
        """
        DESCRIPTION: Verify ACCA Odds Notification content
        EXPECTED: ACCA Odds Notification contains the following information:
        EXPECTED: * Multiples name (Double, Treble, Accumulator (4), etc.) and Odds are displayed
        EXPECTED: * The odds are displayed in fractional format as default for logged OUT in user
        EXPECTED: * The odds are displayed in appropriate format depending on user preference i.e. decimal/ fractional for logged IN user
        EXPECTED: * An arrow is displayed to the right of the message bar for mobile only
        """
        self.verify_acca_bar()
        self.site.login(async_close_dialogs=False, timeout_close_dialogs=5)
        self.site.change_odds_format(odds_format='DECIMAL')
        self.navigate_to_page(name='/sport/football')
        self.site.wait_content_state(state_name='Football')
        self.verify_acca_bar(decimal=True)

    def test_005_verify_potential_payout_parameter_from_buildBet_response(self):
        """
        DESCRIPTION: Verify that potential payout parameter from the buildBet response is displayed on ACCA Odds Notification message
        EXPECTED: Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds
        """
        # TODO cannot check payout from response from buildBet request
        if self.brand == 'ladbrokes':
            payout = self.site.betslip_notification.payout
            self.assertTrue(payout, msg='Payout string is empty')

    def test_006_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: The same are displayed on the Betslip near relevant Multiple
        """
        # TODO cannot check payout from response from buildBet request

    def test_007_repeat_steps_for_races_LP_only(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Races (LP price type only)
        """
        self.click_on_bet_buttons(deselect=True)  # deselect sports selections
        try:
            self.navigate_to_edp(event_id=self.eventID1, sport_name='horse-racing', timeout=5)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RacingEventDetails')

        if self.site.wait_for_stream_and_bet_overlay(timeout=5):
            self.site.stream_and_bet_overlay.close_button.click()

        win_or_eachway_tab = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.assertTrue(win_or_eachway_tab, msg='Win or Each way tab is not opened')
        self.add_selection_to_quick_bet()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        try:
            self.navigate_to_edp(event_id=self.eventID2, sport_name='horse-racing', timeout=5)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RacingEventDetails')

        if self.site.wait_for_my_stable_onboarding_overlay(timeout=5):
            self.site.my_stable_onboarding_overlay.close_button.click()

        win_or_eachway_tab = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.assertTrue(win_or_eachway_tab, msg='Win or Each way tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')

        outcome = list(outcomes.values())[0]
        outcome.bet_button.click()

        self.verify_acca_bar(decimal=True)
        self.test_005_verify_potential_payout_parameter_from_buildBet_response()
