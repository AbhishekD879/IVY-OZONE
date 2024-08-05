import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from faker import Faker
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2   # not configured under tst2
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.mobile_only
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Go to CMS -> Timeline -> Timeline Campaign ->
        DESCRIPTION: -> Create and Publish Posts with the following configuration:
        EXPECTED: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
        EXPECTED: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
        EXPECTED: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
        EXPECTED: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
        EXPECTED: 4.Live Camping is created
        EXPECTED: 5.User is logged in
        EXPECTED: 6.In CMS Template check ""Show Timestamp"" checkbox
        """
        timeline_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle']['Timeline']
        if not timeline_enable:
            self.cms_config.update_system_configuration_structure(config_item='Feature Toggle', field_name='Timeline',
                                                                  field_value=True)

        timeline_system_config = self.cms_config.get_timeline_system_configuration()
        if not timeline_system_config["enabled"]:
            self.assertTrue(self.cms_config.update_timeline_system_config(), "Timeline system config is not enabled")

        self.__class__.post_desc = "Text"

    def test_001_go_to_cms___timeline___timeline_campaign___open_existed_live_campaign___set_value_for_initial_number_of_messages_to_display_field_eg_7_and_save(self):
        """
        DESCRIPTION: Go to CMS -> Timeline -> Timeline Campaign -> Open existed Live Campaign -> Set value for 'Initial number of messages to display' field, e.g 7 and Save
        EXPECTED: Campaign is updated with new number of Post
        """
        # covered in next step

    def test_002_choose_template_with_checked_show_timestamp__create_and_publish_a_new_post_in_live_campaign(self):
        """
        DESCRIPTION: Load the app -> Login ->
        DESCRIPTION: - Сhoose Template with checked "Show Timestamp"
        DESCRIPTION: - Create and Publish a new Post in Live Campaign
        EXPECTED: Post is successfully created and published
        """
        self.site.login()
        faker = Faker()
        template_name = f'New_Template_{faker.city()}'
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")
        Live_Campaign_Id = self.get_timeline_campaign_id()
        get_campaign_info = self.cms_config.get_timeline_campaign_info(campaign_id=Live_Campaign_Id)
        self.__class__.messagesToDisplayCount = get_campaign_info['messagesToDisplayCount']
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text=self.post_desc,
                                                             headerText=template_name, postIconSvgId="NewTimelineHorse",
                                                             headerIconSvgId="clock-icon", showTimestamp=True,
                                                             subHeader="subHeader")
        self.__class__.post_name = timeline_post['template']['name']

    def test_003_load_the_app___login____navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: -> Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """

        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg="Timeline bubble is not displayed")
        actual_title = self.site.timeline.title
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')

    def test_004_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'Just Now' label is displayed for newly created post(post 'age' is between 0 to 30 seconds)
        EXPECTED: < 30 sec - 'Just now'
        EXPECTED: - The same number of posts is displayed as configured in step #1 on CMS
        EXPECTED: - In WS "POST"-> showTimestamp: true
        EXPECTED: ![](index.php?/attachments/get/121003777)
        """
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is opened")
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertTrue(post,
                        msg=f'post name {self.post_name} with price is not displayed')
        self.__class__.expected_time = 'Just now'
        self.assertEqual(post.post_time, self.expected_time,
                         msg=f'Actual time "{post.post_time}" is not same as Expected time "{self.expected_time}"')
        posts = len(self.site.timeline.timeline_campaign.items_as_ordered_dict)
        self.assertTrue(posts <= self.messagesToDisplayCount,
                        msg=f'Number of posts: "{posts}" displayed on UI are more than the number of count set in CMS: "{self.messagesToDisplayCount}"')
        wait_for_result(lambda: post.post_time != self.expected_time, name='Timestamp to update', timeout=60)

    def test_005_look_one_more_time_at_newly_created_post_after_30sec(self):
        """
        DESCRIPTION: Look one more time at newly created post after 30sec
        EXPECTED: - Timestamp Label is displaying (when the post exceeds 30 seconds and < 1 hour
        EXPECTED: -  Is showing date ago value, like '1 minute', '15 minutes', '57 minutes')
        EXPECTED: ![](index.php?/attachments/get/121004805)
        """
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertTrue(post,
                        msg=f'post name {self.post_name} with price is not displayed')
        expected_time = 'minute'
        self.assertIn(expected_time, post.post_time,
                      msg=f'Expected time "{expected_time}" is not in Actual time "{post.post_time}" for post: "{self.post_name}"')

    def test_006_look_at_the_posts_that_was_created_more_that_1_hour_ago(self):
        """
        DESCRIPTION: Look at the posts that was created more that 1 hour ago
        EXPECTED: - Timestamp Label is displaying
        EXPECTED: - > 1 hour - is showing the publish date and time instead of calculating "time ago" value, like '14:00
        EXPECTED: ![](index.php?/attachments/get/121004807)
        """
        # Cannot automate

    def test_007___go_to_cms_and_choose_template_with_unchecked_show_timestamp__create_and_publish_a_new_post_in_live_campaign(self):
        """
        DESCRIPTION: - Go to CMS and choose Template with **UNchecked** "Show Timestamp"
        DESCRIPTION: - Create and Publish a new Post in Live Campaign
        EXPECTED: The post is successfully created and published
        """
        faker = Faker()
        template_name = f'New_Template_{faker.city()}'
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text", showTimestamp=False)
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text=self.post_desc,
                                                             headerText=template_name, postIconSvgId="NewTimelineHorse",
                                                             headerIconSvgId="clock-icon", showTimestamp=False,
                                                             subHeader="subHeader")
        sleep(2)
        self.__class__.post_name2 = timeline_post['template']['name']


    def test_008_return_to_the_timeline_on_ui_and_verified_created_post(self):
        """
        DESCRIPTION: Return to the Timeline on UI and verified created post
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'Just Now' label is NOT displayed for newly created post
        EXPECTED: - Timestamp Label is NOT displayed
        EXPECTED: - In WS "POST"-> showTimestamp: false
        EXPECTED: ![](index.php?/attachments/get/121002750)
        """
        result = wait_for_result(lambda: self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name2.upper()])
        self.assertTrue(result, msg=f'post name {self.post_name2} is not displayed')
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name2.upper()]
        self.assertTrue(post,
                        msg=f'post name {self.post_name2} is not displayed')
        self.assertFalse(post.post_time, msg=f'post time is displayed though "show timestamp" is not active for post: "{self.post_name2}"')
