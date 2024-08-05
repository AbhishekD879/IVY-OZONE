import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import stop_after_attempt, wait_fixed, retry_if_exception_type, retry


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create eventhub in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C11088157_Featured_module_by_Sport_Event_ID_Primary_Market_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C11088157
    NAME: Featured module by <Sport> Event ID: Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when the market becomes suspended in Featured module on the EventHub tab by <Sport> Event ID
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Module by <Sport> EventId(not Outright Event with the primary market) is created in EventHub and it's expanded by default.
    PRECONDITIONS: 3. A user is on Homepage > EventHub tab
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 1. List of primary markets can be found here: https://jira.egalacoral.com/browse/BMA-39433
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * Z.ZZ  - currently supported version of OpenBet SiteServer
    PRECONDITIONS: * XXXX - event ID
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def verify_price_buttons(self, is_enabled=True):
        """
        Verifies if all Price/Odds buttons are enabled/disabled and if prices is still displayed
        :param is_enabled: specifies if the buttons are expected to be enabled
        """
        self.__class__.module = self.get_section(section_name=self.module_name)
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.module.get_bet_button_by_selection_id(selection_id)
            if is_enabled:
                self.assertTrue(bet_button.is_enabled(timeout=60, expected_result=True),
                                msg=f'"{selection_name}" selection is not active in "{self.module_name}" module')
            else:
                self.assertFalse(bet_button.is_enabled(timeout=60, expected_result=False),
                                 msg=f'"{selection_name}" selection is not suspended in "{self.module_name}" module')
            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed in "{self.module_name}" module')

    def test_000_preconditions(self):
        event = self.ob_config.add_football_event_to_autotest_league2()
        self.__class__.market_id = event.default_market_id
        self.__class__.eventID = event.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=self.eventID,
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
        self.verify_price_buttons()

    def test_002_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodes_for_primary_market_market_type(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' market type
        EXPECTED: Event is suspended
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=False)
        event_status = wait_for_result(lambda: self.check_event_is_active(self.eventID), expected_result=False,
                                       name='Event is suspended',
                                       timeout=40)
        self.assertFalse(event_status, msg='Event is not suspended')

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        self.verify_price_buttons(is_enabled=False)

    def test_004_change_attribute_for_this_event_in_timarketstatuscodea_for_primary_market_market_type(self):
        """
        DESCRIPTION: Change attribute for this event in TI:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>' market type
        EXPECTED: Event is active
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=True)

    def test_005_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        self.verify_price_buttons()

    def test_006_collapse_the_module_from_the_previous_step(self):
        """
        DESCRIPTION: Collapse the module from the previous step
        EXPECTED:
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_007_change_attribute_in_ti_for_this_eventmarketstatuscodes_for_primary_market_market_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' market type
        EXPECTED:
        """
        self.test_002_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodes_for_primary_market_market_type()

    def test_008_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.verify_price_buttons(is_enabled=False)

    def test_009_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED:
        """
        self.test_006_collapse_the_module_from_the_previous_step()

    def test_010_change_attribute_in_ti_for_this_eventmarketstatuscodea_for_primary_market_market_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>' market type
        EXPECTED:
        """
        self.test_004_change_attribute_for_this_event_in_timarketstatuscodea_for_primary_market_market_type()

    def test_011_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.verify_price_buttons()
