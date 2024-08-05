import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot suspend events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C29393_Not_Primary_Market_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C29393
    NAME: Not Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when market/markets become suspended on event landing page on the 'Featured' tab (mobile/tablet)/ Featured section (desktop)
    DESCRIPTION: NOTE, UAT assistance is needed for live updates
    DESCRIPTION: NOTE, **User Story** BMA-2451 Feature tab: Live serve price updates
    PRECONDITIONS: To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: ***Boosted selection - this is ******an ******event****** with only one selection which is shown on the 'Featured' tab. ***
    PRECONDITIONS: ***On CMS it  is configured as event shown by selection id.***
    PRECONDITIONS: **NOTE:** **LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events**
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

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_go_to_the_featured_tab_in_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to the 'Featured' tab in Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
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
        sleep(10)
        sections = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).accordions_list.items_as_ordered_dict
        self.assertIn(self.module_name, sections, msg=f'"{self.module_name}" module is not in sections')
        self.__class__.section = sections[self.module_name]

    def test_003_in_the_featured_tab_find_boosted_selection(self):
        """
        DESCRIPTION: In the 'Featured' tab find boosted selection
        EXPECTED: Event with a boosted selection is shown
        """
        # Covered in pre-conditions

    def test_004_trigger_the_following_situation_for_this_eventmarketstatuscodesfor_market_type_boosted_selection_belongs_to(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="S"**
        DESCRIPTION: for  market type boosted selection belongs to
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=False, displayed=True)
        sleep(10)  # Takes time to reflect suspension of event

    def test_005_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: *   Price/Odds button of this event immediately start displaying "S"
        EXPECTED: *   Price/Odds button is disabled
        """
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=40, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_006_change_attribute_for_this_eventmarketstatuscodeafor_market_type_boosted_selection_belongs_to(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: for market type boosted selection belongs to
        EXPECTED:
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True, displayed=True)

    def test_007_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: *   Price/Odds button of this event is not disabled anymore
        EXPECTED: *   Price / Odds button displays prices immediately
        """
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertTrue(bet_button.is_enabled(timeout=40),
                            msg=f'"{selection_name}" selection is suspended for "{self.event_name}"')
