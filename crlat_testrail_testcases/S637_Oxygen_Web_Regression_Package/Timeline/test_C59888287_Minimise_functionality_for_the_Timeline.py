import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.timeline
@vtest
class Test_C59888287_Minimise_functionality_for_the_Timeline(Common):
    """
    TR_ID: C59888287
    NAME: 'Minimise' functionality for the Timeline
    DESCRIPTION: This test case verifies 'Minimise' functionality for the Timeline
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline
    PRECONDITIONS: should be turned ON in the general System configuration ( CMS -> 'System
    PRECONDITIONS: configuration' -> 'Structure' -> 'Feature Toggle' section -> 'Timeline')
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS (CMS -> 'Timeline
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field)
    PRECONDITIONS: 4.Design-https://app.zeplin.io/project/5dc59d1d83c70b83632e749c/
    PRECONDITIONS: screen/5fc90fb663ba1958d258d7bc(Ladbrokes)
    PRECONDITIONS: https://app.zeplin.io/project/5dc59d1d83c70b83632e749c?seid=5fc912c1dc7b8e4f009ea750(Coral)
    PRECONDITIONS: 5.Load the app
    PRECONDITIONS: 6.User is logged in
    PRECONDITIONS: 7.Navigate to the page with configured Timeline
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_tap_on_the_timeline_headerladbrokes__ladbrokes_loungecoral___coral_pulse(self):
        """
        DESCRIPTION: Tap on the Timeline header
        DESCRIPTION: Ladbrokes- Ladbrokes Lounge
        DESCRIPTION: Coral - 'Coral Pulse'
        EXPECTED: 1.Timeline should be opened and displayed in the expanded state
        EXPECTED: 2.The following attributes should be displayed in the Timeline header:
        EXPECTED: 3.
        EXPECTED: a. 'Ladbrokes Lounge' text on the left side of the header
        EXPECTED: b.'Coral Pulse' text on the left side of the header
        EXPECTED: 4.'Minimise' text on the right side of the header
        EXPECTED: 5.Configured Posts
        EXPECTED: 6.For Ladbrokes- An icon LL will be displayed in the background.
        EXPECTED: For Coral-  A plain Blue background will be displayed at the back.
        """
        pass

    def test_002_tap_on_the_minimise_text(self):
        """
        DESCRIPTION: Tap on the 'Minimise' text
        EXPECTED: Timeline should be returns to the collapsed position
        """
        pass
