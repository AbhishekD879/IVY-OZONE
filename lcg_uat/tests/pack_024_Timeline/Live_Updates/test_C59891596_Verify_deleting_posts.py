import json
import pytest
import string
import random
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared import get_device


# @pytest.mark.tst2
# @pytest.mark.stg2  #Not configured in tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59891596_Verify_deleting_posts(Common):
    """
    TR_ID: C59891596
    NAME: Verify deleting posts
    DESCRIPTION: This test case verifies deleting posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 3.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 4.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 5.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 6.Live Campaign is created.
    PRECONDITIONS: 7.User is logged in app
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    @classmethod
    def cms_tearDown(cls):
        cls.get_cms_config()._created_timeline_post
        _created_timeline_post = []
        _created_timeline_template = []

    def verify_post_removed(self, post_id, delimiter='42'):
        sleep(3)
        logs = get_device().get_performance_log(preserve=False)
        for entry in logs[::-1]:
            try:
                payload_data = entry[1]['message']['message']['params']['response']['payloadData']
                if 'POST_REMOVED' in payload_data:
                    removed_post_id = payload_data.split(str(delimiter), maxsplit=1)[1].split(',')[3].split(':')[1]
                    if post_id == removed_post_id.replace('"', ""):
                        message = payload_data.split(str(delimiter), maxsplit=1)[1]
                        return json.loads(message)[1]
            except KeyError:
                continue
        return {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check timeline is status in CMS System Configuration
        """
        if not self.cms_config.get_timeline_system_configuration():
            self.cms_config.update_timeline_system_config()

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_campanig(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the post in the Live Campanig
        EXPECTED: Post should be created and published.
        """
        chars = string.ascii_uppercase + string.digits
        postfix = ''.join(random.choice(chars) for _ in range(3))
        template_name = f'Auto Test template {postfix}'

        camp_id = self.get_timeline_campaign_id()
        self.__class__.timeline_template = self.cms_config.create_timeline_template(template_name=template_name,
                                                                                    text='test')
        self.__class__.template_id = self.timeline_template['id']
        timeline_post = self.cms_config.create_campaign_post(template_id=self.timeline_template['id'],
                                                             campaign_id=camp_id,
                                                             poststatus='PUBLISHED')
        self.__class__.cms_post_id = timeline_post['id']
        self.__class__.cms_template_header = timeline_post['template']['headerText']

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline should be displayed at the bottom of the page, above Footer menu
        """
        self.site.login()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), "TimeLine Bubble not displayed on UI")
        self.assertTrue(self.site.timeline.title, "Timeline title not displayed On UI")

    def test_003_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: Page with the published post should be opened.Content is the same as in CMS.
        """
        self.site.timeline.timeline_bubble.click()
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        "Timeline is not maximised after bubble click")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header,
                        "Timeline header not displayed after click")
        post_ui = self.site.timeline.timeline_campaign.items_as_ordered_dict[
            self.cms_template_header.upper()]
        self.assertTrue(post_ui, f'Post Created in CMS{self.cms_template_header.upper()} not displayed on UI')

    def test_004_go_to_cms_and_delete_post(self):
        """
        DESCRIPTION: Go to CMS and delete post
        EXPECTED: Post should be deleted.
        """
        status_after_delete = self.cms_config.delete_timeline_post(post_id=self.cms_post_id)
        self.assertTrue(status_after_delete, "Created Posted not deleted successfully")
        self.cms_config.delete_timeline_template(template_id=self.template_id)

    def test_005_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: Page should be opened.
        EXPECTED: Deleted post should not be present in the Timeline.
        EXPECTED: In WS 'POST_REMOVED' response should be present with fields
        """
        response = self.verify_post_removed(post_id=str(self.cms_post_id))
        self.assertTrue(response, "Created Posted not deleted successfully")

        ui_timeline_post_list = self.site.timeline.timeline_campaign.items_as_ordered_dict
        timeline_post = self.timeline_template['headerText']

        self.assertNotIn(timeline_post, ui_timeline_post_list.keys(),
                         msg=f'created timeline post "{timeline_post} is not appearing on UI, actual post list {ui_timeline_post_list.keys()}"')
