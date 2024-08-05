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
class Test_C1274039_Verify_Navigation_between_PRE_PARADE_and_WATCH_buttons(Common):
    """
    TR_ID: C1274039
    NAME: Verify Navigation between 'PRE-PARADE' and 'WATCH' buttons
    DESCRIPTION: This test case verifies Navigation between 'PRE-PARADE' and 'LIVE STREAM'
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'PRE-PARADE' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   [BMA-6588 (Quantum Leap - Horse racing visualisation)] [1]
    DESCRIPTION: *   [BMA-6585 (Racecard Layout Update - Media Area)] [2]
    DESCRIPTION: *   [BMA-17781 - Live Sim/Watch Free Display Change for Special Open Collapse Button.] [3]
    DESCRIPTION: *   [BMA-17782 (Live Sim/Watch Free Display Change for the Information Link Exception)] [4]
    DESCRIPTION: *   [BMA-39820 - Desktop HR+ GH Redesign : Race Page - Streaming redesign] [5]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-6558
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-6585
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-17781
    DESCRIPTION: [4]: https://jira.egalacoral.com/browse/BMA-17782
    DESCRIPTION: [5]: https://jira.egalacoral.com/browse/BMA-39820
    DESCRIPTION: AUTOTEST [C528051]
    PRECONDITIONS: *   Application is loaded
    PRECONDITIONS: *   Horseracing Landing page is opened
    PRECONDITIONS: *   Event is started (scheduled race-off time is reached)
    PRECONDITIONS: *   Make sure there is mapped race visualization and streaming to tested event
    PRECONDITIONS: *   User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: *   SiteServer event should be configured to support streaming
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: URL to **Test/Demo** visualization:  https://www.racemodlr.com/coral-demo/visualiser/{event id} (implemented on DEV, TST2, STG2 environments)
    PRECONDITIONS: URL to **Real **visualization: https://www.racemodlr.com/coral/visualiser/{event id} (implemented on PROD environment)
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: * URLs for 'Live Commentary' should be set in CMS:
    PRECONDITIONS: GH= https://sport.mediaondemand.net/player/ladbrokes?sport=greyhounds&showmenu=false
    PRECONDITIONS: HR= https://sport.mediaondemand.net/player/ladbrokes?sport=horses&showmenu=false
    PRECONDITIONS: To set links do the following steps:
    PRECONDITIONS: 1) Go to CMS -> System Configuration -> Structure
    PRECONDITIONS: 2) Type in Search field 'LiveCommentary'
    PRECONDITIONS: 3) Paste links in 'Field Value' per each 'Field Name'
    PRECONDITIONS: 4) Click on 'Save changes'
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page_of_verified_started_event_from_uk__ire_group(self):
        """
        DESCRIPTION: Go to the event details page of verified started event (from 'UK & IRE' group)
        EXPECTED: * Event details page is opened
        EXPECTED: * Twо buttons 'PRE-PARADE' and 'LIVE STREAM'/'WATCH' are displayed
        EXPECTED: * The area below 'PRE-PARADE' button is not expanded
        """
        pass

    def test_002_tap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Tap on the 'PRE-PARADE' button
        EXPECTED: **For Coral:**
        EXPECTED: * 'PRE-PARADE' button becomes active
        EXPECTED: * The area below 'PRE-PARADE' button is expanded
        EXPECTED: * Visualization video object is shown
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' label on button changes to 'DONE'
        """
        pass

    def test_003_tap_on_the_pre_parade_button_for_coral__done_button_for_ladbrokes(self):
        """
        DESCRIPTION: Tap on the 'PRE-PARADE' button (for Coral) / 'Done' button (for Ladbrokes)
        EXPECTED: **For Coral:**
        EXPECTED: *   The area below 'PRE-PARADE' button is collapsed
        EXPECTED: *   The information link is no longer displayed
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'DONE' button is collapsed
        EXPECTED: *   'DONE' label on button changes to 'PRE-PARADE'
        """
        pass

    def test_004_tap_on_the_watchbutton(self):
        """
        DESCRIPTION: Tap on the 'WATCH'button
        EXPECTED: *   The area below 'WATCH' button is expanded
        EXPECTED: *   'WATCH' label on button is changed to 'DONE'
        EXPECTED: *    Stream is launched
        """
        pass

    def test_005_tap_on_the_done_button(self):
        """
        DESCRIPTION: Tap on the 'DONE' button
        EXPECTED: *   The area below 'DONE' button is collapsed
        EXPECTED: *   'DONE' label on button is changed to 'WATCH'
        """
        pass

    def test_006_tap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Tap on the 'PRE-PARADE' button
        EXPECTED: **For Coral:**
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   Visualisation video object is shown
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' label on button is changed to 'DONE'
        EXPECTED: *   Visualization video object is shown
        """
        pass
