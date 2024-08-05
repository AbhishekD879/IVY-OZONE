import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import get_featured_event_hub_by_event_id
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create event hub in prod
# @pytest.mark.hl # Cannot create event hub in hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C9726262_Event_hub_Hiding_Events_on_Event_Hub_tab_depending_on_Displayed_attribute(Common):
    """
    TR_ID: C9726262
    NAME: Event hub: Hiding Events on Event Hub tab depending on 'Displayed' attribute
    DESCRIPTION: This test case verifies Hiding Events on Event hub tab depending on Displayed attribute
    PRECONDITIONS: 1. To display/undisplay event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check Featured webSocket: Network -> WS -> wss://featured-sports.coralsports.nonprod.cloud.ladbrokescoral.com/socket.io/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1) 2 Featured Modules created in CMS > Sport Pages > Event Hub > Edit Event Hub. Modules are Active and are displayed on Event Hub tab in app.
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=self.index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=self.eventID,
                                                              page_type='eventhub', page_id=self.index_number)
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
        DESCRIPTION: Load Oxygen application and navigate to Event Hub tab
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_module = event_hub_content.event_hub_items_dict.get(self.module_name)
        self.assertTrue(event_hub_module, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_002_select_any_sport_event__from_event_hub_tab(self):
        """
        DESCRIPTION: Select any sport event  from Event Hub tab
        """
        # Covered in step 001

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"N" attribute is received in Featured WebSocket
        EXPECTED: - event stops to display on Event Hub tab in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)
        sleep(5)
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertFalse(module_content, msg='Event is displayed on UI')

        event_hub = get_featured_event_hub_by_event_id(event_id=self.eventID, index_number=self.index_number)
        is_displayed = event_hub['event']['displayed']
        self.assertEqual(is_displayed, 'N',
                         msg=f'Actual attribute :"{is_displayed}" is not same as'
                             f'Expected attribute: "N"')

    def test_004_in_ti_tool_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set previously selected event to Displayed and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"Y" attribute is received in Featured WebSocket
        EXPECTED: - event does NOT start to display in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        sleep(5)
        event_hub = get_featured_event_hub_by_event_id(event_id=self.eventID, index_number=self.index_number)
        is_displayed = event_hub['event']['displayed']
        self.assertEqual(is_displayed, 'Y',
                         msg=f'Actual attribute :"{is_displayed}" is not same as'
                             f'Expected attribute: "Y"')

    def test_005_refresh_the_page_and_verify_the_event_displaying(self):
        """
        DESCRIPTION: Refresh the page and verify the event displaying
        EXPECTED: Event starts to display on Event Hub tab
        """
        self.device.refresh_page()
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(module_content,  msg='Event is not displayed on UI')
