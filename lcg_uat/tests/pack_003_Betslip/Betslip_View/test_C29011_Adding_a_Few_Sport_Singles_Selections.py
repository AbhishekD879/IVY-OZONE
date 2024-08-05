import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result, wait_for_haul
from collections import OrderedDict
from random import choice
from crlat_ob_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.smoke
@pytest.mark.betslip
@pytest.mark.football
@pytest.mark.critical
@pytest.mark.slow
@pytest.mark.timeout(900)
@pytest.mark.login
@pytest.mark.reg157_fix
@vtest
class Test_C29011_Adding_a_Few_Sport_Singles_Selections(BaseBetSlipTest):
    """
    TR_ID: C29011
    NAME: Adding Few <Sport> Singles Selections
    DESCRIPTION: This test case verifies how several single selections should be added to the Bet Slip
    PRECONDITIONS: 1.User balance is sufficient to place bets
    PRECONDITIONS: 2.To retrieve information from the Site Server use the following steps:
    PRECONDITIONS: To get class IDs and type IDs for Football sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: - XX- Category ID (Sport ID)
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: To get a list of events for types use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: - XXX - the type ID
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. To get a list of events' details use link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: - XXXX is the event ID
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: - 'name' to see the event name
    PRECONDITIONS: - 'name' on the market level - to see the market name
    PRECONDITIONS: - 'name' on the outcome level - to see selection name
    PRECONDITIONS: - 'livePriceNum'/'livePriceDen' in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: - 'priceDec' in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True
    events = {}
    league1, league2 = None, None
    number_of_events = 2
    end_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z'

    def get_active_event_selections(self, events: list, **kwargs) -> dict:
        """
        Gets dictionary of selections of active events for given category (sport, racing, etc.)
        :param events: List of events
        :param kwargs: accepts additional_filters - query_builder filter
        :return: selection ids
        """
        outcomes = [event['event']['children'][0]['market']['children'] for event in events]

        selections_ids = {}
        for event in outcomes:
            for outcome in event:
                selections_ids[outcome['outcome']['name']] = outcome['outcome']['id']
        return selections_ids

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create football events, PROD: Find 2 active football events
        """
        betslip_config = self.get_initial_data_system_configuration().get('Betslip')
        if not betslip_config:
            betslip_config = self.cms_config.get_system_configuration_item('Betslip')
        if not betslip_config.get('maxBetNumber'):
            self.__class__.max_singles_selection_number = 0
        else:
            self.__class__.max_singles_selection_number = int(betslip_config.get('maxBetNumber'))
        if self.max_singles_selection_number <= 0:
            raise CmsClientException(f'Max number of selections in Betslip is "{self.max_singles_selection_number}". '
                                     f'Cannot continue the test')
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            if len(events) < 2:
                SiteServeException('Not enough event found')
            # event 1
            event1 = choice(events)
            events.remove(event1)
            self.__class__.eventID_1 = event1['event']['id']
            self.__class__.created_event_name = normalize_name(event1['event']['name']).strip()
            self.events[self.eventID_1] = self.created_event_name

            market = next((market for market in event1['event']['children']
                           if 'Match Betting' in market['market']['templateMarketName']), None)
            if not market:
                raise SiteServeException('No Match Betting market available')

            self.__class__.market_name = market['market']['name']

            outcomes = market['market'].get('children')
            if not outcomes:
                raise SiteServeException('There are no available outcomes')

            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)

            if not self.team1:
                raise SiteServeException('No Home team found')
            if not self.team2:
                raise SiteServeException('No Away team found')

            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=event1)
            self.__class__.expected_betslip_counter_value += 1

            self._logger.info(f'*** Found event 1 with id: "{self.eventID_1}", name: "{self.created_event_name}", '
                              f'league: "{self.league1}", market name: "{self.market_name}", teams: "{self.team1}" & "{self.team2}"')

            # event 2
            event2 = choice(events)
            self.__class__.eventID_2 = event2['event']['id']
            self.__class__.created_event_2_name = normalize_name(event2['event']['name'])
            self.events[self.eventID_2] = self.created_event_2_name

            market2 = next((market for market in event2['event']['children']
                           if 'Match Betting' in market['market']['templateMarketName']), None)
            if not market2:
                raise SiteServeException('No Match Betting market available')

            self.__class__.market_name2 = market2['market']['name']

            outcomes2 = market2['market'].get('children')
            if not outcomes2:
                raise SiteServeException('There are no available outcomes')

            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1_2 = next((outcome['outcome']['name'] for outcome in outcomes2 if
                                           outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2_2 = next((outcome['outcome']['name'] for outcome in outcomes2 if
                                           outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)

            if not self.team1_2:
                raise SiteServeException('No Home team found')
            if not self.team2_2:
                raise SiteServeException('No Away team found')

            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=event2)
            self.__class__.expected_betslip_counter_value += 1

            self._logger.info(f'*** Found event 2 with id: "{self.eventID_2}", name: "{self.created_event_2_name}", '
                              f'league: "{self.league2}", teams: "{self.team1_2}" & "{self.team2_2}"')

            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         number_of_events=3)
            self.__class__.eventID = events[0]['event']['id']
            all_selection_ids = self.get_active_event_selections(events=events)
            self.__class__.max_selection_ids = list(all_selection_ids.values())[:self.max_singles_selection_number]

            self._logger.info(f'*** Found event 3 with id: "{self.eventID}", max selection ids: "{self.max_selection_ids}"')
        else:
            for i in range(0, self.number_of_events):
                event_params = self.ob_config.add_autotest_premier_league_football_event()
                self.events[event_params.event_id] = f'{event_params.team1} v {event_params.team2}'
            actual_value = len(self.events.items())
            self.__class__.league1 = self.__class__.league2 = tests.settings.football_autotest_league
            self.__class__.outcome_price1_1 = self.ob_config.event.prices['odds_home']
            self.__class__.outcome_price1_2 = self.ob_config.event.prices['odds_draw']
            self.__class__.market_name = self.__class__.market_name2 = \
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')

            event = self.ob_config.add_UK_racing_event(number_of_runners=self.max_singles_selection_number)
            self.__class__.max_selection_ids = list(event.selection_ids.values())
            self.__class__.outcome_price2_1 = self.ob_config.event.prices['odds_home']
            self.__class__.outcome_price2_2 = self.ob_config.event.prices['odds_draw']
            self.__class__.eventID = event.event_id

            self.__class__.expected_betslip_counter_value = self.number_of_events
            self.assertEqual(actual_value, self.expected_betslip_counter_value,
                             msg=f'Actual number of created events "{actual_value}" '
                                 f'is not the same as expected "{self.expected_betslip_counter_value}"')

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        self.site.open_sport(name='FOOTBALL')

    def test_003_make_a_few_selections_for_the_same_market(self):
        """
        DESCRIPTION: Make a few selections for the same market
        EXPECTED: 1.  Selected price / odds buttons are highlighted in green
        EXPECTED: 2.  Betslip counter is increased to value which is equal to quantity of added selections
        """
        event = self.get_event_from_league(event_id=list(self.events.keys())[0],
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[0]}"')
        self.__class__.selection_name, selection_price = list(output_prices.items())[0]
        selection_price.scroll_to()
        selection_price.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=15)
        self.assertTrue(selection_price.is_selected(timeout=5),
                        msg=f'Bet button "{self.selection_name}" is not active after selection')
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[0]}"')
        self.__class__.selection_name2, selection_price2 = list(output_prices.items())[1]
        selection_price2.scroll_to()
        wait_for_haul()
        selection_price2.click()
        self.assertTrue(selection_price2.is_selected(timeout=5),
                        msg=f'Bet button "{self.selection_name2}" is not active after selection')

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.__class__.betslip_counter = self.site.header.bet_slip_counter.counter_value

    def test_004_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip with bets details is opened
        """
        self.site.open_betslip()

    def test_005_verify_selections_displaying(self):
        """
        DESCRIPTION: Verify selections displaying
        EXPECTED: All single selections are displayed:
        EXPECTED: - All selections are expanded
        """
        section_name = self.get_betslip_content().your_selections_label
        self.assertEqual(section_name, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Betslip section name "{section_name}" '
                             f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(selections_count, self.betslip_counter,
                         msg=f'BetSlip counter in section name "{selections_count}" '
                             f'and counter "{self.betslip_counter}" doesn\'t match')

        self.__class__.stake = self.get_betslip_sections().Singles.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found')

        self.__class__.stake2 = self.get_betslip_sections().Singles.get(self.selection_name2)
        self.assertTrue(self.stake2, msg=f'"{self.selection_name2}" stake was not found')

    def test_006_verify_selections_information(self, same_market=True):
        """
        DESCRIPTION: Verify selections information
        EXPECTED: The following info is displayed on the Bet Slip
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name ( **'name'** attribute on event level)
        EXPECTED: - Format for Sports: 'Team_A v/vs Team_B'
        EXPECTED: 4.  Selection odds ('livePriceNum'/'livePriceDen' attributes in fraction format OR 'price Dec' in decimal format)
        """
        event_name = self.stake.event_name
        self.assertEqual(event_name, list(self.events.values())[0],
                         msg=f'Selection name "{event_name}" is not the same as expected "{list(self.events.values())[0]}"')
        outcome_name = self.stake.outcome_name
        self.assertEqual(outcome_name, self.selection_name,
                         msg=f'Selection name "{outcome_name}" is not the same as expected "{self.selection_name}"')
        market_name = self.stake.market_name
        self.assertEqual(market_name, self.market_name,
                         msg=f'Market name "{market_name}" is not the same as expected "{self.market_name}"')
        odds = self.stake.odds
        if tests.settings.backend_env == 'prod':
            event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_1, query_builder=self.ss_query_builder)
            outcomes = next(((market['market']['children']) for market in event[0]['event']['children'] if
                             'Match Betting' in market['market']['templateMarketName'] and market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')

            self.__class__.initial_prices = OrderedDict([(outcome['outcome']['name'],
                                                          f'{outcome["outcome"]["children"][0]["price"]["priceNum"]}/'
                                                          f'{outcome["outcome"]["children"][0]["price"]["priceDen"]}')
                                                         for outcome in outcomes])
            self.__class__.outcome_price1_1 = self.initial_prices[self.team1]
            self.__class__.outcome_price1_2 = self.initial_prices['Draw']

            event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_2, query_builder=self.ss_query_builder)

            outcomes2 = next(((market['market']['children']) for market in event[0]['event']['children'] if
                              'Match Betting' in market['market']['templateMarketName'] and market['market'].get('children')), None)
            if outcomes2 is None:
                raise SiteServeException('There are no available outcomes')

            self.__class__.initial_prices2 = OrderedDict([(outcome['outcome']['name'],
                                                           f'{outcome["outcome"]["children"][0]["price"]["priceNum"]}/'
                                                           f'{outcome["outcome"]["children"][0]["price"]["priceDen"]}')
                                                          for outcome in outcomes2])
            self.__class__.outcome_price2_1 = self.initial_prices2[self.team1_2]
            self.__class__.outcome_price2_2 = self.initial_prices2['Draw']

        self.assertEqual(odds, self.outcome_price1_1,
                         msg=f'Outcome price "{odds}" is not the same as expected "{self.outcome_price1_1}"')
        self.assertTrue(self.stake.est_returns_label, msg='"Est. Returns" field is not displayed')
        self.assertTrue(self.stake.est_returns, msg='"Est. Returns" field is not displayed')
        label = vec.betslip.ESTIMATED_RESULTS if self.brand == 'bma' else vec.betslip.POTENTIAL_RESULTS
        self.assertEqual(self.stake.est_returns_label.text, label,
                         msg=f'Incorrect label of "Est. Returns" field\n'
                         f'Actual: {self.stake.est_returns_label.text}\nExpected: "{label}"')
        self.assertEqual(float(self.stake.est_returns), 0.00,
                         msg=f'Est. Returns amount is: "{self.stake.est_returns}" but should be "0.00")')

        event_name2 = self.stake2.event_name
        if same_market:
            second_selection_name = list(self.events.values())[0]
            expected_price = self.outcome_price1_2
        else:
            second_selection_name = list(self.events.values())[1]
            expected_price = self.outcome_price2_2

        self.assertEqual(event_name2, second_selection_name,
                         msg=f'Selection name "{event_name2}" is not the same as expected "{second_selection_name}"')
        outcome_name2 = self.stake2.outcome_name
        self.assertEqual(outcome_name2, self.selection_name2,
                         msg=f'Selection name "{outcome_name2}" is not the same as expected "{self.selection_name2}"')
        market_name2 = self.stake2.market_name
        self.assertEqual(market_name2, self.market_name2,
                         msg=f'Market name "{market_name2}" is not the same as expected "{self.market_name2}"')
        odds2 = self.stake2.odds
        self.assertEqual(float(odds2.split('/')[0]) / float(odds2.split('/')[1]),
                         float(expected_price.split('/')[0]) / float(expected_price.split('/')[1]),
                         msg=f'Outcome "{outcome_name2}" price "{odds2}" is not the same as expected "{expected_price}"')
        self.assertTrue(self.stake2.est_returns_label, msg='"Est. Returns" field is not displayed')
        self.assertTrue(self.stake2.est_returns, msg='"Est. Returns" field is not displayed')
        label = vec.betslip.ESTIMATED_RESULTS if self.brand == 'bma' else vec.betslip.POTENTIAL_RESULTS
        self.assertEqual(self.stake2.est_returns_label.text, label,
                         msg=f'Incorrect label of "Est. Returns" field\n'
                         f'Actual: {self.stake2.est_returns_label.text}\nExpected: "{label}"')
        self.assertEqual(float(self.stake2.est_returns), 0.00,
                         msg=f'Est. Returns amount is: "{self.stake2.est_returns}" but should be "0.00")')

    def test_007_verify_login_and_place_bet_button(self, login=False):
        """
        DESCRIPTION: Verify that 'REMOVE ALL' text is displayed at the top of Betslip
        DESCRIPTION: Verify 'LOGIN & PLACE BET' button
        EXPECTED: 'REMOVE ALL' text is present at the top of Betslip
        EXPECTED: 'LOGIN & PLACE BET' button is present at the bottom of the page and always visible
        """
        remove_all_button = self.get_betslip_content().remove_all_button
        name = remove_all_button.name
        self.assertTrue(remove_all_button.is_displayed(), msg='REMOVE ALL button is not displayed')
        self.assertEqual(name, vec.betslip.REMOVE_ALL_SELECTIONS,
                         msg=f'Button name "{name}" is not as expected "{vec.betslip.REMOVE_ALL_SELECTIONS}"')
        if login:
            self.assertEqual(self.get_betslip_content().bet_now_button.name,
                             vec.betslip.BET_NOW,
                             msg=f'Bet button caption should be "{vec.betslip.BET_NOW}"')
        else:
            bet_button_caption = self.get_betslip_content().bet_now_button.name
            self.assertEqual(bet_button_caption,
                             vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                             msg=f'Bet button caption "{bet_button_caption}" is not the same as expected "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()
        self.__class__.expected_betslip_counter_value = 0

    def test_008_add_max_num_to_the_bet_slip(self):
        """
        DESCRIPTION: Add <Max_num> to the Bet Slip
        EXPECTED: Max_num - Max number of singles selection is CMS configurable (System configuration -> maxBetNumber value)
        """
        # TODO uncomment after VANO-1727 is resolved
        # self.open_betslip_with_selections(selection_ids=self.max_selection_ids)
        self.open_betslip_with_selections(selection_ids=self.max_selection_ids[:10])
        if self.max_singles_selection_number > 10:
            self.open_betslip_with_selections(selection_ids=self.max_selection_ids[10:])

    def test_009_try_to_add_max_num_plus_1selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Try to add <Max_num> + 1 selection to the Bet Slip
        EXPECTED: 1.  Ability to add selection is restricted
        EXPECTED: 2.  Error message appears: "Maximum number of selections allowed on betslip is <Max number of singles selection>"
        """
        self.site.close_betslip()
        self.site.open_sport(name='FOOTBALL')
        event = self.get_event_from_league(event_id=list(self.events.keys())[0],
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[0]}"')
        self.__class__.selection_name, selection_price = list(output_prices.items())[0]
        selection_price.click()

        betslip_full_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_BETSLIP_FULL)
        self.assertTrue(betslip_full_dialog, msg=f'{vec.dialogs.DIALOG_MANAGER_BETSLIP_FULL} is not shown')
        expected_message = vec.betslip.MAX_SELECTION_MESSAGE.format(max_number=self.max_singles_selection_number)
        result = wait_for_result(lambda: expected_message == betslip_full_dialog.title_text,
                                 timeout=30,
                                 name='Waiting for Betslip full message')
        self.assertTrue(result, msg=f'Actual dialog message - "{betslip_full_dialog.title_text} is not equal to expected - '
                                    f'"{expected_message}"')
        betslip_full_dialog.close_dialog()

    def test_010_deselect_selection_from_the_event_page(self):
        """
        DESCRIPTION: Deselect selection from the event page
        EXPECTED: 1.  The price becomes un-highlighted in grey
        EXPECTED: 2.  Bet Slip counter is decreased by 1
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        edp_tab_menus = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        #Check if We Are On WIN OR E/W Tab because get_active_events_for_category() method only returns selection for WIN or E/W Tab
        if edp_tab_menus.current != 'WIN OR E/W':
            edp_tab_menus.items_as_ordered_dict.get('WIN OR E/W', None).click()
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No one section was found')
        initial_value = int(self.site.header.bet_slip_counter.counter_value)
        first_section_name, first_section = list(sections.items())[0]
        outcomes = first_section.items_as_ordered_dict
        outcome_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()

        self.verify_betslip_counter_change(expected_value=initial_value - 1)

    def test_011_log_in_to_the_application_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Log in to the application and Repeat steps №2-10
        EXPECTED: Results are the same, except
        EXPECTED: Instead 'LOGIN & PLACE BET' button 'PLACE BET' button is shown
        """
        self.site.open_betslip()
        self.clear_betslip()
        self.site.login(username=tests.settings.betplacement_user)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(format_changed, msg='Odds format is not changed to fractional')
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.__class__.expected_betslip_counter_value = self.number_of_events
        self.test_003_make_a_few_selections_for_the_same_market()
        self.test_004_go_to_the_betslip()
        self.test_007_verify_login_and_place_bet_button(login=True)

    def test_012_make_selections_for_different_markets(self):
        """
        DESCRIPTION: Make selections for different markets
        EXPECTED: The same as in step №3
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.__class__.expected_betslip_counter_value = self.number_of_events
        event = self.get_event_from_league(event_id=list(self.events.keys())[0],
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[0]}"')
        self.__class__.selection_name, selection_price = list(output_prices.items())[0]
        selection_price.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=15)
        self.assertTrue(selection_price.is_selected(timeout=2),
                        msg=f'Bet button "{self.selection_name}" is not active after selection')

        event2 = self.get_event_from_league(event_id=list(self.events.keys())[1],
                                            section_name=self.league2)
        self.output_prices2 = event2.get_active_prices()
        self.assertTrue(self.output_prices2,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[1]}"')
        self.__class__.selection_name2, selection_price2 = list(self.output_prices2.items())[1]
        selection_price2.scroll_to()
        selection_price2.click()
        self.assertTrue(selection_price2.is_selected(timeout=2),
                        msg=f'Bet button "{self.selection_name2}" is not active after selection')

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.__class__.betslip_counter = self.site.header.bet_slip_counter.counter_value

    def test_013_repeat_steps4_7(self):
        """
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: The same as in step №11
        """
        self.test_004_go_to_the_betslip()
        self.test_005_verify_selections_displaying()
        self.test_006_verify_selections_information(same_market=False)
        self.test_007_verify_login_and_place_bet_button(login=True)
