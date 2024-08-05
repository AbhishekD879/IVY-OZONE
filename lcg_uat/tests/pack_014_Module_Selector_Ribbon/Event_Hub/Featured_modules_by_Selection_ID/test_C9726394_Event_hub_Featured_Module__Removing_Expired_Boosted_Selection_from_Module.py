import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C9726394_Event_hub_Featured_Module__Removing_Expired_Boosted_Selection_from_Module(BaseFeaturedTest):
    """
    TR_ID: C9726394
    NAME: Event hub: Featured Module - Removing Expired Boosted Selection from Module
    DESCRIPTION: This test case verifies that Boosted Selection is removed from displaying within Event Hub Module on front-end
    PRECONDITIONS: 1) There is a Selection (Select Events by - 'Selection' in CMS) in module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3) To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    PRECONDITIONS: 5) User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        event = self.ob_config.add_UK_racing_event(time_to_start=2,
                                                   number_of_runners=2, lp_prices={0: '1/2', 1: '3/2'})
        self.__class__.eventID = event.event_id
        selection_id = list(event.selection_ids.items())[0][1]
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                              query_builder=self.ss_query_builder)
        markets = self.event_resp[0]['event']['children']
        outcomes = next(((market['market'].get('children')) for market in markets), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        self.__class__.outcome_name1 = outcomes[0]["outcome"]["name"]

        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Selection',
                                                              id=selection_id,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.__class__.event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(self.event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')

    def test_001_find_module_with_a_selection_from_preconditions(self):
        """
        DESCRIPTION: Find module with a Selection from preconditions
        EXPECTED: Selection is displayed with correct outcome
        """
        event_hub_modules = self.event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        self.__class__.module = self.get_section(self.module_name)
        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')
        bet_buttons = self.module.get_available_prices()
        self.assertTrue(bet_buttons, msg=f'No selections found: "{bet_buttons}"')
        bet_button = bet_buttons.get(self.outcome_name1)
        self.assertTrue(bet_button,
                        msg=f'"{self.outcome_name1}" selection bet button is not found within module "{self.module_name}"')

    def test_002_trigger_completionexpiration_one_of_the_event_that_include_the_selection(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the event that include the selection
        EXPECTED: The Selection of completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False)
        self.device.refresh_page()
        bet_buttons = self.module.get_available_prices()
        self.assertFalse(bet_buttons, msg=f'No selection is not removed from the front end"')
