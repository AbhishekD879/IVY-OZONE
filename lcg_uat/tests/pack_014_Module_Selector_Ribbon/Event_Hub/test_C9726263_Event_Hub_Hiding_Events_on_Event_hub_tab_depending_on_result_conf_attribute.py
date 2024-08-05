import pytest
import json
from tests.base_test import vtest
from tests.Common import Common
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException
from time import sleep
from voltron.pages.shared import get_device


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create event hub in prod
# @pytest.mark.hl # Cannot create event hub in hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C9726263_Event_Hub_Hiding_Events_on_Event_hub_tab_depending_on_result_conf_attribute(Common):
    """
    TR_ID: C9726263
    NAME: Event Hub: Hiding Events on Event hub tab depending on 'result_conf' attribute
    DESCRIPTION: This test case verifies Hiding Events on Event Hub tab depending on 'result_conf' attribute
    PRECONDITIONS: 1. To set result for event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'result_conf' attribute value check LIVE SERV pushes: Network -> push -> Preview/response tab
    """
    keep_browser_open = True

    def result_conf(self, param, index_number: str, delimiter='42'):
        logs = get_device().get_performance_log()
        delimit = delimiter + '/' + 'h' + str(index_number) + ','
        for entry in logs[::-1]:
            try:
                if param in entry[1]['message']['message']['params']['response']['payloadData']:
                    return json.loads(entry[1]['message']['message']['params']['response']['payloadData'].split(delimit)[1])[1]
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Event hub
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.selection_ids = list(event_params.selection_ids.values())
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID = self.ob_config.market_ids[event_params.event_id][market_short_name]
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=self.index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=self.eventID,
                                                              page_type='eventhub', page_id=self.index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{self.index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=self.index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state(state_name='Homepage')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_load_oxygen_application_and_navigate_to_event_hub_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Event hub tab
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_module = event_hub_content.event_hub_items_dict.get(self.module_name)
        self.assertTrue(event_hub_module, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_002_select_any_live_sport_event_from_event_hub_tab(self):
        """
        DESCRIPTION: Select any LIVE sport event from Event Hub tab
        """
        # Covered in step 001

    def test_003_in_ti_tool_set_results_for_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set results for selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - result_conf:”Y” attribute is received in Live Serve push
        EXPECTED: - event stops to display on Event Hub tab in real time
        """
        self.result_event(selection_ids=self.selection_ids, market_id=self.marketID, event_id=self.eventID)
        sleep(5)
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertFalse(module_content, msg='Event is displayed on UI')
        event_hub = self.result_conf(param='result_conf', index_number=self.index_number)
        result_conf = event_hub['event']['result_conf']
        self.assertEqual(result_conf, 'Y',
                         msg=f'Actual attribute :"{result_conf}" is not same as'
                             f'Expected attribute: "Y"')
