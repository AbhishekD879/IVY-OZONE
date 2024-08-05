import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create Event hub in prod
# @pytest.mark.hl
@pytest.mark.featured
@pytest.mark.event_hub
@pytest.mark.sanity
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C14253860_Featured_module_by_Market_ID_Expiration_of_Event(BaseFeaturedTest):
    """
    TR_ID: C14253860
    NAME: Featured module by Market ID: Expiration of Event
    DESCRIPTION: This test case verifies that Featured module by Market ID is removed when an event is expired
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Featured module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in the previously created EventHub and it's expanded by default. (Sports Pages > EventHub > Featured events > 'Create Featured Tab Module')
    PRECONDITIONS: 3. Should be also created Module Ribbon tab related to the created Event Hub (from step1) - CMS->Module Ribbon Tabs->Create Module Ribbon Tab (choose 'Event Hub' in the 'Directive Name' dropdown and created Event Hub (from step1) in 'Event Hub Name' dropdown)
    PRECONDITIONS: 4. A user is on Homepage > EventHub tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: * To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL XXX - the event ID X.XX - currently supported version of OpenBet release LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete the event:
    PRECONDITIONS: * open the event page in TI;
    PRECONDITIONS: * set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: * open the event page in TI;
    PRECONDITIONS: * undisplay it and save changes.
    """
    keep_browser_open = True
    extra_market = [('both_teams_to_score', {'cashout': True})]

    def test_000_preconditions(self):
        """
        DESCRIPTION:- Create Events and Event hub
        """
        # Create event
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=self.extra_market,
                                                                                 perform_stream=True)
        self.__class__.eventID = event_params.event_id

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_name = normalize_name(event_resp[0]['event']['name'])
        markets = event_resp[0]['event']['children']
        default_market_id = [market['market']['id'] for market in markets if
                             market['market']['templateMarketName'] == 'Match Betting'][0]
        self.__class__.outcomes = next(((market['market'].get('children')) for market in markets), None)
        if self.outcomes is None:
            raise SiteServeException('There are no available outcomes')
        # outcomeMeaningMinorCode: A - away, H - home, D - draw
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'H'), None)
        self.__class__.team2 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'A'), None)
        self._logger.info(f'*** Created Football event  with name "{event_name}"')

        # Create Event Hub module
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')

        module_data = self.cms_config.add_featured_tab_module(select_event_by='Market',
                                                              id=default_market_id,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-14,
                                                              module_time_from_hours_delta=-14)
        self.__class__.module_name = module_data['title'].upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get('modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from preconditions
        EXPECTED: The event is displayed with correct outcomes
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module, msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

        event_hub_team_1 = event_hub_module.first_player
        event_hub_team_2 = event_hub_module.second_player
        self.assertEqual(event_hub_team_1, self.team1, msg=f'Team1 name "{event_hub_team_1}" on Event hub module is '
                                                           f'not equal to expected "{self.team1}"')
        self.assertEqual(event_hub_team_2, self.team2, msg=f'Team2 name "{event_hub_team_2}" on Event hub module is '
                                                           f'not equal to expected "{self.team2}"')

        price_buttons = event_hub_module.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')

        for name, bet_button in list(price_buttons.items()):
            price = bet_button.outcome_price_text
            self.assertRegexpMatches(price, self.fractional_pattern,
                                     msg=f'Odds value "{price}" is not in correct format "{self.fractional_pattern}"')
            price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes
                               if 'price' in i["outcome"]["children"][0].keys() and i["outcome"]['name'] == name), '')
            self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes}"')
            price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
            self.assertEqual(price, price_resp,
                             msg=f'Price "{price}" is not the same as in response "{price_resp}"')

    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Module from Step 1 is undisplayed
        EXPECTED: Message 'No events found' is displayed
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertFalse(event_hub_modules, msg=f'Modules found on "{self.event_hub_tab_name}" tab')
        result = wait_for_result(lambda: event_hub_content.has_no_events_label(),
                                 timeout=50,
                                 name='"No Events Found" msg not displayed')
        self.assertTrue(result, msg='"No Events Found" msg not displayed')
