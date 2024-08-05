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
class Test_C60018035_Tracking_of_adding_to_Betslip_after_clicking_on_a_post(Common):
    """
    TR_ID: C60018035
    NAME: Tracking of adding to Betslip after clicking on a post
    DESCRIPTION: This test case verifies GA tracking of adding to Betslip after clicking on a post
    PRECONDITIONS: - CMS-API Endpoints: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: - Timeline should be enabled in CMS ( **CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox** ) and also, Timeline should be turned ON in the general System configuration ( **CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline'** )
    PRECONDITIONS: - Timeline is available for the configured pages in CMS ( **CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field** )
    PRECONDITIONS: ![](index.php?/attachments/get/118653501)
    PRECONDITIONS: Timeline posts with prices are created and published
    PRECONDITIONS: Design - https://app.zeplin.io/project/5dc59d1d83c70b83632e749c/screen/5e99df4a01006e7e1806a50e
    PRECONDITIONS: **NOTE** Parameters and values in 'dataLayer' object are different than in the design INN-988 (agreed in INN-1558)
    PRECONDITIONS: Load the app
    PRECONDITIONS: User is logged in
    PRECONDITIONS: Betslip is empty
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: Post with price is displayed
        """
        pass

    def test_003_tap_on_the_price_button(self):
        """
        DESCRIPTION: Tap on the price button
        EXPECTED: - Quick bet overlay is opened over the top of the timeline
        """
        pass

    def test_004_click_button_add_to_betslip_on_quick_bet_overlay(self):
        """
        DESCRIPTION: Click button 'Add to Betslip' on Quick bet overlay
        EXPECTED: - Quick bet widget is closed
        EXPECTED: - User is returned to timeline
        """
        pass

    def test_005_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - event: "trackEvent"
        EXPECTED: - eventAction: "add to quickbet"
        EXPECTED: - eventCategory: "quickbet"
        EXPECTED: - eventLabel: "success"
        EXPECTED: and
        EXPECTED: - event: "trackEvent"
        EXPECTED: - eventAction: "add to betslip"
        EXPECTED: - eventCategory: "quickbet"
        EXPECTED: - eventLabel: "success"
        """
        pass

    def test_006_return_to_timeline_and_add_one_more_price_to_betslip(self):
        """
        DESCRIPTION: Return to Timeline and add one more price to Betslip
        EXPECTED: - Green 'selected' state is applied in timeline for that selection
        EXPECTED: - Selection is added to Betslip
        EXPECTED: - Betslip counter is increased by one
        EXPECTED: - Expanded Timeline is still displaying
        """
        pass

    def test_007_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - event: "trackEvent"
        EXPECTED: - eventAction: "add to betslip"
        EXPECTED: - eventCategory: "betslip"
        EXPECTED: - eventLabel: "success"
        """
        pass
