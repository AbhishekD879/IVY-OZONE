import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create event hub in prod
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726260_Event_Hub_Verify_Module_is_removed_from_Event_Hub_when_there_are_no_events_to_display_if_module_is_disabled(Common):
    """
    TR_ID: C9726260
    NAME: Event Hub: Verify Module is removed from Event Hub when there are no events to display if module is disabled
    DESCRIPTION: This test case verifies that Module is not present if there are no available events to display or if 'Enabled' field in CMS is unchecked.
    DESCRIPTION: To be run on mobile, tablet
    PRECONDITIONS: 1) 2 Featured Modules with at least 2 events in each created in CMS > Sport Pages > Event Hub > Edit Event Hub. Modules are Active and are displayed on Event Hub tab in app.
    PRECONDITIONS: 2) CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1) 2 Featured Modules created in CMS > Sport Pages > Event Hub > Edit Event Hub. Modules are Active and are displayed on Event Hub tab in app.
        """
        event_params1 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID1 = event_params1.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_data = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID1, page_type='eventhub', page_id=index_number,
            events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10)
        self.__class__.module_name = self.module_data['title'].upper()
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
                                 name=f'Event_hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')
        self.site.wait_content_state_changed(timeout=5)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_001_go_to_cms_and_uncheck_active_for_the_first_module___click_save_button(self):
        """
        DESCRIPTION: Go to CMS and uncheck 'Active' for the first Module -> click 'Save' button
        """
        self.cms_config.update_featured_tab_module(module_id=self.module_data['id'], enabled=False)

    def test_002_verify_module_area_in_app(self):
        """
        DESCRIPTION: Verify Module Area in app
        EXPECTED: Module is removed from Event Hub tab
        """
        self.site.wait_content_state_changed(timeout=40)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertFalse(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_003_go_to_cms_event_hub_featured_module_page_and_click_remove_all_in_events_in_module_section_for_second_module___click_save_button(self):
        """
        DESCRIPTION: Go to CMS (Event Hub> Featured module page) and click 'Remove all' in 'Events in Module section' for second Module -> click 'Save' button
        """
        self.test_000_preconditions()
        self.cms_config.update_featured_tab_module(module_id=self.module_data['id'], data=[])

    def test_004_verify_module_area_in_app(self):
        """
        DESCRIPTION: Verify Module Area in app
        EXPECTED: Module is removed from Event Hub tab
        """
        self.test_002_verify_module_area_in_app()
