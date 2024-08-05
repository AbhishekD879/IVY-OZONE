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
class Test_C59927336_Verify_live_updates_for_the_resulted_event(Common):
    """
    TR_ID: C59927336
    NAME: Verify live updates for the resulted event
    DESCRIPTION: This test case verifies live updates for Expired event/ Resulted event
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Campaign is created
    PRECONDITIONS: 2.Timeline posts with prices are created and published
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in ( NOTE Timeline is displayed ONLY for Logged In Users )
    PRECONDITIONS: -Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: It should be verified for:
    PRECONDITIONS: - Races
    PRECONDITIONS: - Tier 1 Sports
    PRECONDITIONS: - Tier 2 Sports
    PRECONDITIONS: - Tier 3 Sports
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_click_on_the_timeline_ladbrokes_lounge_button(self):
        """
        DESCRIPTION: Click on the Timeline 'Ladbrokes Lounge' button
        EXPECTED: - Page with the published post is opened
        EXPECTED: - Price is present in the post
        EXPECTED: - Content is the same as in CMS
        EXPECTED: - In WS 'POST' response is present with all fields form CMS
        """
        pass

    def test_002_go_to_ob_and_result_the_event(self):
        """
        DESCRIPTION: Go to OB and result the event
        EXPECTED: - Event has resulted
        EXPECTED: - Changes are saved successfully in OB
        """
        pass

    def test_003___return_to_the_timeline_and_verify_outcomes_for_the_event__chek_ws(self):
        """
        DESCRIPTION: - Return to the 'Timeline' and verify outcomes for the event
        DESCRIPTION: - Cheсk WS
        EXPECTED: - Post is present in the 'Timeline'
        EXPECTED: - Corresponding 'Price/Odds' button displays with n/a status
        EXPECTED: ![](index.php?/attachments/get/119601968)
        EXPECTED: - The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type POST_CHANGED
        EXPECTED: outcomes:
        EXPECTED: isResulted: true
        """
        pass

    def test_004_collapse_timeline_and_result_the_event(self):
        """
        DESCRIPTION: Collapse 'Timeline' and result the event
        EXPECTED: - The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type POST_CHANGED
        EXPECTED: outcomes:
        EXPECTED: isResulted: true
        """
        pass

    def test_005_expand_timeline_and_verify_the_selection_for_the_post_on_ui(self):
        """
        DESCRIPTION: Expand 'Timeline' and verify the selection for the Post on UI
        EXPECTED: - Post is present in the 'Timeline'
        EXPECTED: - Corresponding 'Price/Odds' button displays with n/a status
        EXPECTED: ![](index.php?/attachments/get/119601968)
        """
        pass
