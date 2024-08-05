import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C1274042_Verify_PRE_PARADE_for_Not_Started_Race(Common):
    """
    TR_ID: C1274042
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

    def test_001_go_to_a_hr_event_from_uk__ire_groupmore_than_15_minutes_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Go to a HR event (from 'UK & IRE' group) **more than 15 minutes** before the scheduled race-off time
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Event details page is opened
        EXPECTED: * Media area consists of ' PRE-PARADE' and 'LIVE STREAM'/'WATCH' buttons and not auto-expanded
        EXPECTED: **For Desktop:**
        EXPECTED: * Event details page is opened
        EXPECTED: * Media area consists of ' PRE-PARADE' and 'LIVE STREAM'/'WATCH' buttons
        EXPECTED: * The Button 'PRE-PARADE' button is inActive by default and not auto-expanded
        EXPECTED: * Relevant icon is NOT shown next to the ' PRE-PARADE' label
        """
        pass

    def test_002_refresh_the_page_when_theresmore_than_5_minutes_left_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Refresh the page when there's **more than 5 minutes** left before the scheduled race-off time
        EXPECTED: *   The area below 'PRE-PARADE' button is collapsed
        EXPECTED: *   'PRE-PARADE' button is inActive
        """
        pass

    def test_003_clicktap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' button
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   Content of Quantum Leap iFrame is shown
        EXPECTED: *   Visualisation is shown for logged out user
        EXPECTED: *   An information link labeled "Find out more about Watch Free here" appears under Media Area on the page **for Mobile/Tablet on Coral**
        EXPECTED: *   'PRE-PARADE' button becomes 'DONE' on **Ladbrokes** (Mobile, Tablet and Desktop)
        """
        pass

    def test_004_clicktap_on_the_pre_parade_coral__done_ladbrokes_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' (Coral) / 'DONE' (Ladbrokes) button
        EXPECTED: For Coral:
        EXPECTED: * The area below 'PRE-PARADE' button is collapsed
        EXPECTED: * The information link is no longer displayed
        EXPECTED: For Ladbrokes:
        EXPECTED: * The area below 'DONE' button is collapsed
        EXPECTED: * 'DONE' label on button changes to 'PRE-PARADE'
        """
        pass

    def test_005_log_in_with_the_user_from_preconditions(self):
        """
        DESCRIPTION: Log in with the user from preconditions
        EXPECTED: The user is logged in
        """
        pass

    def test_006_clicktap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' button
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' button becomes Active
        EXPECTED: *   Content of Quantum Leap iFrame is shown
        EXPECTED: *   Visualisation is shown for  logged in user
        EXPECTED: *   An information link labeled "Find out more about Watch Free here" appears under Media Area on the page **for Mobile/Tablet on Coral**
        EXPECTED: *   'PRE-PARADE' button becomes 'DONE' on **Ladbrokes** (Mobile, Tablet and Desktop)
        """
        pass

    def test_007_clicktap_on_the_pre_parade_coral__done_ladbrokes_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' (Coral) / 'DONE' (Ladbrokes) button
        EXPECTED: *   The area below 'PRE-PARADE' button is collapsed
        EXPECTED: *   The information link is no longer displayed **for Mobile/Tablet on Coral**
        """
        pass
