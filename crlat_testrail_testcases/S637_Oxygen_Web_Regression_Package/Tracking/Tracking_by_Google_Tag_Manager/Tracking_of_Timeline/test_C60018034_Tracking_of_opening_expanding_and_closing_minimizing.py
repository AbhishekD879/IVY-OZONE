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
class Test_C60018034_Tracking_of_opening_expanding_and_closing_minimizing(Common):
    """
    TR_ID: C60018034
    NAME: Tracking of opening/expanding and closing/minimizing
    DESCRIPTION: This test case verifies GA tracking of opening/expanding and closing/minimizing Timeline
    PRECONDITIONS: - Confluence instruction - **How to create Timeline Template, Campaign, Posts** - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: - Timeline should be enabled in CMS ( **CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox** ) and also, Timeline should be turned ON in the general System configuration ( **CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline'** )
    PRECONDITIONS: ![](index.php?/attachments/get/118653501)
    PRECONDITIONS: - Timeline is available for the configured pages in CMS ( **CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field** )
    PRECONDITIONS: - Posts should be also created in the CMS
    PRECONDITIONS: Load the app
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - 'HIGHLIGHTS' tab is opened on the Home page
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline is opened and displayed in the expanded state
        """
        pass

    def test_003_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - 	‘eventCategory’ : ‘ladbrokes lounge’,
        EXPECTED: - 	**‘eventAction’ : ‘open’**,
        EXPECTED: - ‘eventLabel’: `${CMS Campaign Name} // e.g. Demo 12/08/2020
        """
        pass

    def test_004_tap_on_the_minimise_text(self):
        """
        DESCRIPTION: Tap on the 'Minimise' text
        EXPECTED: Timeline returns to the collapsed position
        """
        pass

    def test_005_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - ‘eventCategory’ : ‘ladbrokes lounge’,
        EXPECTED: - **‘eventAction’ : ‘close’**,
        EXPECTED: - ‘eventLabel’: `${CMS Campaign Name} // e.g. Demo 12/08/2020
        """
        pass

    def test_006_tap_on_the_timeline_header_again(self):
        """
        DESCRIPTION: Tap on the Timeline header again
        EXPECTED: Timeline is opened and displayed in the expanded state
        """
        pass

    def test_007_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - 	‘eventCategory’ : ‘ladbrokes lounge’,
        EXPECTED: - 	**‘eventAction’ : ‘open’**,
        EXPECTED: - ‘eventLabel’: `${CMS Campaign Name} // e.g. Demo 12/08/2020
        """
        pass
