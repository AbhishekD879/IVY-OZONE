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
class Test_C59918221_Verify_navigation_to_EDP_or_Promo_Pages_from_Timeline(Common):
    """
    TR_ID: C59918221
    NAME: Verify navigation to EDP or Promo Pages from Timeline
    DESCRIPTION: This test case verifies navigation to EDP or Promo Pages from Timeline
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.Template is created with the following attributes:
    PRECONDITIONS: I.'Post Href' (link to EDP or Promo page)
    PRECONDITIONS: ii.Show Redirect Arrow' checkbox is checked
    PRECONDITIONS: 5.Timeline posts with additional navigation are created and published
    PRECONDITIONS: 6.Load the app
    PRECONDITIONS: 7.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - Post with additional navigation is displayed, Redirect Arrow is shown
        """
        pass

    def test_003_tap_on_the_navigation_clickable_area(self):
        """
        DESCRIPTION: Tap on the navigation clickable area
        EXPECTED: - User is navigated to the target location (EDP Page; Promotions page)
        EXPECTED: (location should be the same as configured in CMS)
        EXPECTED: - Timeline widget is minimized to allow the user to view target content
        """
        pass
