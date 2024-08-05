import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # We can not create event in prod
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094976_Verify_that_the_PRE_PARADE_is_not_auto_launched(BaseRacing):
    """
    TR_ID: C60094976
    NAME: Verify that the PRE-PARADE  is not auto-launched
    DESCRIPTION: This test case verifies visualization (LiveSim) auto opening on Event Details page under Media Area.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-6588 (Quantum Leap - Horse racing visualisation)
    DESCRIPTION: *   BMA-9298 (Upgrade Live Sim Visualisation)
    DESCRIPTION: *   BMA-9295 (Automatically Open The Live Sim Visualisation Before A Race)
    DESCRIPTION: *   BMA_17781 - (Live Sim/Watch Free Display Change for Special Open Collapse Button)
    DESCRIPTION: *   BMA-17782 (Live Sim/Watch Free Display Change for the Information Link Exception)
    DESCRIPTION: *   BMA-52028 - Live Sim - Stop Auto Launch
    DESCRIPTION: AUTOTEST [C528112]
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    PRECONDITIONS: * Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add racing events with different start time :
        DESCRIPTION: UK & IRE
        EXPECTED: Racing events added
        """
        self.__class__.event_6min = self.ob_config.add_UK_racing_event(is_live=True,
                                                                       at_races_stream=True, time_to_start=10)
        self.__class__.event_5min = self.ob_config.add_UK_racing_event(is_live=True,
                                                                       at_races_stream=True, time_to_start=5)
        self.__class__.event_4min = self.ob_config.add_UK_racing_event(is_live=True,
                                                                       at_races_stream=True, time_to_start=4)

    def verify_media_area_with_diff_event(self, event_id):
        self.navigate_to_edp(event_id=event_id.event_id, sport_name='horse-racing')
        horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(horse_racing_edp.watch_free_button.is_displayed(),
                        msg=f'"PRE-PARADE" button is not displayed')
        self.assertTrue(horse_racing_edp.video_stream_button.is_displayed(),
                        msg=f'"{horse_racing_edp.watch_free_button.name}" button is not active')
        result = wait_for_result(lambda: horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertFalse(result, msg='Visualisation video is shown')

    def test_001_go_to_the_event_details_page_of_a_race_from_uk__ire_group_more_than_5_minutes_before_the_race_off_time(
            self):
        """
        DESCRIPTION: Go to the event details page of a race (from 'UK & IRE' group) **more than 5 minutes** before the race off time
        EXPECTED: Event details page is opened
        """
        self.verify_media_area_with_diff_event(event_id=self.event_6min)

    def test_002_navigate_to_media_area(self):
        """
        DESCRIPTION: Navigate to media area
        EXPECTED: * Media area consists of 'PRE-PARADE' button and 'WATCH'' button
        EXPECTED: * The 'PRE-PARADE ' video is not expanded automatically
        """
        # Covered in above step

    def test_003_stay_on_event_details_page_and_verify_visualisations_automatic_launching__5_minutes_before_the_race_off_time(
            self):
        """
        DESCRIPTION: Stay on Event Details page and verify Visualisations automatic launching  **5 minutes** before the race off time
        EXPECTED: * Media area consists of 'PRE-PARADE' button and 'WATCH'' button
        EXPECTED: * The 'PRE-PARADE ' video is not expanded automatically
        """
        self.verify_media_area_with_diff_event(event_id=self.event_5min)

    def test_004_go_to_the_event_details_page_of_a_race_from_uk__ire_group_less_than_5_minutes_before_the_race_off_time(
            self):
        """
        DESCRIPTION: Go to the event details page of a race (from 'UK & IRE' group)  **less than 5 minutes** before the race off time
        EXPECTED: * Media area consists of 'PRE-PARADE' button and 'WATCH' button
        EXPECTED: * The 'PRE-PARADE ' video is not expanded automatically
        """
        self.verify_media_area_with_diff_event(event_id=self.event_4min)

    def test_005_repeat_steps_1_4_with__weak_internet_for_example_slow_3g__lockunlock_devices(self):
        """
        DESCRIPTION: Repeat steps #1-4 with:
        DESCRIPTION: - Weak Internet (for example, slow 3G)
        DESCRIPTION: - Lock/Unlock devices
        """
        # Can not be automated
