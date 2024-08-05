import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter, SiteServeRequests

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28854_Unnamed_Favourite_Selections_Display(BaseRacing):
    """
    TR_ID: C28854
    NAME: Unnamed Favourite Selections Display
    DESCRIPTION: This test case verify Unnamed Favourite and Unnamed 2nd Favourite Selections Display
    PRECONDITIONS: There is a <Race> with unnamed favourite selections:
    PRECONDITIONS: - Unnamed Favourite
    PRECONDITIONS: - Unnamed 2nd Favourite
    """
    keep_browser_open = True
    ss_market_outcomes = None
    win_or_each_way_market_outcomes = None
    horses_info = {'Unnamed Favourite': None, 'Unnamed 2nd Favourite': None}
    last_horse = second_last_horse = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Add horseracing event with Unnamed Favourite selections, PROD: Find horseracing event with Unnamed Favourite selections
        """
        if tests.settings.backend_env == 'prod':

            class_ids = self.get_class_ids_for_category(category_id=self.ob_config.horseracing_config.category_id)
            ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                       class_id=class_ids,
                                       brand=self.brand)

            events_filter = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
                .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP')) \
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME,
                                                        OPERATORS.EQUALS,
                                                        f'|Win or Each Way|')))
            self.__class__.selection_ids = {}

            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)

            unnamed_present = False
            for event in resp:
                if event.get('event') and event['event'].get('children'):
                    markets = event['event']['children']
                    for market in markets:
                        if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                            for outcome in market['market']['children']:
                                if 'Unnamed' in outcome['outcome']['name']:
                                    unnamed_present = True
                                    break
                            if unnamed_present:
                                self.__class__.eventID = event['event']['id']
                                for outcome in market['market']['children']:
                                    self.selection_ids[outcome['outcome']['name']] = outcome['outcome']['id']
                        if unnamed_present:
                            break
                if unnamed_present:
                    break
            if not unnamed_present:
                raise SiteServeException('No events with Unnamed selection found')
        else:
            event_info = self.ob_config.add_UK_racing_event(number_of_runners=3, unnamed_favorites=True)
            self.__class__.eventID = event_info.event_id
            self.__class__.selection_ids = event_info.selection_ids

        for selection, selection_id in self.selection_ids.items():
            if selection in self.horses_info.keys():
                self.__class__.horses_info.update({selection: selection_id})

        if len(self.selection_ids) == 0:
            raise SiteServeException('There are no Unnamed Favourites selections available')

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        ss_event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                     query_builder=self.ss_query_builder)
        self.__class__.ss_market_outcomes = ss_event_details[0]['event']['children'][0]['market']['children']

    def test_002_verify_ordering_of_unnamed_favourite_selections(self):
        """
        DESCRIPTION: Verify ordering of Unnamed Favourite Selections
        EXPECTED: Unnamed Favourites are displayed at the end of the list in the following order:
        EXPECTED: 1st - Unnamed Favourite
        EXPECTED: 2nd - Unnamed 2nd Favourite
        """
        tab_content = self.site.racing_event_details.tab_content
        markets_list = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Event details page has no available markets')
        tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        try:
            self.assertIn(tab_name, markets_list,
                          msg=f'"{tab_name}" market is not available among available markets "{markets_list.keys()}"')
        except Exception:
            self._logger.info(f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" market is not available among available '
                              f'markets, "{markets_list}" is opened')
            market_tabs = tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            for market_name, market_value in market_tabs.items():
                if market_name == tab_name:
                    market_value.click()
                    self.site.wait_splash_to_hide(5)
                    markets_list = tab_content.event_markets_list.items_as_ordered_dict
                    self.assertIn(tab_name, markets_list,
                                  msg=f'"{tab_name}" market is not available among available markets "{markets_list.keys()}"')
                    break

        win_or_each_way_market = markets_list.get(tab_name)
        self.__class__.win_or_each_way_market_outcomes = win_or_each_way_market.items_as_ordered_dict
        self.assertTrue(self.win_or_each_way_market_outcomes, msg=f'"{tab_name}" market has no available outcomes')

        list_of_horses = list(self.win_or_each_way_market_outcomes.keys())
        self.__class__.last_horse = list_of_horses[-1]
        self.__class__.second_last_horse = list_of_horses[-2]
        self.assertTrue(self.last_horse == 'Unnamed 2nd Favourite' and self.second_last_horse == 'Unnamed Favourite',
                        msg=f'Unnamed Favourites displayed in the wrong order. '
                        f'Last horse is: "{self.last_horse}", second last horse is: "{self.second_last_horse}"')

    def test_003_verify_unnamed_favourite_selection_displaying(self):
        """
        DESCRIPTION: Verify Unnamed Favourite selection displaying
        EXPECTED: Name is "Unnamed Favourite" (corresponds to the 'name' attribute in SiteServer)
        EXPECTED: Note: attribute 'outcomeMeaningMinorCode'=1 for this selection
        """
        horse_name = 'Unnamed Favourite'
        outcome_id = self.horses_info.get(horse_name)

        outcome = next((outcome for outcome in self.ss_market_outcomes if outcome['outcome']['id'] == outcome_id), None)
        self.assertTrue(outcome, msg=f'There is no market outcome with "{horse_name}" name attribute')

        self.assertEqual(self.second_last_horse, outcome['outcome']['name'],
                         msg=f'Horse name "{self.second_last_horse}" do not corresponds to the \'name\' '
                         f'attribute in SiteServer "{outcome["outcome"]["name"]}"')
        self.assertEqual(outcome['outcome']['outcomeMeaningMinorCode'], '1',
                         msg=f'\'outcomeMeaningMinorCode\' attribute value "{outcome["outcome"]["outcomeMeaningMinorCode"]}" '
                         f'is not the same as expected "1"')

    def test_004_verify_unnamed_2nd_favourite_selection_displaying(self):
        """
        DESCRIPTION: Verify Unnamed 2nd Favourite selection displaying
        EXPECTED: Name is "Unnamed 2nd Favourite" (corresponds to the **'name' **attribute in SiteServer)
        EXPECTED: Note: attribute 'outcomeMeaningMinorCode'=2 for this selection
        """
        horse_name = 'Unnamed 2nd Favourite'
        outcome_id = self.horses_info.get(horse_name)

        outcome = next((outcome for outcome in self.ss_market_outcomes if outcome['outcome']['id'] == outcome_id), None)
        self.assertTrue(outcome, msg=f'There is no market outcome with "{horse_name}" name attribute')

        self.assertEqual(self.last_horse, outcome['outcome']['name'],
                         msg=f'Horse name "{self.last_horse}" do not corresponds to the \'name\' attribute in SiteServer "{outcome["outcome"]["name"]}"')
        self.assertEqual(outcome['outcome']['outcomeMeaningMinorCode'], '2',
                         msg=f'\'outcomeMeaningMinorCode\' attribute value "{outcome["outcome"]["outcomeMeaningMinorCode"]}" '
                         f'is not the same as expected "2"')

    def test_005_verify_price_odds_button(self):
        """
        DESCRIPTION: Verify price/odds button
        EXPECTED: Price/Odds is SP for both selections
        """
        for horse in self.horses_info.keys():
            unnamed_selection = self.win_or_each_way_market_outcomes.get(horse)
            selection_odds = unnamed_selection.bet_button.name
            self.assertEqual(selection_odds, 'SP', msg=f'Odds "{selection_odds}" are not the same as expected "SP"')
