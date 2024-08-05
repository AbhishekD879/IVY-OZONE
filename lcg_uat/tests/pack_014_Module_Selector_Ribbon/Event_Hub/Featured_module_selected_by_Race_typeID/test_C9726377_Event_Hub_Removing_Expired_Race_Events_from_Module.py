import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from time import sleep
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create event hub on prod/beta
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726377_Event_Hub_Removing_Expired_Race_Events_from_Module(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C9726377
    NAME: Event Hub: Removing Expired <Race> Events from Module
    DESCRIPTION: This test case verifies that <Race> events are removed from displaying within Module on front-end
    PRECONDITIONS: 1) There are at least 2 <Race> (Select Events by - 'Race Type ID' in CMS) events in module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3) To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?
    PRECONDITIONS: translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?
    PRECONDITIONS: translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    PRECONDITIONS: 5) User is on Event Hub tab on Homepage.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Event Hub is created in CMS > Sport pages > Event hub. Module by <Race> TypeID is created in Event Hub and contains events
        PRECONDITIONS: 2. User is on Homepage > Event hub tab
        PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_id = event.event_id
        self._logger.info(f'*** Created Horse racing event name "{self.event_name}"')
        self.__class__.selections = {selection_name: selection_id for selection_name, selection_id in event.selection_ids.items()}
        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId', id=race_type_id,
                                                                             page_type='eventhub', page_id=index_number,
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10)['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number, display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get(
                                                                         'modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event_hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_find_module_with_race_events_from_preconditions(self):
        """
        DESCRIPTION: Find module with <Race> events from preconditions
        EXPECTED: Events are displayed with correct outcomes
        """
        self.site.wait_content_state(state_name='Homepage')
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        events = module_content._items_as_ordered_dict
        self.assertTrue(events, msg="event is not displayed")

        self.ob_config.change_event_state(event_id=self.event_id, displayed=False)
        self.device.refresh_page()
        sleep(10)
        event = module_content._items_as_ordered_dict

        self.assertFalse(event, msg="event is not removed from front-end")

    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        # covered in above step
