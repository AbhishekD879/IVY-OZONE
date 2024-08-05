import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2986504_Verify_events_on_Races_event_details_page_from_Next_Races_module(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2986504
    NAME: Verify events on <Races> event details page from 'Next Races' module
    DESCRIPTION: This test case verifies events on <Races> EDP when navigating from 'Next Races' module
    PRECONDITIONS: 1. 'Next Races' module is configured in CMS on:
    PRECONDITIONS: - Horse Racing > 'Featured' tab
    PRECONDITIONS: - [NOT YET IMPLEMENTED] Horse Racing > 'Next Races' tab
    PRECONDITIONS: - Home Page > 'Next Races' tab
    PRECONDITIONS: 2. 'Next Races' are available on Greyhounds > 'Today' tab
    PRECONDITIONS: 3. Events from different <Types> are available within 'Next Races' module
    PRECONDITIONS: 4. App is loaded
    PRECONDITIONS: 5. Home page > 'Next Races' tab is opened
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        if cls.horse_racing_isVirtualRaces_Enabled_status == 'Yes':
            cms_config.update_system_configuration_structure(config_item='NextRaces',
                                                              field_name='isVirtualRacesEnabled',
                                                              field_value='Yes')
        if cls.greyhound_isVirtualRaces_Enabled_status == 'Yes':
            cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                                  field_name='isVirtualRacesEnabled',
                                                                  field_value='Yes')


    def test_000_preconditions(self):
        """
            PRECONDITIONS: 1. 'Next Races' module is configured in CMS
            PRECONDITIONS: 2. In CMS > structure > Nextraces ,change 'isVirtualRacesEnabled' to No if yes
        """
        if tests.settings.backend_env != 'prod':
            next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
            if not next_races_toggle:
                next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
            if not next_races_toggle.get('nextRacesComponentEnabled'):
                self._logger.warning('*** "NextRacesToggle -> nextRacesComponentEnabled" component is disabled. Needs '
                                     'to be enabled')
                self.cms_config.set_next_races_toggle_component_status(next_races_component_status=True)
        self.__class__.horse_racing_isVirtualRaces_Enabled_status = self.cms_config.get_system_configuration_structure()['NextRaces']['isVirtualRacesEnabled']
        self.__class__.greyhound_isVirtualRaces_Enabled_status = self.cms_config.get_system_configuration_structure()['GreyhoundNextRaces']['isVirtualRacesEnabled']
        if self.horse_racing_isVirtualRaces_Enabled_status == 'Yes':
            self.cms_config.update_system_configuration_structure(config_item='NextRaces',
                                                                  field_name='isVirtualRacesEnabled',
                                                                  field_value='No')
            wait_for_haul(5)
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('HorseRacing', timeout=20)

    def test_001_tap_on_any_event_from_next_races(self, sport='HR'):
        """
        DESCRIPTION: Tap on any event from 'Next Races'
        EXPECTED: - <Races> event details page is opened
        EXPECTED: - Corresponding 'Event Time' tab is selected and visible
        """
        if self.brand == 'ladbrokes':
            if sport == 'HR':
                current_tab = self.site.horse_racing.tabs_menu.current
                if current_tab != vec.racing.RACING_NEXT_RACES_NAME:
                    self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
                    current_tab = self.site.horse_racing.tabs_menu.current
                self.assertTrue(current_tab,
                                msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
                sections = self.get_sections('horse-racing')
            else:
                grey_hound_next_races_tab = self.site.greyhound.tabs_menu.current
                if grey_hound_next_races_tab != vec.racing.RACING_NEXT_RACES_NAME:
                    self.site.greyhound.tabs_menu.items_as_ordered_dict.get(vec.racing.RACING_NEXT_RACES_NAME).click()
                    grey_hound_next_races_tab = self.site.greyhound.tabs_menu.current
                self.assertTrue(grey_hound_next_races_tab,
                                msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
                sections = self.get_sections('greyhound-racing')
            wait_for_haul(5)
            for section_name, section in sections.items():
                if section.sub_header.has_e_w_and_places():
                    runners = section.runners.items_as_ordered_dict
                    self.assertTrue(runners, msg=f'No runners found in racing card "{section_name}"')
                    if self.device_type != 'desktop':
                        runner_name, runner = list(runners.items())[0]
                        runner.click()
                    else:
                        section.scroll_to()
                        if section.header.more_link:
                            section.header.more_link.click()
                break
        else:
            next_races = self.get_next_races_section()
            events = next_races.items_as_ordered_dict
            self.assertTrue(events, msg='No events were found in Next races section')
            _, event = list(events.items())[0]
            event.click()
            sleep(3)
        if sport == 'HR':
            self.site.wait_content_state(state_name='RacingEventDetails', timeout=20)
        else:
            self.site.wait_content_state(state_name='GreyHoundEventDetails', timeout=20)

    def test_002_verify_event_time_tabs(self):
        """
        DESCRIPTION: Verify 'Event Time' tabs
        EXPECTED: Only 'Event Time' tabs that are available in 'Next Races' module are displayed
        EXPECTED: (Events from different <Types> of <Races>)
        """
        # covered in step 003

    def test_003_navigate_through_event_time_tabs(self, sport='HR'):
        """
        DESCRIPTION: Navigate through 'Event Time' tabs
        EXPECTED: Corresponding events from 'Next Races' module are displayed
        """
        if sport == 'HR':
            events_list = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
            default_event = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        else:
            events_list = self.site.greyhound_event_details.tab_content.event_off_times_list.items_as_ordered_dict
            default_event = self.site.greyhound_event_details.tab_content.event_off_times_list.selected_item
        for event_name in events_list.keys():
            if event_name == default_event:
                continue
            if sport == 'HR':
                events_list = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
            else:
                events_list = self.site.greyhound_event_details.tab_content.event_off_times_list.items_as_ordered_dict
            events_list[event_name].click()
            self.assertTrue(event_name, msg=f'"{event_name}" event time tab is not displayed')

    def test_004_repeat_steps_1_3_for__horse_racing__featured_tab__next_races_modulenot_yet_implemented__horse_racing__next_races_tab__greyhounds__today_tab(
            self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Horse Racing > 'Featured' tab > 'Next Races' module
        DESCRIPTION: [NOT YET IMPLEMENTED]- Horse Racing > 'Next Races' tab
        DESCRIPTION: - Greyhounds > 'Today' tab
        EXPECTED:
        """
        if self.greyhound_isVirtualRaces_Enabled_status == 'Yes':
            self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                                  field_name='isVirtualRacesEnabled',
                                                                  field_value='No')
            wait_for_haul(5)
        if self.brand != 'ladbrokes':
            self.navigate_to_page(name='greyhounds')
            self.site.wait_content_state('Greyhounds')
        else:
            self.navigate_to_page(name='greyhound-racing')
            self.site.wait_content_state('Greyhoundracing')
        self.test_001_tap_on_any_event_from_next_races(sport='GR')
        self.test_003_navigate_through_event_time_tabs(sport='GR')