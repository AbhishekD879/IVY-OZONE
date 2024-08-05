import pytest
from faker import Faker
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2 #not configured under tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.mobile_only
@vtest
class Test_C59888154_Verify_displaying_Generic_News_Post(Common):
    """
    TR_ID: C59888154
    NAME: Verify displaying Generic News Post
    DESCRIPTION: This test case verifies displaying Horse Racing Result Post
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_000_go_to_cms___timeline___timeline_campaign____create_and_publish_posts_with_the_following_configuration1_sport_icon_select_from_list_of_available_icons_eg_horse_racing_football_should_be_configured_in_template2_show_timestamp_should_be_configured_in_template3_header_text_eg_canford_can4_sub_header_optional__eg_harry_kane_9mins5_text_eg_three_favourites_have_(self):
        """
        DESCRIPTION: Go to CMS -> Timeline -> Timeline Campaign ->
        DESCRIPTION: -> Create and Publish Posts with the following configuration:
        DESCRIPTION: 1. Sport Icon (Select from list of available icons e.g horse racing, football) *(should be configured in Template)*
        DESCRIPTION: 2. Show Timestamp *(should be configured in Template)*
        DESCRIPTION: 3. Header Text: e.g CANFORD CAN
        DESCRIPTION: 4. Sub Header (Optional) : e.g Harry Kane (9mins)
        DESCRIPTION: 5. Text: e.g Three favourites have ….."
        EXPECTED: Post is successfully created and published
        """
        timeline_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle']['Timeline']
        if not timeline_enable:
            self.cms_config.update_system_configuration_structure(config_item='Feature Toggle', field_name='Timeline',
                                                                  field_value=True)
        timeline_system_config = self.cms_config.get_timeline_system_configuration()
        if not timeline_system_config["enabled"]:
            self.assertTrue(self.cms_config.update_timeline_system_config(), "Timeline system config is not enabled")
        self.__class__.post_desc = "Text"
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        event_ID = event.get('event').get('id')
        outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('No outcomes available')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        selection_ID = list(selection_ids.values())[0]
        faker = Faker()
        template_name = f'New_Template_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")

        self.cms_config.update_timeline_template(template_id=timeline_template['id'],
                                                 name=template_name,
                                                 eventId=event_ID, selectionId=selection_ID)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text=self.post_desc,
                                                             headerText=template_name, postIconSvgId="NewTimelineHorse",
                                                             headerIconSvgId="clock-icon", showTimestamp=True,
                                                             subHeader="subHeader")

        self.__class__.post_name = timeline_post['template']['name']

    def test_001_load_the_app___login____navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -> Login ->
        DESCRIPTION: -> Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        self.site.login()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg="Timeline bubble is not displayed")
        actual_title = self.site.timeline.title
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - **Newly created posts on CMS appears instantly on the frontend**
        """
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is opened")
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} with price is not displayed')

    def test_003_verify_displaying_newly_created_generic_news_post(self):
        """
        DESCRIPTION: Verify displaying newly created Generic News post
        EXPECTED: Generic News post is displayed as per designs:
        EXPECTED: - Sport Icon (Select from list of available icons e.g horse racing, football)
        EXPECTED: - Timestamp to show age of the post : e.g 23 Min
        EXPECTED: - Title: e.g CANFORD CAN
        EXPECTED: - Sub Header (Optional) : e.g Harry Kane (9mins)
        EXPECTED: - Description: e.g Three favourites have …..
        EXPECTED: ![](index.php?/attachments/get/118677252)
        """
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} with price is not displayed')
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_icon,
                        msg=f'post icon is not displayed')
        self.assertEqual(
            self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_description,
            self.post_desc, msg=f'Actual post description: "{self.post_desc}" is not equal with the Expected post desc')
        self.assertTrue(
            self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_time,
            msg="post time is not displayed")
