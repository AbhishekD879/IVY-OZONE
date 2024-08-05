import pytest
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C11386070_Event_Hub_Verify_module_is_removed_from_Featured_when_event_is_finished(BaseHighlightsCarouselTest):
    """
    TR_ID: C11386070
    NAME: Event Hub: Verify module is removed from Featured when event is finished
    DESCRIPTION: This test case verifies module is removed from Event Hub tab when event is finished
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 3. Featured module by Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 4. User is on Homepage > Event Hub tab
    PRECONDITIONS: 5. To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        event = self.ob_config.add_american_football_outright_event_to_autotest_league(selections_number=3)
        market_id = event.default_market_id
        self.__class__.eventID = event.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Market',
                                                              id=market_id,
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

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_find_module_from_preconditions(self):
        """
        DESCRIPTION: Find module from preconditions
        EXPECTED: Module displayed with correct event/outcomes
        """
        sleep(30)
        self.site.wait_content_state(state_name='Homepage')
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        sleep(15)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_module}" tab')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: * Live update with type EVENT is received in WS with attribute 'displayed="N"
        EXPECTED: * Module is removed from Featured tab
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        self.site.wait_splash_to_hide()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        sleep(40)
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertFalse(event_hub_modules, msg=f'Modules found on "{self.event_hub_tab_name}" tab')
