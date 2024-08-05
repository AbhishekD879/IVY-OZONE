import pytest
import voltron.environments.constants as vec
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2  # qa2 setup is not present fr timeline
# @pytest.mark.stg2
@pytest.mark.mobile_only
@pytest.mark.prod
@pytest.mark.low
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59888157_Verify_displaying_Timeline_in_the_open_expanded_state(Common):
    """
    TR_ID: C59888157
    NAME: Verify displaying Timeline  in the open (expanded) state
    DESCRIPTION: This test case verifies Timeline in the open (expanded) state
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline
    PRECONDITIONS: should be turned ON in the general System configuration ( CMS -> 'System
    PRECONDITIONS: configuration' -> 'Structure' -> 'Feature Toggle' section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline'
    PRECONDITIONS: section -> 'Timeline System Config' item -> 'Page URLs' field )
    PRECONDITIONS: Note: User can add multiple Page URL's to the list but manually need to refresh the page or app to see the reflected changes.
    PRECONDITIONS: 4.Posts should be also created in the CMS
    PRECONDITIONS: 5.Zeplin Links- https://app.zeplin.io/project/5dc59d1d83c70b83632
    PRECONDITIONS: e749c/screen/5fc90fbd08b6a9505bdfe043(Ladbrokes)
    PRECONDITIONS: https://app.zeplin.io/project/5dc59d1d83c70b83632e749c?seid=5fc912c1dc7b8e4f009ea750(Coral)
    PRECONDITIONS: 6.Load the app
    PRECONDITIONS: 7.User is logged in
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
        PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
        PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also,
        PRECONDITIONS: Timeline should be turned ON in the general System configuration ( CMS
        PRECONDITIONS: -> 'System configuration' -> 'Structure' -> 'Feature Toggle' section -> 'Timeline')
        PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->
        PRECONDITIONS: 'Timeline' section -> 'Timeline System Config' item -> 'Page URLs' field )
        PRECONDITIONS: 4.Design-https://app.zeplin.io/project/5dc59d1d83c70b83632e749c?
        PRECONDITIONS: said=5fc912c1dc7b8e4f009ea750
        PRECONDITIONS: 5.Load the app
        PRECONDITIONS: 6.User is logged in
        PRECONDITIONS: Timeline feature is for both Brands:
        PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
        PRECONDITIONS: Coral- Coral Pulse
        """
        faker = Faker()
        template_name = f'New_LoggedInText_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")

        self.cms_config.update_timeline_template(template_id=timeline_template['id'],
                                                 name=template_name)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text='test',
                                                             headerText=template_name)

        self.__class__.post_name = timeline_post['template']['name']
        self.site.login()

    def test_001_1navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: 1.Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline should be displayed at the bottom of the page, above Footer menu
        """
        self.site.wait_content_state("Home")
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg=f'"Timeline Bubble" is not displayed')

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline should be opened and displayed in the expanded state
        """
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is not expanded")

    def test_003_verify_timeline_in_the_expanded_state(self):
        """
        DESCRIPTION: Verify Timeline in the expanded state
        EXPECTED: 1.The following attributes should be
        EXPECTED: displayed in the Timeline header:
        EXPECTED: 2. a.Ladbrokes Lounge' text on the left side of the header
        EXPECTED: b. Coral Pulse' text on the left side of the header
        EXPECTED: 3.'Minimise' text on the right side of the header across both the brands
        EXPECTED: 4.Timeline has dark background at the top, left/right sides
        EXPECTED: 5.Configured posts are displayed on the white background
        EXPECTED: 6. For Ladbrokes- An icon LL will be displayed in the background.
        EXPECTED: For Coral-  A plain Blue background will be displayed at the back.
        """
        actual_title = self.site.timeline.timeline_campaign.timeline_header.text
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')
        header_left_position = self.site.timeline.timeline_campaign.timeline_header.location['x'] > \
            self.site.timeline.timeline_campaign.timeline_header.location['y']
        self.assertTrue(header_left_position,
                        msg="Timeline header text is not on the left side of the header")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        minimise_location = self.site.timeline.timeline_campaign.timeline_minimise.location['x']
        self.assertTrue(minimise_location >= 460, msg="'Minimise' text is not on the right side of the header")
        timeline_background = self.site.timeline.timeline_campaign.background_color_value
        self.assertEqual(timeline_background, vec.colors.TIMELINE_BACKGROUND_COLOR,
                         msg=f'Actual timeline background color: "{timeline_background}"'
                             f'is not the same as expected: "{vec.colors.TIMELINE_BACKGROUND_COLOR}"')
        post_background = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].background_color_value
        self.assertEqual(post_background, vec.colors.POST_BACKGROUND_COLOR,
                         msg=f'Actual timeline post color: "{post_background}"'
                             f'is not the same as expected: "{vec.colors.POST_BACKGROUND_COLOR}"')

    def test_004_verify_timeline_view_for_the_mostrecent_post_1st_post_in_the_list(self):
        """
        DESCRIPTION: Verify Timeline view for the Most
        DESCRIPTION: Recent Post (1st Post in the list)
        EXPECTED: The Most Recent Post (1st Post in
        EXPECTED: the list) should be displayed with a rounded edge
        """
        date = {}
        posts = self.site.timeline.timeline_campaign.items_as_ordered_dict
        actual_most_recent_post = list(posts.values())[0].name
        for item_name, item in posts.items():
            date[item_name] = item.post_time
        sorted_posts = sorted(date.items(), key=lambda x: x[1])[-1]
        expected_most_recent_post = sorted_posts[0]
        self.assertEqual(actual_most_recent_post, expected_most_recent_post,
                         msg=f'Actual timeline most recent post: "{actual_most_recent_post}"'
                             f'is not the same as expected: "{expected_most_recent_post}"')

    def test_005_scroll_down_to_the_next_posts_on_thetimeline_page(self):
        """
        DESCRIPTION: Scroll down to the next Posts on the
        DESCRIPTION: Timeline page
        EXPECTED: The next posts should be displayed with a straight edge
        """
        # edges verification cannot be automated
