import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094801_Verify_that_in_races_status_in_Next_races(BaseRacing):
    """
    TR_ID: C60094801
    NAME: Verify that in races status in Next races
    DESCRIPTION: Verify that in Next races tab no status should display as the tab contains only the future races.
    PRECONDITIONS: 1: Horse racing events should be available in Next races tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1: Horse racing events should be available in Next races tab
        PRECONDITIONS: "Next Races" should  be enabled in CMS (CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for HorseRacing in CMS')
        self.setup_cms_next_races_number_of_events()

        if tests.settings.backend_env != 'prod':
            type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
            self.check_and_setup_cms_next_races_for_type(type_id=type_id)
            self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=2)

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_race_from_next_races_tab(self):
        """
        DESCRIPTION: Click on any race from Next races tab
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other available races from Next race tab should be displayed
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(
            self.next_races_title)
        self.assertTrue(sections, msg=f'No "{self.next_races_title}" tab found')
        meetings = sections.items_as_ordered_dict
        self.assertTrue(meetings, msg='No meetings found')
        event = list(meetings.values())[0 if len(list(meetings)) == 1 else len(list(meetings)) - 1]
        event.full_race_card.click()
        self.site.wait_content_state('RacingEventDetails', timeout=30)
        self.event_off_times_list = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        self.assertTrue(self.event_off_times_list, msg='Horse racing events time panel is not displayed')
        for event_name, event in self.event_off_times_list.items():
            self.assertFalse(event.is_resulted, msg=f'Event : "{event_name}" is resulted')
            self.assertFalse(event.is_race_off(), msg=f'Event : "{event_name}" have race off label')

    def test_004_validate_status(self):
        """
        DESCRIPTION: Validate Status
        EXPECTED: 1: User should not be able to view any status in Next races.
        """
        # covered in the step test_003
