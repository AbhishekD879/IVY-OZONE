import pytest

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl # Cannot suspend/un suspend event on prod and hl
@pytest.mark.high
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.module_ribbon
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.medium
@vtest
class Test_C29383_Featured_Event_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C29383
    NAME: Featured Event Becomes Suspended
    DESCRIPTION: Verifies correct state representation (suspended / active) of event selections on FEATURED tab
    PRECONDITIONS: 1. Modules are created and contain events/selections
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet or Desktop
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI, create football event and featured module
        EXPECTED: Football event and featured module were created
        """
        start_time = self.get_date_time_formatted_string(hours=3)
        event = self.ob_config.add_football_event_to_featured_autotest_league(start_time=start_time)
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids
        self.__class__.event_name = f'{event.team1} v {event.team2}'
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, id=type_id, show_expanded=True, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title']

        self.__class__.module_name = module_name.upper()
        self._logger.info(f'*** Feature module name is: {self.module_name}')

    def test_001_go_to_the_featured_tab_in_module_ribbon_tabs(self):
        """
        DESCRIPTION: Go to the 'Featured' tab in Module Ribbon Tabs
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected by default
        EXPECTED: **For desktop:**
        EXPECTED: 'Featured' section is displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

        self.__class__.featured_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

        if self.device_type == 'mobile':
            module_selection_ribbon = self.site.home.module_selection_ribbon
            self.__class__.tabs_bma = module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(self.tabs_bma, msg='Cannot found tabs on Oxygen Module Selector Ribbon')
            self.assertIn(self.featured_tab, self.tabs_bma,
                          msg=f'"{self.featured_tab}" tab not found in Module Selector Ribbon')
            self.assertTrue(self.tabs_bma[self.featured_tab].is_selected(),
                            msg='Featured tab is not selected by default')

        sections = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).accordions_list.items_as_ordered_dict
        self.assertIn(self.module_name, sections, msg=f'"{self.module_name}" module is not in sections')
        self.__class__.section = sections[self.module_name]

    def test_002_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices
        DESCRIPTION: (or 'SP' buttons for <Race> events)
        EXPECTED: Module is expanded
        """
        self.section.expand()
        self.assertTrue(self.section.is_expanded(),
                        msg=f'Section "{self.module_name}" is not expanded')

        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')
        self.assertIn(self.event_name, events, msg='No event "%s" found in events list "%s"'
                                                   % (self.event_name, ', '.join(events.keys())))

    def test_003_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Suspend the event in TI
        EXPECTED: Event is suspended
        """
        # TODO reimplement after VOL-1970
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertTrue(bet_button.is_enabled(timeout=3),
                            msg=f'"{selection_name}" selection is suspended for "{self.event_name}" event')

        self.ob_config.change_event_state(event_id=self.eventID, active=False, displayed=True)

    def test_004_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (prices are still displayed)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=40, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_005_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True, displayed=True)

        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertTrue(bet_button.is_enabled(timeout=40),
                            msg=f'"{selection_name}" selection is suspended for "{self.event_name}"')

    def test_006_collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices(self):
        """
        DESCRIPTION: Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices
        DESCRIPTION: (or 'SP' buttons for <Race> events)
        EXPECTED: Module is collapsed
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False),
                         msg=f'Section "{self.module_name}" is expanded')

    def test_007_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Suspend the event in TI
        EXPECTED: Event is suspended
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=False, displayed=True)

    def test_008_expand_module_from_step_6_with_the_event_and_verify_its_outcomes(self):
        """
        DESCRIPTION: Expand module from step 6 with the event and verify its outcomes
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (prices are still displayed)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        self.section.expand()
        self.assertTrue(self.section.is_expanded(),
                        msg=f'Section "{self.module_name}" is not expanded')

        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=60, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=2, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_009_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED: Module is collapsed
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False),
                         msg=f'Section "{self.module_name}" is expanded')

    def test_010_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: Event is active again
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True, displayed=True)

    def test_011_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        self.section.expand()
        self.assertTrue(self.section.is_expanded(),
                        msg=f'Section "{self.module_name}" is not expanded')

        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertTrue(bet_button.is_enabled(timeout=40),
                            msg=f'"{selection_name}" selection is suspended for "{self.event_name}" event')
