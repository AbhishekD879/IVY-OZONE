import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1274043_Verify_PRE_PARADE_for_Groups_of_Races(Common):
    """
    TR_ID: C1274043
    NAME: Verify PRE-PARADE for Groups of Races
    DESCRIPTION: This test case verifies availability of visualization (LiveSim) for Race on Event Details page under Media Area.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-6588 (Quantum Leap - Horse racing visualisation)
    DESCRIPTION: *   BMA-9298 (Upgrade Live Sim Visualisation)
    DESCRIPTION: *   BMA-9295 (Automatically Open The Live Sim Visualisation Before A Race)
    DESCRIPTION: *   BMA-17781 (Live Sim/Watch Free Display Change for Special Open Collapse Button)
    DESCRIPTION: AUTOTEST [C528111]
    PRECONDITIONS: *   Applicaiton is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    """
    keep_browser_open = True

    def test_001_go_touk__ire_group(self):
        """
        DESCRIPTION: Go to '**UK & IRE**' group
        EXPECTED: 
        """
        pass

    def test_002_open_event_details_pagemore_than_5_minutes_before_the_scheduled_race_off_time_or_open_live_event_details_page(self):
        """
        DESCRIPTION: Open event details page **more **than 5 minutes before the scheduled race-off time or open Live event details page
        EXPECTED: *     Event details page is opened
        EXPECTED: *    'PRE-PARADE' button is present under media area
        """
        pass

    def test_003_go_to_international_group(self):
        """
        DESCRIPTION: Go to '**International**' group
        EXPECTED: 
        """
        pass

    def test_004_open_event_details_pagemore_than_5_minutes_before_the_scheduled_race_off_time_or_open_live_event_details_page(self):
        """
        DESCRIPTION: Open event details page **more **than 5 minutes before the scheduled race-off time or open Live event details page
        EXPECTED: *   Event details page is opened
        EXPECTED: *   'PRE-PARADE' button is NOT present under media area
        """
        pass

    def test_005_go_to_virtual_group(self):
        """
        DESCRIPTION: Go to '**Virtual**' group
        EXPECTED: 
        """
        pass

    def test_006_open_event_details_pagemore_than_5_minutes_before_the_scheduled_race_off_time_or_open_live_event_details_page(self):
        """
        DESCRIPTION: Open event details page **more **than 5 minutes before the scheduled race-off time or open Live event details page
        EXPECTED: *   Event details page is opened
        EXPECTED: *   'PRE-PARADE' button is NOT present under media area
        """
        pass
