import pytest
import tests
from random import choice
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create Eventhub in prod/beta
@pytest.mark.mobile_only
@pytest.mark.sanity
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C14253863_Event_hub_Verify_module_created_by_Race_Win_or_Each_Way_market(BaseRacing):
    """
    TR_ID: C14253863
    NAME: Event hub: Verify module created by <Race> Win or Each Way market
    DESCRIPTION: This test case verifies Featured events module created by <Race> Win or Each Way market on Event Hub
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. <Race> event created in TI
    PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 4. Featured module by Market Id (Win Or Each Way) is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 5. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True
    max_rows = 3

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. CMS, TI:
        PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
        PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
        PRECONDITIONS: 2. <Race> event created in TI
        PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
        PRECONDITIONS: 4. Featured module by Market Id (Win Or Each Way) is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
        PRECONDITIONS: 5. User is on Homepage > Event Hub tab
        """
        # Create event
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(
                category_id=self.ob_config.add_UK_racing_event(number_of_runners=3),
                all_available_events=True)

            event = choice(events)
            self.__class__.eventID = event['event']['id']
            if event['event'].get('drilldownTagNames'):
                self.__class__.is_watch_live = any(
                    flag in event['event']['drilldownTagNames'] for flag in self.watch_live_flags)
            else:
                self.__class__.is_watch_live = False
        else:
            event_params = self.ob_config.add_UK_racing_event(perform_stream=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.is_watch_live = True

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.markets = event_resp[0]['event']['children']
        default_market_id = [market['market']['id'] for market in self.markets if
                             market['market']['templateMarketName'] == 'Win or Each Way'][0]
        self.__class__.outcomes = next(((market['market'].get('children')) for market in self.markets), None)
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
                                                              page_id=index_number, events_time_from_hours_delta=-14,
                                                              module_time_from_hours_delta=-14, max_rows=self.max_rows)
        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get(
                                                                         'modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result,
                        msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_navigate_to_module_from_preconditions_and_verify_its_header(self):
        """
        DESCRIPTION: Navigate to Module from preconditions and verify it's header
        EXPECTED: * Module Header contains Event time and name and 'More' button.
        EXPECTED: More button navigates user to EDP
        EXPECTED: * Header CANNOT be collapsed/expanded
        """
        self.site.wait_content_state('Homepage')
        self.site.wait_content_state_changed(timeout=60)
        self.site.home.module_selection_ribbon.tab_menu.click_button(self.event_hub_tab_name)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules, self.__class__.event = \
            list(event_hub_content.event_hub_items_dict.items())[0]
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        subheader = event_hub_content.subheader.text
        self.assertTrue(subheader, msg='Each way terms are not displayed')
        self.assertFalse(self.event.is_expanded(timeout=2),
                         msg=f'Module: "{self.module_name}" not expanded')
        self.__class__.event_hub_module = list(self.event.items_as_ordered_dict.keys())
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        for runner in self.event_hub_module:
            num, name, price = runner.split('\n')
            self.assertTrue(name, msg='Runner name is not displayed')
            self.assertEqual(price, 'SP', msg='SP price is not displayed')
        event_hub_content.see_all.click()
        self.site.wait_content_state_changed()

    def test_002_verify_area_below_header(self):
        """
        DESCRIPTION: Verify area below header
        EXPECTED: * Area contains:
        EXPECTED: - Each Way terms
        EXPECTED: - Watch icon (if available)
        """
        try:
            self.assertTrue(self.event.has_stream(), msg='"Watch Live" icon is not found')
        except VoltronException:
            self._logger.info(msg="Watch live icon is not available")

    def test_003_verify_list_of_runners(self):
        """
        DESCRIPTION: Verify List of runners
        EXPECTED: * Number of runners displayed corresponds to number of selections set in CMS
        EXPECTED: * Price buttons displayed near each selection with price set in TI
        """
        # Covered in step 002

    def test_004_verify_the_bottom_of_the_module(self):
        """
        DESCRIPTION: Verify the bottom of the module
        EXPECTED: * There is no 'See all' button displayed at the bottom of the page for the *<Race> Win or Each Way market* module
        EXPECTED: (After redesign 'See all' selection button has been removed)
        EXPECTED: * Number of selections that are shown equals to *Number of Selections to Display* value in module configuration in CMS
        """
        self.assertFalse(self.event.show_more, msg='Show more link is displayed')
        self.assertEqual(len(self.event_hub_module), self.max_rows, msg=f'Number of selections that are shown are not '
                                                                        f'equals to "{self.max_rows}" ')
