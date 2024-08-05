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
class Test_C59888153_Verify_displaying_Horse_Racing_Result_Post(Common):
    """
    TR_ID: C59888153
    NAME: Verify displaying Horse Racing Result Post
    DESCRIPTION: This test case verifies displaying Horse Racing Result Post
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Ladbrokes:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_1go_to_cms___timeline___timelinecampaign___create_and_publish_postswith_the_following_configuration2results_icon_should_be_configured_intemplate3show_left_side_redblue_line_should_beconfigured_in_templateladbrokes__left_side_red_linecoral__left_side_blue_line4header_text_eg_resultsmarket_rasen_5055subheader_text_eg_queen_motherstakes6filled_text_with_position__price_maxnumber_of_positions__7__1st_horsename_odds_(self):
        """
        DESCRIPTION: "1.Go to CMS -> Timeline -> Timeline
        DESCRIPTION: Campaign -> Create and Publish Posts
        DESCRIPTION: with the following configuration:
        DESCRIPTION: 2.Results Icon (should be configured in
        DESCRIPTION: Template)
        DESCRIPTION: 3.Show Left Side Red/Blue Line (should be
        DESCRIPTION: configured in Template)
        DESCRIPTION: Ladbrokes- Left Side Red Line
        DESCRIPTION: Coral- Left Side Blue Line
        DESCRIPTION: 4.Header Text: e.g. RESULTS:
        DESCRIPTION: MARKET RASEN (5.05)
        DESCRIPTION: 5.Subheader Text: e.g. Queen Mother
        DESCRIPTION: Stakes
        DESCRIPTION: 6.Filled Text with Position & price (max
        DESCRIPTION: number of positions = 7) : 1st: Horse
        DESCRIPTION: name (odds/) "
        EXPECTED: Post is successfully created and published
        """
        pass

    def test_002_load_the_app___login____navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -> Login ->
        DESCRIPTION: -> Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_003_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - **Newly created posts on CMS appears instantly on the frontend**
        """
        pass

    def test_004_verify_displaying_newly_created_results_post(self):
        """
        DESCRIPTION: Verify displaying newly created results post
        EXPECTED: "Results post should be displayed as per designs:
        EXPECTED: 1.Results Icon
        EXPECTED: 2. Red Banner(Ladbrokes)
        EXPECTED: b.Blue Banner(Coral)
        EXPECTED: 3. Result time stamp should not be
        EXPECTED: displayed
        EXPECTED: 4.Title: e.g. RESULTS: MARKET
        EXPECTED: RASEN (5.05)
        EXPECTED: 5.Description: e.g. Queen Mother
        EXPECTED: Stakes
        EXPECTED: 6.Position & price (max number of
        EXPECTED: positions = 7) : 1st: Horse name
        EXPECTED: (odds/)
        EXPECTED: "
        """
        pass
