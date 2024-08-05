import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726264_Event_Hub_Verify_hiding_of_Races_events_on_Event_Hub_tab_depending_on_Displayed_attribute(Common):
    """
    TR_ID: C9726264
    NAME: Event Hub: Verify hiding of <Races> events on Event Hub tab depending on 'Displayed' attribute
    DESCRIPTION: This test case verifies  hiding of <Races> events on Event Hub tab depending on 'Displayed' attribute
    PRECONDITIONS: 1. To display/undisplay events use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check LIVE SERV pushes: Network -> push -> Preview/response tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1) 2 Featured Modules created in CMS > Sport Pages > Event Hub > Edit Event Hub. Modules are Active and are displayed on Event Hub tab in app.
        """
        event_params = self.ob_config.add_UK_racing_event()
        self.__class__.race_event_name = event_params.ss_response['event']['name']
        self.__class__.eventID = event_params.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=self.eventID,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10,
                                                              page_type='eventhub', page_id=index_number)

        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    def test_001_load_oxygen_application_and_navigate_to_event_hub_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Event Hub tab
        """
        self.site.wait_content_state(state_name='Homepage')
        sleep(5)
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_module = event_hub_content.event_hub_items_dict.get(self.module_name)
        self.assertTrue(event_hub_module, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_002_select_any_race_event_from_event_hub_tab(self):
        """
        DESCRIPTION: Select any Race event from Event Hub tab
        EXPECTED:
        """
        module = self.get_section(self.module_name)
        events = module.items_as_ordered_dict
        self.assertIn(self.race_event_name, events.keys(), msg=f'Created race event "{self.race_event_name}" is not appeared under module "{self.module_name}"')

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Event Hub tab
        EXPECTED: Race event is not displayed in application
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertFalse(module_content, msg='Event is displayed on UI')

    def test_004_refresh_the_page_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Event Hub tab
        EXPECTED: Race event is NOT displayed in application
        """
        self.device.refresh_page()
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertFalse(module_content, msg='Event is displayed on UI')

    def test_005_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: Set previously selected event to 'Displayed' and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Event Hub tab
        EXPECTED: Event is displayed on Event Hub tab
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(module_content, msg='Event is displayed on UI')
        module = self.get_section(self.module_name)
        events = module.items_as_ordered_dict
        self.assertIn(self.race_event_name, events.keys(),
                      msg=f'Created race event "{self.race_event_name}" is not appeared under module "{self.module_name}"')

    def test_006_refresh_the_page_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Event Hub tab
        EXPECTED: Event is displayed on Event Hub tab
        """
        self.device.refresh_page()
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(module_content, msg='Event is displayed on UI')
        module = self.get_section(self.module_name)
        events = module.items_as_ordered_dict
        self.assertIn(self.race_event_name, events.keys(),
                      msg=f'Created race event "{self.race_event_name}" is not appeared under module "{self.module_name}"')
