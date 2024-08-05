import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@vtest
class Test_C59888574_Verify_that_Open_Closed_Campaign_can_not_Publish_Posts(Common):
    """
    TR_ID: C59888574
    NAME: Verify that Open/Closed Campaign can not Publish Posts
    DESCRIPTION: This test case Verify that Open/Closed Campaign can not Publish Posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Confluence instruction - How to create Timeline Template, Campaign,
    PRECONDITIONS: Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+
    PRECONDITIONS: Template%2C+Campaign+and+Posts (TBD)
    PRECONDITIONS: 3.Timeline should be enabled in CMS (CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox)
    PRECONDITIONS: 4.Timeline should be turned ON in the general System configuration (CMS
    PRECONDITIONS: ->'System configuration' ->'Structure' ->'Feature Toggle' section ->'Timeline')
    PRECONDITIONS: 5.Timeline is available for the configured pages in CMS (CMS ->'Timeline'
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field)
    PRECONDITIONS: 6.Open/Closed Campaign is created
    PRECONDITIONS: 7.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_create_a_post_in_the_open_or_close_campaign(self):
        """
        DESCRIPTION: Go to CMS and create a Post in the Open or Close Campaign
        EXPECTED: Post is created
        """
        pass

    def test_002_click_save__publish_button(self):
        """
        DESCRIPTION: Click 'Save & Publish' button
        EXPECTED: Error: Validation failed with reason:
        EXPECTED: You can only operate DRAFT posts while Campaign is not
        EXPECTED: displayed to the customers
        """
        pass

    def test_003_navigate_to_the_page_with_configuredtimeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured
        DESCRIPTION: 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline should be displayed at the bottom of the page, above
        EXPECTED: Footer menu
        """
        pass

    def test_004_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: 1.Page should be opened
        EXPECTED: 2.Post should not be present in the Timeline
        EXPECTED: 3.In WS 'Post' response should not be present
        """
        pass
