import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-5753')
@vtest
class Test_C28855_Verify_Price_Odds_Buttons_for_Race_with_SP_price_type(BaseRacing):
    """
    TR_ID: C28855
    NAME: Verify Order of Active SP Selections
    DESCRIPTION: Verify Price/Odds Buttons for <Race> with SP price type
    PRECONDITIONS: There is <Race> events with SP prices available, no LP prices:
    PRECONDITIONS: (1) event with 'runnerNumber' attribute
    PRECONDITIONS: (2) event without 'runnerNumber' attribute
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = []
            additional_filter.append(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                               OPERATORS.INTERSECTS, 'SP')))
            additional_filter.append(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.RUNNER_NUMBER, OPERATORS.IS_NOT_EMPTY))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)
            sp_event = None
            for event in events:
                for market in event['event']['children']:
                    if market['market'].get('children') and market.get('market').get(
                            'templateMarketName') == 'Win or Each Way':
                        if all(not outcome['outcome'].get('children') for outcome in market['market']['children']) and \
                                len([outcome for outcome in market['market']['children']
                                    if outcome['outcome'].get('runnerNumber')]) > 2:
                            sp_event = event
                            break
                if sp_event:
                    break

            if sp_event is None:
                raise SiteServeException('There is no HR events with runner numbers')
            self.__class__.eventID_1 = sp_event['event']['id']

            # On prod only unnamed racers don't have runner number
            additional_filter = []
            additional_filter.append(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                               OPERATORS.EQUALS, 'SP')))
            additional_filter.append(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.RUNNER_NUMBER, OPERATORS.IS_EMPTY))
            additional_filter.append(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.OUTCOME, ATTRIBUTES.NAME, OPERATORS.NOT_CONTAINS,
                                                                               'Unnamed')))
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=additional_filter)[0]
            if event is None:
                raise SiteServeException('There is no HR events without runner numbers')
            self.__class__.eventID_2 = event['event']['id']
            self.__class__.unnamed_order = ['Unnamed Favourite', 'Unnamed 2nd Favourite']
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=4)
            self.__class__.eventID_1 = event_params.event_id

            runner_numbers = ['-', '-', '-', '-']
            event_params = self.ob_config.add_UK_racing_event(runner_numbers=runner_numbers)
            self.__class__.eventID_2 = event_params.event_id

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID_1, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict.get(
            "WIN OR E/W").click()

    def test_002_open_event_1_from_preconditions(self):
        """
        DESCRIPTION: Open event (1) from preconditions
        EXPECTED: All selections display SP
        """
        self.__class__.default_tab = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        tabs = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.items()
        tab_name, self.__class__.tab = list(tabs)[0]
        self.assertEqual(tab_name, self.default_tab,
                         msg=f'{self.default_tab} is not opened')

        for outcome_name, outcome in self.tab.items_as_ordered_dict.items():
            self.assertEqual(outcome.bet_button.outcome_price_text, 'SP',
                             msg=f'Price for {outcome_name} is not the same as expected. '
                                 f'Actual: {outcome.bet_button.outcome_price_text}. Expected: "SP"')

    def test_003_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered by '**runnerNumber'** attribute in ascending order
        """
        list_of_numbers = []
        for outcome_name, outcome in self.tab.items_as_ordered_dict.items():
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                list_of_numbers.append(int(outcome.runner_number))
        self.assertListEqual(list_of_numbers, sorted(list_of_numbers),
                             msg=f'Outcomes "{list_of_numbers}" are not sorted by '
                             f'runner numbers "{sorted(list_of_numbers)}"')

    def test_004_open_event_2_from_preconditions(self):
        """
        DESCRIPTION: Open event (2) from preconditions
        EXPECTED: All selections display SP
        """
        self.navigate_to_edp(event_id=self.eventID_2, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict.get(
            "WIN OR E/W").click()
        tabs = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.items()
        tab_name, self.__class__.tab = list(tabs)[0]
        self.assertEqual(tab_name, self.default_tab,
                         msg=f'"{self.default_tab}" is not opened')

        for outcome_name, outcome in self.tab.items_as_ordered_dict.items():
            if 'Unnamed' in outcome_name:
                self.assertEqual(outcome.bet_button.outcome_price_text, 'SP',
                                 msg=f'Price for {outcome_name} is not the same as expected. '
                                 f'Actual: {outcome_name}. Expected: "SP"')

    def test_005_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered alphabetically
        EXPECTED: Alphabetically by first letter of Horse name
        EXPECTED: If first letter of Outcome name is the same then sort by second letter
        """
        list_of_names = []
        for outcome_name, outcome in self.tab.items_as_ordered_dict.items():
            if tests.settings.backend_env == 'prod':
                if 'Unnamed' in outcome_name:
                    list_of_names.append(outcome_name)
            else:
                list_of_names.append(outcome_name)

        if tests.settings.backend_env == 'prod':
            self.assertListEqual(list_of_names, self.unnamed_order,
                                 msg=f'Outcomes are not sorted by runner names. '
                                 f'Actual order: "{list_of_names}". Expected: "{self.unnamed_order}"')
        else:
            self.assertListEqual(list_of_names, sorted(list_of_names),
                                 msg=f'Outcomes are not sorted by runner names. '
                                 f'Actual order: "{list_of_names}". Expected: "{sorted(list_of_names)}"')
