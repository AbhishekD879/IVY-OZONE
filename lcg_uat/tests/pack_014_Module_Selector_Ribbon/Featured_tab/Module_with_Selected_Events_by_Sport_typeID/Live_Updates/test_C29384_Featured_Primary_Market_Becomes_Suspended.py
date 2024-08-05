import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod  # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29384_Featured_Primary_Market_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C29384
    NAME: Featured: Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when market/markets become suspended on event landing page on the 'Featured' tab(mobile/tablet)/ Featured section (desktop)
    PRECONDITIONS: 1. Modules are created and contain events/selections
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet or Desktop
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI, create football event and featured module
        EXPECTED: Football event and featured module were created
        """
        self.site.wait_content_state("Homepage")
        start_time = self.get_date_time_formatted_string(hours=3)
        event = self.ob_config.add_football_event_to_featured_autotest_league(start_time=start_time)
        self.__class__.eventID = event.event_id
        self.__class__.market_id = event.default_market_id
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
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        self.wait_for_featured_module(name=self.module_name)

        self.featured_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

        if self.device_type == 'mobile':
            module_selection_ribbon = self.site.home.module_selection_ribbon
            self.tabs_bma = module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(self.tabs_bma, msg='Cannot found tabs on Oxygen Module Selector Ribbon')
            self.assertIn(self.featured_tab, self.tabs_bma,
                          msg=f'"{self.featured_tab}" tab not found in Module Selector Ribbon')
            self.assertTrue(self.tabs_bma[self.featured_tab].is_selected(),
                            msg='Featured tab is not selected by default')

        sections = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).accordions_list.items_as_ordered_dict
        self.assertIn(self.module_name, sections, msg=f'"{self.module_name}" module is not in sections')
        self.__class__.section = sections[self.module_name]

    def test_002_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED:
        """
        self.section.expand()
        self.assertTrue(self.section.is_expanded(),
                        msg=f'Section "{self.module_name}" is not expanded')

        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')
        self.assertIn(self.event_name, events, msg='No event "%s" found in events list "%s"'
                                                   % (self.event_name, ', '.join(events.keys())))

    def test_003_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodesfor_primary_market_or_win_or_each_way_for_races_market_type(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' (or 'Win Or Each Way' for <Races>) market type
        EXPECTED: Event is suspended
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.market_id, active=False, displayed=True)

    def test_004_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=40, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_005_change_attribute_for_this_event_in_timarketstatuscodeafor_primary_market_or_win_or_each_way_for_racesmarket_type(self):
        """
        DESCRIPTION: Change attribute for this event in TI:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>'  (or 'Win Or Each Way' for <Races>) market type
        EXPECTED: Event is active
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.market_id, active=True, displayed=True)

    def test_006_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertTrue(bet_button.is_enabled(timeout=40),
                            msg=f'"{selection_name}" selection is suspended for "{self.event_name}"')

    def test_007_collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED:
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False),
                         msg=f'Section "{self.module_name}" is expanded')

    def test_008_change_attribute_in_ti_for_this_eventmarketstatuscodesfor_primary_market_or_win_or_each_way_for_racesmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>'  (or 'Win Or Each Way' for <Races>) market type
        EXPECTED:
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.market_id, active=False, displayed=True)

    def test_009_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
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

    def test_010_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED:
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False),
                         msg=f'Section "{self.module_name}" is expanded')

    def test_011_change_attribute_in_ti_for_this_eventmarketstatuscodeafor_primary_market_or_win_or_each_way_for_racesmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>'  (or 'Win Or Each Way' for <Races>) market type
        EXPECTED:
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.market_id, active=True, displayed=True)

    def test_012_expand_module_and_verify_outcomes_for_the_event(self):
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
