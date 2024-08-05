import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Need to create events which will start in 15 mins
@pytest.mark.horseracing
@pytest.mark.watch_free
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C60094974_Verify_PRE_PARADE_for_Not_Started_Race(BaseRacing):
    """
    TR_ID: C60094974
    NAME: Verify PRE-PARADE for Not Started Race
    DESCRIPTION: This test case verifies visualization (LiveSim) for Not Started Race on Event Details page under Media Area.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-6588 (Quantum Leap - Horse racing visualisation)
    DESCRIPTION: *   BMA-9298 (Upgrade Live Sim Visualisation)
    DESCRIPTION: *   BMA-9295 (Automatically Open The Live Sim Visualisation Before A Race)
    DESCRIPTION: *   BMA-17781 (Live Sim/Watch Free Display Change for Special Open Collapse Button)
    DESCRIPTION: *   BMA-17782 (Live Sim/Watch Free Display Change for the Information Link Exception)
    DESCRIPTION: AUTOTEST [C528114]
    PRECONDITIONS: *   Applicaiton is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    PRECONDITIONS: *   Event is NOT started yet
    PRECONDITIONS: *   Make sure there is mapped race visualization for tested event
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: * Create a valid user account
    PRECONDITIONS: * The user is logged out
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    """
    keep_browser_open = True

    def test_000_create_events(self):
        """
        DESCRIPTION: Add racing event with start time more than 15 minutes to UK & IRE, International and Virtual types
        EXPECTED: Racing event added
        """
        event_params = self.ob_config.add_UK_racing_event(time_to_start=15, at_races_stream=True)
        self.__class__.eventID, event_off_time = event_params.event_id, event_params.event_off_time
        self._logger.info(f'*** Created event with ID {self.eventID}')
        self.__class__.created_event_name = f'{event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'

    def test_001_go_to_a_hr_event_from_uk__ire_groupmore_than_15_minutes_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Go to a HR event (from 'UK & IRE' group) **more than 15 minutes** before the scheduled race-off time
        EXPECTED: * Event details page is opened
        EXPECTED: * Media area consists of ' PRE-PARADE' and 'LIVE STREAM'/'WATCH' buttons
        EXPECTED: * The Button 'PRE-PARADE' button is inActive by default and not auto-expanded
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(horse_racing_edp.has_watch_free_button(),
                        msg=f'"Pre-Parade" button was not found for event "{self.created_event_name}"')
        self.assertTrue(horse_racing_edp.video_stream_button.is_displayed(),
                        msg=f'"{horse_racing_edp.video_stream_button.name}" button is not displayed')
        self.assertFalse(horse_racing_edp.watch_free_button.is_selected(
            expected_result=False),
            msg='"PRE-PARADE" button is active')
        result = wait_for_result(lambda: horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video area',
                                 poll_interval=5,
                                 timeout=30)
        self.assertFalse(result, msg='Pre-Parade area is expanded')

    def test_002_refresh_the_page_when_theresmore_than_5_minutes_left_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Refresh the page when there's **more than 5 minutes** left before the scheduled race-off time
        EXPECTED: *   The area below 'PRE-PARADE' button is collapsed
        EXPECTED: *   'PRE-PARADE' button is inActive
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        # To avoid stale element exception , reintialized it
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(
            expected_result=False),
            msg='"PRE-PARADE" button is active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertFalse(result, msg='Visualisation video is shown')

    def test_003_clicktap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' button
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   Visualisation is shown for logged out user
        EXPECTED: *   'PRE-PARADE' button becomes 'DONE' (Mobile, Tablet and Desktop)
        """
        self.horse_racing_edp.watch_free_button.click()
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg='"PRE-PARADE" button is not active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is not shown')
        result = wait_for_result(lambda: self.horse_racing_edp.watch_free_button.name == vec.sb.DONE.upper(),
                                 name='"PRE_PARADE" button to become "DONE"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Button "{self.horse_racing_edp.watch_free_button.name}"'
                                    f' did not change label to "{vec.sb.DONE.upper()}"')

    def test_004_clicktap_on_the_done_button(self):
        """
        DESCRIPTION: Click/Tap on the 'DONE' button
        EXPECTED: * The area below 'DONE' button is collapsed
        EXPECTED: * 'DONE' label on button changes to 'PRE-PARADE'
        """
        self.horse_racing_edp.watch_free_button.click()
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(expected_result=False),
                         msg='"PRE-PARADE" button is active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertFalse(result, msg='Visualisation video is shown')
        result = wait_for_result(lambda: self.horse_racing_edp.watch_free_button.name == vec.sb.PRE_PARADE.upper(),
                                 name='"DONE" button to become "PRE-PARADE"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Button "{self.horse_racing_edp.watch_free_button.name}"'
                                    f' did not change label to "{vec.sb.PRE_PARADE.upper()}"')

    def test_005_log_in_with_the_user_from_preconditions(self):
        """
        DESCRIPTION: Log in with the user from preconditions
        EXPECTED: The user is logged in
        """
        self.site.login()

    def test_006_clicktap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' button
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' button becomes Active
        EXPECTED: *   Visualisation is shown for  logged in user
        EXPECTED: *   'PRE-PARADE' button becomes 'DONE' (Mobile, Tablet and Desktop)
        """
        self.test_003_clicktap_on_the_pre_parade_button()

    def test_007_clicktap_on_the_done_button(self):
        """
        DESCRIPTION: Click/Tap on the 'DONE' button
        EXPECTED: *   The area below 'PRE-PARADE' button is collapsed
        """
        self.test_004_clicktap_on_the_done_button()
