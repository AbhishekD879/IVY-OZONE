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
class Test_C60018040_Tracking_of_loading(Common):
    """
    TR_ID: C60018040
    NAME: Tracking of loading
    DESCRIPTION: This test case verifies GA tracking of launching Timeline on each page
    PRECONDITIONS: Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: Load the app
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - 	‘eventCategory’ : ‘ladbrokes lounge’,
        EXPECTED: - 	‘eventAction’ : ‘rendered’,
        EXPECTED: - ‘eventLabel’: `${CMS Campaign Name} // e.g. Demo 12/08/2020
        """
        pass

    def test_003_navigate_to_one_more_page_that_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to one more page that configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_004_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - 	‘eventCategory’ : ‘ladbrokes lounge’,
        EXPECTED: - 	‘eventAction’ : ‘rendered’,
        EXPECTED: - ‘eventLabel’: `${CMS Campaign Name} // e.g. Demo 12/08/2020
        """
        pass
