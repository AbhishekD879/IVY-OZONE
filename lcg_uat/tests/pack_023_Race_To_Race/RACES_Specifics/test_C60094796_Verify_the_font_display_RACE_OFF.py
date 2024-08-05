from random import randint
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import pytest
import tests


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # creation of events involved
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C60094796_Verify_the_font_display_RACE_OFF(BaseRacing):
    """
    TR_ID: C60094796
    NAME: Verify the font display "RACE OFF"
    DESCRIPTION: Ladbrokes: Verify that "RACE OFF" is displayed in red color font with color code : #ff0000.
    DESCRIPTION: Coral: Verify that "RACE OFF" is displayed in Orange color font with color code : #f56b23.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should kick start
    """
    keep_browser_open = True
    lad_race_off_color_code = 'rgba(255, 0, 0, 1)'
    cora_race_off_color_code = 'rgba(245, 107, 35, 1)'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env != 'prod':
            minutes = randint(40, 50)
            start_time = self.get_date_time_formatted_string(minutes=-minutes)
            event_params = self.ob_config.add_UK_racing_event(start_time=start_time, cashout=True, is_live=True)
            self.__class__.event_id = event_params.event_id

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        # covered in step 001

    def test_003_click_on_any_race_off_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any "RACE OFF" race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        events = self.site.racing_event_details.tab_content.has_event_off_times_list()
        self.assertTrue(events, msg='other races not found')

    def test_004_validate_race_off_status_font(self):
        """
        DESCRIPTION: Validate "RACE OFF" status font
        DESCRIPTION: ![](index.php?/attachments/get/111160928)
        DESCRIPTION: ![](index.php?/attachments/get/111160929)
        EXPECTED: Ladbrokes:
        EXPECTED: 1: User should be displayed with "RACE OFF" status.
        EXPECTED: 2: "RACE OFF" status should be displayed in red color font with color code : #ff0000.
        EXPECTED: Coral:
        EXPECTED: 1: User should be displayed with "RACE OFF" status.
        EXPECTED: 2: "RACE OFF" status should be displayed in orange color font with color code : #f56b23.
        """
        races = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        race = races.get(self.site.racing_event_details.tab_content.event_off_times_list.selected_item)
        race_off_label = race.race_off_element()
        c_code = race_off_label.value_of_css_property('color')
        if self.brand == 'bma':
            self.assertEqual(c_code, self.cora_race_off_color_code, msg='race off color codes are not equal')
        else:
            self.assertEqual(c_code, self.lad_race_off_color_code, msg='race off color codes are not equal')
