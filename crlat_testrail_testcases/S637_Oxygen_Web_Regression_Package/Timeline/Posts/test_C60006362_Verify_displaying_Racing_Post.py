import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.timeline
@vtest
class Test_C60006362_Verify_displaying_Racing_Post(Common):
    """
    TR_ID: C60006362
    NAME: Verify displaying Racing Post
    DESCRIPTION: This test case verifies displaying Racing Post
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.Campaign should be configured
    PRECONDITIONS: 5.'Spotlight' and 'Verdict' Templates should be configured
    PRECONDITIONS: 6.Spotlight and Verdict Posts should be created and published (CMS -> 'Timeline' section -> 'Timeline Campaign' item -> 'Spotlights' button)-> -> Insert classIds in the 'Fetch for classIds' field (e.g. 226,223)-> Click 'Refresh Events' button-> -> Click on the event time of the one event-> Click 'Create Post' in Spotlight/Verdict section)
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_load_the_app__gt_login__gt_gt_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -&gt; Login -&gt;
        DESCRIPTION: -&gt; Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline is opened and displayed in the expanded state
        """
        pass

    def test_003_verify_displaying_racing_post_verdict(self):
        """
        DESCRIPTION: Verify displaying Racing Post Verdict
        EXPECTED: Racing Post post tile with CMS content is displayed as per design:
        EXPECTED: - Timestamp
        EXPECTED: - Icon (for selected template)
        EXPECTED: - Race name
        EXPECTED: - Racing Post label: **Verdict**
        EXPECTED: - Content box
        EXPECTED: - Price button (if it configured)
        EXPECTED: ![](index.php?/attachments/get/120869382)
        """
        pass

    def test_004_verify_displaying_racing_post_spotlight(self):
        """
        DESCRIPTION: Verify displaying Racing Post Spotlight
        EXPECTED: Racing Post post tile with CMS content is displayed as per design:
        EXPECTED: - Timestamp
        EXPECTED: - Icon (for selected template)
        EXPECTED: - Race name
        EXPECTED: - Racing Post label: **Spotlight**
        EXPECTED: - Content box
        EXPECTED: - Price button (if it configured)
        EXPECTED: ![](index.php?/attachments/get/120869383)
        """
        pass
