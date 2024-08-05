import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot suspend the events in beta/Prod TI
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C11114608_Featured_module_by_Market_ID_Event_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C11114608
    NAME: Featured module by Market ID: Event Becomes Suspended
    DESCRIPTION: This test case verifies situation when an event becomes suspended in Featured Event Module on the EventHub tab(mobile/tablet) of a module by MarketID
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Featured module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in the previously created EventHub and it's expanded by default.
    PRECONDITIONS: 3. A user is on Homepage > EventHub tab
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

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        EXPECTED: * The configured module is displayed on Featured tab and is expanded by default
        EXPECTED: * All 'Price/Odds' buttons are active
        """
        self.site.wait_content_state_changed(timeout=30)
        sleep(3)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=30)
        self.site.wait_content_state(state_name='Homepage')
        sleep(5)
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

    def test_002_in_ti_find_event_from_the_created_module_and_suspend_it(self):
        """
        DESCRIPTION: In TI find Event from the created module and suspend it
        EXPECTED: Event is suspended
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
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

    def test_004_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_price_buttons()

    def test_005_collapse_the_module_from_the_previous_step_and_suspend_the_event_from_the_module(self):
        """
        DESCRIPTION: Collapse the module from the previous step and suspend the Event from the module
        EXPECTED: Event is suspended
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        event_status = wait_for_result(lambda: self.check_event_is_active(self.eventID), expected_result=False,
                                       name='Event is suspended',
                                       timeout=60)
        self.assertFalse(event_status, msg='Event is not suspended')

    def test_006_expand_module_from_step_5_with_the_event_and_verify_its_outcomes(self):
        """
        DESCRIPTION: Expand module from step 5 with the event and verify its outcomes
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.verify_price_buttons(is_enabled=False)

    def test_007_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED:
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_008_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: Event is active again
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        event_status = wait_for_result(lambda: self.check_event_is_active(self.eventID),
                                       name='Event is active', timeout=40)
        self.assertTrue(event_status, msg='Event is not active')

    def test_009_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.verify_price_buttons()
