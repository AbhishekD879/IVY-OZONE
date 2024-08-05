import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot configure featured tab events in prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11087726_Featured_module_by_Sport_Event_ID_Event_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C11087726
    NAME: Featured module by <Sport> Event ID: Event Becomes Suspended
    DESCRIPTION: This test case verifies situation when event becomes suspended in Featured Event Module on the EventHub tab(mobile/tablet)
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Module by <Sport> EventId(not Outright Event with primary market) is created in EventHub and it's expanded by default.
    PRECONDITIONS: 3. User is on Homepage > EventHub tab
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: To get into SiteServer use this link:t CF and CT
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * Z.ZZ  - current supported version of OpenBet SiteServer
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

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        EXPECTED: * Configured module is displayed on Featured tab and is expanded by default
        EXPECTED: * All 'Price/Odds' buttons are active
        """
        params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = params.event_id
        self.__class__.market_id = params.default_market_id
        self.__class__.selection_ids = params.selection_ids
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        module = self.get_section(section_name=self.module_name)
        self.assertTrue(module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
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
                                       timeout=40)
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
