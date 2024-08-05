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
class Test_C60018036_Tracking_of_navigation_after_clicking_on_a_post(Common):
    """
    TR_ID: C60018036
    NAME: Tracking of navigation after clicking on a post
    DESCRIPTION: This test case verifies GA tracking of navigation after clicking on a post from Timeline
    PRECONDITIONS: - CMS-API Endpoints: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: - Timeline should be enabled in CMS ( **CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox** ) and also, Timeline should be turned ON in the general System configuration ( **CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline'** )
    PRECONDITIONS: - Timeline is available for the configured pages in CMS ( **CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field** )
    PRECONDITIONS: ![](index.php?/attachments/get/118653501)
    PRECONDITIONS: - Timeline posts with additional navigation are created and published
    PRECONDITIONS: Load the app
    PRECONDITIONS: User is logged in
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
        EXPECTED: Timeline is opened and displayed in the expanded state
        EXPECTED: Post with additional navigation is displayed, Redirect Arrow is shown
        """
        pass

    def test_003_tap_on_the_post_to_navigate_to_the_target_location_edp_page_promotions_page_location_should_be_the_same_as_configured_in_cms(self):
        """
        DESCRIPTION: Tap on the post to navigate to the target location (EDP Page; Promotions page) (location should be the same as configured in CMS)
        EXPECTED: - User is navigated to the target location (EDP Page; Promotions page) (location should be the same as configured in CMS)
        EXPECTED: - Timeline widget is minimized to allow the user to view target content
        """
        pass

    def test_004_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - 	‘eventCategory’ : ‘ladbrokes lounge’,
        EXPECTED: - 	**‘eventAction’ : ‘navigation’**
        EXPECTED: - ‘eventLabel’: `${Destination URI}, // e.g. /horse-racing/horse-- --racing-live/hamilton/16-50-hamilton/230854274/win-or-each-way
        EXPECTED: - ‘dimension114’: `${Template Name}, // e.g. Racing Post Spotlight Template
        EXPECTED: - ‘dimension115’: `${Template ID} // e.g. 5f3393e1c9e77c0001dec68f
        """
        pass
