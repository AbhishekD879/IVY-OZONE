import json
import pytest
from faker import Faker
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2  # qa2 setup is not present for timeline
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59888283_Verify_Unpublishing_edited_posts_on_the_UI(Common):
    """
    TR_ID: C59888283
    NAME: Verify Unpublishing edited posts on the UI
    DESCRIPTION: This test case verify displaying content on the UI
    PRECONDITIONS: - CMS-API Endpoints: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Confluence instruction - **How to create Timeline Template, Campaign, Posts** - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: - Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: - Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: - Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: - Live Campanig is created
    PRECONDITIONS: - Design - https://app.zeplin.io/project/5dc59d1d83c70b83632e749c/screen/5efc40efdb99fb613a6fcb47
    PRECONDITIONS: User is logged in app
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_timeline_websocket_data(self, delimiter, posttype):
        """
        This method will get web socket data for type Post_type and Post_remove
        """
        sleep(3)
        logs = self.device.get_performance_log()
        for entry in logs[::-1]:
            try:
                payload_data = entry[1]['message']['message']['params']['response']['payloadData']
                if posttype in payload_data and \
                        payload_data.startswith(str(delimiter)):
                    if payload_data.split(str(delimiter), maxsplit=1)[1].split(',')[0].split('[')[1].replace('"',
                                                                                                             '') == posttype :
                        message = json.loads(payload_data[len(str(delimiter)):])[1]
                    return message
            except (KeyError, IndexError, AttributeError):
                continue

    def validate_ws_post_data(self):
        """
        This method will verify fields in CMS and websocke request call of campaign post
        """
        data = self.get_timeline_websocket_data(delimiter='42', posttype='POST_PAGE')
        websocket_post_data = ''
        for post in data['page']:
            if post['id'] == self.timeline_post['id']:
                websocket_post_data = post
                break
        timeline = self.timeline_post

        self.assertEqual(self.timeline_post['id'], websocket_post_data['id'],
                         msg=f'Timeline campaign post-id is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline post data "{self.timeline_post}"')
        self.assertEqual(self.timeline_post['campaignId'], websocket_post_data['campaignId'],
                         msg=f'Timeline campaign-id is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline post data "{self.timeline_post}"')
        self.assertEqual(str(self.timeline_post['campaignName'] or ''), str(websocket_post_data['campaignName'] or ''),
                         msg=f'Timeline campaignName is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline post data "{self.timeline_post}"')
        self.assertEqual(self.timeline_post['isSpotlight'], websocket_post_data['spotlight'],
                         msg=f'Timeline spotlight is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline data "{self.timeline_post}"')
        self.assertEqual(self.timeline_post['pinned'], websocket_post_data['pinned'],
                         msg=f'Timeline pinned is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline data "{self.timeline_post}"')
        self.assertEqual(self.timeline_post['isVerdict'], websocket_post_data['verdict'],
                         msg=f'Timeline isVerdict is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline data "{self.timeline_post}"')
        self.assertEqual(self.timeline_post['template']['text'].replace('<p>', ''),
                         websocket_post_data['template']['text'].replace('<p>', ''),
                         msg=f'Timeline template text is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline data "{self.timeline_post}"')
        self.assertFalse(websocket_post_data['template']['topRightCornerImagePath'],
                         msg=f'Timeline template text is not correct in Websocket Post_page call, websocket data" {websocket_post_data}" and created timeline data "{self.timeline_post}"')

        for data in list(timeline['template'].keys()):
            if data == 'createdBy' or data == 'createdByUserName' or data == 'updatedBy' or data == 'updatedByUserName' \
                    or data == 'createdAt' or data == 'updatedAt' or data == 'brand' or data == 'draft' \
                    or data == 'headerIconSvgId' or data == 'postIconSvgId' or data == 'topRightCornerImage' or data == 'text':
                del timeline['template'][data]

        for data in list(websocket_post_data['template'].keys()):
            if data == 'topRightCornerImagePath' or data == 'text':
                del websocket_post_data['template'][data]

        self.assertDictEqual(timeline['template'], websocket_post_data['template'],
                             msg=f'Timeline template data is not correct in websocket data')

    def test_000_preconditions(self):
        """
       PRECONDITIONS: - CMS-API Endpoints: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
       PRECONDITIONS: - Confluence instruction - **How to create Timeline Template, Campaign, Posts** - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
       PRECONDITIONS: - Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
       PRECONDITIONS: - Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
       PRECONDITIONS: - Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
       PRECONDITIONS: - Live Campanig is created
       PRECONDITIONS: - Design - https://app.zeplin.io/project/5dc59d1d83c70b83632e749c/screen/5efc40efdb99fb613a6fcb47
       PRECONDITIONS: User is logged in app
        """

        Timeline = \
            self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration']['FeatureToggle'][
                'Timeline']
        if not Timeline:
            self.cms_config.update_system_configuration_structure(config_item='FeatureToggle', field_name='Timeline',
                                                                  field_value=True)
            timeline = self.cms_config.get_system_configuration_structure()['FeatureToggle']['Timeline']
            self.assertTrue(timeline, msg='"Timeline" is not enabled in CMS')

        timeline_config = self.cms_config.get_timeline_system_configuration()

        if not timeline_config['enabled']:
            self.cms_config.update_timeline_system_config(enabled=True)
            timeline_config_update = self.cms_config.get_timeline_system_configuration()
            self.assertTrue(timeline_config_update['enabled'],
                            msg="Timeline is disabled in timeline system configuration")

        self.__class__.camapign_id = self.get_timeline_campaign_id()

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_campanig(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the Post in the Live Campanig
        EXPECTED: - Post is created and published
        EXPECTED: - Post is displayed on the UI Timeline
        """
        faker = Faker()
        self.__class__.template_name = f'Auto Test template {faker.name()}'
        self.__class__.timeline_template = self.cms_config.create_timeline_template(template_name=self.template_name,
                                                                                    text='test')
        self.__class__.timeline_post = self.cms_config.create_campaign_post(template_id=self.timeline_template['id'],
                                                                            template_name=self.template_name,
                                                                            campaign_id=self.camapign_id,
                                                                            poststatus='PUBLISHED', text='test',
                                                                            headerText=self.template_name)

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        self.site.login()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(),
                        msg='Timeline icon is not present on homepage')

    def test_003_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: - Page with the published post is opened
        EXPECTED: - Content is the same as in CMS
        EXPECTED: - In WS 'Post' response is present with all fields form CMS
        EXPECTED: ![](index.php?/attachments/get/118665503)
        """
        self.site.timeline.timeline_bubble.click()
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict,
                        msg='Timeline campaign is not opened')
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.template_name.upper()],
                        msg=f'Created post {self.template_name} is not displayed on timeline')
        self.validate_ws_post_data()

    def test_004_go_to_cms_and_click_unpublish_button(self):
        """
        DESCRIPTION: Go to CMS and click 'Unpublish' button
        EXPECTED: - Changes are saved
        EXPECTED: - Post is Unpublished
        """
        self.cms_config.update_campaign_post(post_id=self.timeline_post['id'], template_id=self.timeline_template['id'],
                                             template_name=self.template_name, campaign_id=self.camapign_id,
                                             poststatus='UNPUBLISHED')

    def test_005_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: - Page is opened
        EXPECTED: - Unpublished post is not present in the Timeline
        EXPECTED: - In WS 'POST_REMOVED' response is present with fields:
        EXPECTED: ![](index.php?/attachments/get/118665505)
        """
        data = self.get_timeline_websocket_data(delimiter='42', posttype='POST_REMOVED')
        self.assertTrue(data, msg=f'In WS "POST_REMOVED" response is not present')
        self.assertEqual(data['affectedMessageId'], self.timeline_post['id'],
                         msg=f'Timeline post-id is not matching in "Post Removed" WS call')
        ui_timeline_post_list = self.site.timeline.timeline_campaign.items_as_ordered_dict
        timeline_post = self.timeline_template['headerText']
        self.assertNotIn(timeline_post, ui_timeline_post_list.keys(),
                         msg=f'created timeline post "{timeline_post} is not appearing on UI, actual post list {ui_timeline_post_list.keys()}"')

