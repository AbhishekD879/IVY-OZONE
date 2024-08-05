import pytest
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create event hub in prod/beta
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11250794_Featured_module_Market_ID_Outcome_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C11250794
    NAME: Featured module Market ID: Outcome Becomes Suspended
    DESCRIPTION: This test case verifies situation when outcome/outcomes become suspended on Homepage on the EventHub tab(mobile/tablet) of a module by MarketID
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Featured module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in the previously created EventHub and it's expanded by default.
    PRECONDITIONS: 3. A user is on Homepage > EventHub tab.
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) > Sports Pages > EventHub > Featured events > 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * Z.ZZ - currently supported version of OpenBet SiteServer
    PRECONDITIONS: * XXXX - event ID
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = list(event.selection_ids.values())
        self.__class__.market_id = event.default_market_id
        event1 = self.ob_config.add_autotest_premier_league_football_event()

        self.__class__.market_id1 = event1.default_market_id
        self.__class__.eventID1 = event1.event_id
        self.__class__.selection_ids1 = list(event1.selection_ids.values())

        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Market', id=self.market_id,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        module_data1 = self.cms_config.add_featured_tab_module(select_event_by='Market', id=self.market_id1,
                                                               page_type='eventhub',
                                                               page_id=index_number,
                                                               events_time_from_hours_delta=-10,
                                                               module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()
        self.__class__.module_name1 = module_data1['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)

        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state(state_name='Homepage')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        EXPECTED:
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        self.__class__.module = self.get_section(section_name=self.module_name)
        self.__class__.module1 = self.get_section(section_name=self.module_name1)

    def test_002_trigger_the_following_situation_in_ti_for_this_eventoutcomestatuscodes_for_one_of_the_outcomes_of_the_market(
            self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of the market
        EXPECTED:
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=True,
                                              active=False)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'S', msg="Not matching")

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * Only one Price/Odds button is disabled immediately
        EXPECTED: * The rest Price/Odds buttons of the same market are not changed
        """
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertFalse(bet_button1.is_enabled(timeout=10, expected_result=True),
                         msg=f'selection is active in "{self.module_name}" module')
        bet_button2 = self.module.get_bet_button_by_selection_id(self.selection_ids[1])
        self.assertTrue(bet_button2.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')
        bet_button3 = self.module.get_bet_button_by_selection_id(self.selection_ids[2])
        self.assertTrue(bet_button3.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')

    def test_004_change_attribute_for_this_eventoutcomestatuscodea_for_the_same_outcome(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        EXPECTED: * Price/Odds button of this outcome is not disabled anymore
        EXPECTED: * Price/Odds button becomes active
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=True,
                                              active=True)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'A', msg="Not matching")
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')

    def test_005_find_another_event_with_priceodds_buttons_that_displaying_prices(self):
        """
        DESCRIPTION: Find another event with 'Price/Odds' buttons that displaying prices
        EXPECTED:
        """
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'A', msg="Not matching")
        bet_button1 = self.module1.get_bet_button_by_selection_id(self.selection_ids1[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name1}" module')

    def test_006_trigger_the_following_situation_for_this_eventoutcomestatuscodes_for_one_of_the_outcomes_of_the_market_or_win_or_each_way_for_races_market_type(
            self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of the market (or 'Win Or Each Way' for <Races>) market type
        EXPECTED:
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids1[0], displayed=True,
                                              active=False)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'S', msg="Not matching")

    def test_007_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * Only one Price/Odds button is disabled immediately
        EXPECTED: * The rest Price/Odds buttons of the same market are not changed
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        bet_button1 = self.module1.get_bet_button_by_selection_id(self.selection_ids1[0])
        self.assertFalse(bet_button1.is_enabled(timeout=10, expected_result=True),
                         msg=f'selection is active in "{self.module_name1}" module')
        bet_button2 = self.module1.get_bet_button_by_selection_id(self.selection_ids1[1])
        self.assertTrue(bet_button2.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name1}" module')
        bet_button3 = self.module1.get_bet_button_by_selection_id(self.selection_ids1[2])
        self.assertTrue(bet_button3.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name1}" module')

    def test_008_collapse_module(self):
        """
        DESCRIPTION: Collapse module
        EXPECTED:
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_009_change_attribute_for_this_eventoutcomestatuscodea_for_the_same_outcome(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        EXPECTED:
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids1[0], displayed=True,
                                              active=True)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'A', msg="Not matching")
        bet_button1 = self.module1.get_bet_button_by_selection_id(self.selection_ids1[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name1}" module')

    def test_010_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * Price/Odds button of this outcome is not disabled anymore
        EXPECTED: * Price/Odds button becomes active
        """
        self.module1.expand()
        self.assertTrue(self.module1.is_expanded(), msg=f'"{self.module_name1}" module is not expanded')
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'A', msg="Not matching")
        bet_button1 = self.module1.get_bet_button_by_selection_id(self.selection_ids1[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name1}" module')
