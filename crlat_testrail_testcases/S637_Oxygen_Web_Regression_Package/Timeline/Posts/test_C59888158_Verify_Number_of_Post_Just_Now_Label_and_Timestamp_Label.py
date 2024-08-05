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
class Test_C59888158_Verify_Number_of_Post_Just_Now_Label_and_Timestamp_Label(Common):
    """
    TR_ID: C59888158
    NAME: Verify Number of Post, 'Just Now'  Label and Timestamp Label
    DESCRIPTION: This test case verifies Number of Post, 'Just Now'  Label and Timestamp Label
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.Live Camping is created
    PRECONDITIONS: 5.User is logged in
    PRECONDITIONS: 6.In CMS Template check ""Show Timestamp"" checkbox
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_go_to_cms__gt_timeline__gt_timeline_campaign__gt_open_existed_live_campaign__gt_set_value_for_initial_number_of_messages_to_display_field_eg_7_and_save(self):
        """
        DESCRIPTION: Go to CMS -&gt; Timeline -&gt; Timeline Campaign -&gt; Open existed Live Campaign -&gt; Set value for 'Initial number of messages to display' field, e.g 7 and Save
        EXPECTED: Campaign is updated with new number of Post
        """
        pass

    def test_002___hoose_template_with_checked_show_timestamp__create_and_publish_a_new_post_in_live_campaign(self):
        """
        DESCRIPTION: - Сhoose Template with checked "Show Timestamp"
        DESCRIPTION: - Create and Publish a new Post in Live Campaign
        EXPECTED: Post is successfully created and published
        """
        pass

    def test_003_load_the_app__gt_login__gt_gt_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -&gt; Login -&gt;
        DESCRIPTION: -&gt; Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_004_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'Just Now' label is displayed for newly created post(post 'age' is between 0 to 30 seconds)
        EXPECTED: &lt; 30 sec - 'Just now'
        EXPECTED: - The same number of posts is displayed as configured in step #1 on CMS
        EXPECTED: - In WS "POST"-&gt; showTimestamp: true
        EXPECTED: ![](index.php?/attachments/get/121003777)
        """
        pass

    def test_005_look_one_more_time_at_newly_created_post_after_30sec(self):
        """
        DESCRIPTION: Look one more time at newly created post after 30sec
        EXPECTED: - Timestamp Label is displaying (when the post exceeds 30 seconds and &lt; 1 hour
        EXPECTED: -  Is showing date ago value, like '1 minute', '15 minutes', '57 minutes')
        EXPECTED: ![](index.php?/attachments/get/121004805)
        """
        pass

    def test_006_look_at_the_posts_that_was_created_more_that_1_hour_ago(self):
        """
        DESCRIPTION: Look at the posts that was created more that 1 hour ago
        EXPECTED: - Timestamp Label is displaying
        EXPECTED: - &gt; 1 hour - is showing the publish date and time instead of calculating "time ago" value, like '14:00
        EXPECTED: ![](index.php?/attachments/get/121004807)
        """
        pass

    def test_007___go_to_cms_and_choose_template_with_unchecked_show_timestamp__create_and_publish_a_new_post_in_live_campaign(self):
        """
        DESCRIPTION: - Go to CMS and choose Template with **UNchecked** "Show Timestamp"
        DESCRIPTION: - Create and Publish a new Post in Live Campaign
        EXPECTED: The post is successfully created and published
        """
        pass

    def test_008_return_to_the_timeline_on_ui_and_verified_created_post(self):
        """
        DESCRIPTION: Return to the Timeline on UI and verified created post
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'Just Now' label is NOT displayed for newly created post
        EXPECTED: - Timestamp Label is NOT displayed
        EXPECTED: - In WS "POST"-&gt; showTimestamp: false
        EXPECTED: ![](index.php?/attachments/get/121002750)
        """
        pass
