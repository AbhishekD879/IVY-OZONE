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
class Test_C59887569_Verify_displaying_Timeline_header_in_the_application(Common):
    """
    TR_ID: C59887569
    NAME: Verify displaying Timeline header  in the application
    DESCRIPTION: This test case verifies Timeline header in the application
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS&gt;System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -&gt; 'Timeline' section -&gt;
    PRECONDITIONS: 'Timeline System Config' item -&gt; 'Enabled' checkbox ) and also,
    PRECONDITIONS: Timeline should be turned ON in the general System configuration ( CMS
    PRECONDITIONS: -&gt; 'System configuration' -&gt; 'Structure' -&gt; 'Feature Toggle' section -&gt; 'Timeline')
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -&gt;
    PRECONDITIONS: 'Timeline' section -&gt; 'Timeline System Config' item -&gt; 'Page URLs' field )
    PRECONDITIONS: 4.Design-https://app.zeplin.io/project/5dc59d1d83c70b83632e749c?
    PRECONDITIONS: said=5fc912c1dc7b8e4f009ea750
    PRECONDITIONS: 5.Load the app
    PRECONDITIONS: 6.User is logged in
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_1navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: 1.Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline should be displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_2verify_timeline_header(self):
        """
        DESCRIPTION: 2.Verify Timeline header
        EXPECTED: 1.Timeline header consist of:
        EXPECTED: Ladbrokes- Ladbrokes Lounge
        EXPECTED: Coral-  'Coral Pulse'
        EXPECTED: Yellow dot- Coral
        EXPECTED: Red dot - Ladbrokes(Only if new POST was created and update was received)
        EXPECTED: 2. Timeline header has rounded corners
        EXPECTED: 3. Timeline header is collapsed by default
        """
        pass

    def test_003_3scroll_up_and_down_on_the_page(self):
        """
        DESCRIPTION: 3.Scroll up and down on the page
        EXPECTED: 1.Timeline header should be sticky to the Footer menu
        EXPECTED: 2.Timeline header should be in collapsed mode
        """
        pass
