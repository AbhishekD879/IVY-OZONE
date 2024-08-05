import json
import pytest
from time import sleep
from faker import Faker
from tests.Common import Common
from tests.base_test import vtest


# @pytest.mark.tst2  # qa2 setup is not present for timeline
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59888281_Verify_Publishing_edited_content_on_the_UI(Common):
    """
    TR_ID: C59888281
    NAME: Verify Publishing edited content on the  UI
    DESCRIPTION: This test case verify displaying content on the  UI
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

    def get_timeline_websocket_data(self, delimiter, posttype, post_id):
        """
        This method will get web socket data for type Post_type
        """
        sleep(5)
        logs = self.device.get_performance_log()
        for entry in logs[::-1]:
            try:
                payload_data = entry[1]['message']['message']['params']['response']['payloadData']
                if posttype in payload_data and \
                        payload_data.startswith(str(delimiter)):
                    message = json.loads(payload_data[len(str(delimiter)):])[1]
                    if payload_data.split(str(delimiter), maxsplit=1)[1].split(',')[0].split('[')[1].replace('"',
                                                                                                             '') == posttype and posttype == 'POST_CHANGED':
                        if message['data']['id'] == post_id:
                            return message['data']
                    elif payload_data.split(str(delimiter), maxsplit=1)[1].split(',')[0].split('[')[1].replace('"',
                                                                                                               '') == posttype and posttype == 'POST':
                        if message['id'] == post_id:
                            return message
            except (KeyError, IndexError, AttributeError):
                continue

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
        self.site.login()
        self.site.wait_content_state("Homepage", timeout=30)

    def test_001_go_to_cms_and_create_and_publish_the_post_in_the_live_campanig(self):
        """
        DESCRIPTION: Go to CMS and create and Publish the post in the Live Campanig
        EXPECTED: Post is created and published
        """
        self.__class__.camapign_id = self.get_timeline_campaign_id()
        event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
        market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
        outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
        selection_id = list(all_selection_ids.values())[0]

        self.__class__.event_id = event['event']['id']
        faker = Faker()
        self.__class__.spotlight_template_name = f'Auto Test spotlight template {faker.name()}'
        self.__class__.spotlight_template = self.cms_config.create_timeline_template(
            template_name=self.spotlight_template_name,
            text='test', isSpotlightTemplate=True)
        self.cms_config.update_timeline_template(template_id=self.spotlight_template['id'],
                                                 eventId=self.event_id, selectionId=selection_id,
                                                 showRacingPostLogoInHeader=True,
                                                 betPromptHeader="Racing Post Spotlight", isSpotlightTemplate=True)
        self.__class__.spotlight_timeline_post = self.cms_config.create_campaign_post(template_id=self.spotlight_template['id'],
                                                                                      template_name=self.spotlight_template_name,
                                                                                      campaign_id=self.camapign_id, poststatus='PUBLISHED', text='test',
                                                                                      headerText=self.spotlight_template_name)

        self.__class__.template_name = f'Auto Test template {faker.name()}'
        self.__class__.plain_template = self.cms_config.create_timeline_template(template_name=self.template_name,
                                                                                 text='test')
        self.__class__.plain_timeline_post = self.cms_config.create_campaign_post(template_id=self.plain_template['id'],
                                                                                  template_name=self.template_name,
                                                                                  campaign_id=self.camapign_id,
                                                                                  poststatus='PUBLISHED', text='test',
                                                                                  headerText=self.template_name)

    def test_002_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        self.site.wait_content_state("Homepage", timeout=30)
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(),
                        msg='Timeline icon is not present on homepage')

    def test_003_click_on_the_timeline_ladbrokes_lounge_button_indexphpattachmentsget119084428(self):
        """
        DESCRIPTION: Click on the Timeline 'Ladbrokes Lounge' button ![](index.php?/attachments/get/119084428)
        EXPECTED: - Page with the published post is opened
        EXPECTED: - Content is the same as in CMS
        EXPECTED: - In WS 'POST' response is present with all fields form CMS:
        EXPECTED: ![](index.php?/attachments/get/118665500)
        EXPECTED: ![](index.php?/attachments/get/119084429)
        """
        self.site.timeline.timeline_bubble.click()
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict,
                        msg='Timeline campaign is not opened')
        post_ui = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.spotlight_template_name.upper()]
        self.assertTrue(post_ui, msg=f'Created post {self.plain_timeline_post} is not displayed on timeline')
        self.assertEqual(post_ui.post_description, self.plain_timeline_post['template']['text'],
                         msg=f'post description {self.plain_timeline_post} is not displayed/incorrect on timeline')
        self.assertEqual(post_ui.post_yellow_header, self.plain_timeline_post['template']['yellowHeaderText'].upper(),
                         msg=f'post_yellow_header {self.plain_timeline_post} is not displayed/incorrect on timeline')
        ws_post_page = self.get_timeline_websocket_data(delimiter='42', posttype='POST',
                                                        post_id=self.plain_timeline_post['id'])
        self.assertTrue(ws_post_page, msg='Websocket "Post" call is not present')
        self.assertEqual(ws_post_page['template']['headerText'], self.plain_timeline_post['template']['headerText'],
                         msg=f'Header text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_timeline_post}"')
        self.assertEqual(ws_post_page['template']['yellowHeaderText'],
                         self.plain_timeline_post['template']['yellowHeaderText'],
                         msg=f'yellowHeaderText is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_timeline_post}"')
        self.assertEqual(ws_post_page['template']['text'].replace('<p>', ''),
                         self.plain_timeline_post['template']['text'].replace('<p>', ''),
                         msg=f'Template text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_timeline_post}"')
        self.assertEqual(ws_post_page['template']['id'], self.plain_timeline_post['template']['id'],
                         msg=f'Template-id is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_timeline_post}"')
        self.assertEqual(ws_post_page['id'], self.plain_timeline_post['id'],
                         msg=f'Post-id is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_timeline_post}"')

    def test_004___go_to_cms_and_edit_verdictspotlight_post__try_to_edit_all_fieldsindexphpattachmentsget118702615__click_save_and_publish_button(
            self):
        """
        DESCRIPTION: - Go to CMS and edit Verdict/Spotlight post
        DESCRIPTION: - Try to edit all fields
        DESCRIPTION: ![](index.php?/attachments/get/118702615)
        DESCRIPTION: - Click 'Save and Publish' button
        EXPECTED: - All fields except text is editable for Verdict/Spotlight post
        EXPECTED: - Changes are saved
        EXPECTED: - Post is Published
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
        self.__class__.eventID = event['event']['id']
        outcomes_resp = event['event']['children'][0]['market']['children']
        self.__class__.selection_id, price_resp = next(((i['outcome']['id'], i['outcome']['children'][0]['price'])
                                                          for i in outcomes_resp if
                                                          i['outcome'].get('children') and 'price' in
                                                          i['outcome']['children'][0].keys()),
                                                         (outcomes_resp[0]['outcome']['name'], ''))
        self.__class__.price = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}' if price_resp else 'SP'  # if price response is empty -> SP

        self.__class__.text = 'testing'
        self.__class__.betPromptHeader = "Racing Post Spotlight Test"
        self.__class__.yellowHeaderText = "Updated yellow header text"
        self.__class__.updated_spotlight_template_name = self.spotlight_template_name + " " + 'test'
        self.__class__.spotlight_template_update = self.cms_config.update_campaign_post(
            post_id=self.spotlight_timeline_post['id'],
            text=self.text, headerText=self.updated_spotlight_template_name,
            eventId=self.event_id, selectionId=self.selection_id, poststatus='PUBLISHED',
            betPromptHeader=self.betPromptHeader, yellowHeaderText=self.yellowHeaderText)

    def test_005_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: - Page with published post is opened
        EXPECTED: - Content is the same as in CMS
        EXPECTED: - In WS 'POST_CHANGED' response is present with fields:
        EXPECTED: ![](index.php?/attachments/get/118665570)
        """
        # Since changes are taking time to reflect on UI hence added sleep
        sleep(5)
        update_post = self.site.timeline.timeline_campaign.items_as_ordered_dict[
            self.updated_spotlight_template_name.upper()]
        self.assertTrue(update_post,
                        msg=f'Updated spotlight post {self.updated_spotlight_template_name} is not displayed on timeline')
        self.assertEqual(update_post.post_yellow_header, self.yellowHeaderText.upper(),
                         msg=f'updated post_yellow_header {self.yellowHeaderText} is not displayed/incorrect on timeline updated post')
        self.assertEqual(update_post.post_bet_prompt_header, self.betPromptHeader,
                         msg=f'updated post_bet_prompt_header {self.betPromptHeader} is not displayed/incorrect on timeline updated post')
        self.assertEqual(update_post.post_description, self.text,
                         msg=f'updated post_description {self.text} is not displayed/incorrect on timeline updated post')
        self.assertEqual(update_post.post_bet_button.text, self.price,
                         msg=f'updated post_price {self.price} is not displayed/incorrect on timeline updated post')
        ws_post_page = self.get_timeline_websocket_data(delimiter='42', posttype='POST_CHANGED',
                                                        post_id=self.spotlight_template_update['id'])
        self.assertTrue(ws_post_page, msg='Websocket "Post_page" call is not present')
        self.assertEqual(ws_post_page['template']['headerText'], self.updated_spotlight_template_name,
                         msg=f'Post Header text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')
        self.assertEqual(ws_post_page['template']['yellowHeaderText'], self.yellowHeaderText,
                         msg=f'Post yellowHeaderText is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')
        self.assertEqual(ws_post_page['template']['text'].replace('<p>', ''), self.text,
                         msg=f'Template text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')
        self.assertEqual(ws_post_page['template']['betPromptHeader'], self.betPromptHeader,
                         msg=f'Template text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')
        self.assertEqual(ws_post_page['template']['eventId'], self.event_id,
                         msg=f'Event-id is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')
        self.assertEqual(ws_post_page['template']['selectionId'], self.selection_id,
                         msg=f'Selection-id text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')

    def test_006___go_to_cms_and_edit_simple_post__try_to_edit_all_fieldsindexphpattachmentsget118702616__click_save_and_publish_button(
            self):
        """
        DESCRIPTION: - Go to CMS and edit simple post
        DESCRIPTION: - Try to edit all fields
        DESCRIPTION: ![](index.php?/attachments/get/118702616)
        DESCRIPTION: - Click 'Save and Publish' button
        EXPECTED: - All fields and also text is editable for post
        EXPECTED: - Changes are saved
        EXPECTED: - Post is Published
        """
        self.__class__.updated_template_name = self.template_name + " " + 'test'
        self.__class__.plain_template_update = self.cms_config.update_campaign_post(
            post_id=self.plain_timeline_post['id'], text=self.text,
            headerText=self.updated_template_name, poststatus='PUBLISHED', yellowHeaderText=self.yellowHeaderText)

    def test_007_return_to_the_posts_page_on_ui(self):
        """
        DESCRIPTION: Return to the Posts page on UI
        EXPECTED: - Page with published post is opened
        EXPECTED: - Content is the same as in CMS
        EXPECTED: - In WS 'POST_CHANGED' response is present with fields:
        EXPECTED: ![](index.php?/attachments/get/118665570)
        """
        # Since changes are taking time to reflect on UI hence added sleep
        sleep(5)
        updated_post_ui = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.updated_template_name.upper()]
        self.assertTrue(updated_post_ui,
                        msg=f'Updated post {self.updated_template_name} is not displayed on timeline')
        self.assertEqual(updated_post_ui.post_description, self.text,
                         msg=f'updated post_description {self.text} is not displayed/incorrect on timeline updated post')
        self.assertEqual(updated_post_ui.post_yellow_header, self.yellowHeaderText.upper(),
                         msg=f'updated post_yellow_header {self.yellowHeaderText} is not displayed/incorrect on timeline updated post')
        ws_post_page = self.get_timeline_websocket_data(delimiter='42', posttype='POST_CHANGED',
                                                        post_id=self.plain_template_update['id'])
        self.assertTrue(ws_post_page, msg='Websocket "Post_page" call is not present')

        self.assertEqual(ws_post_page['template']['headerText'], self.updated_template_name,
                         msg=f'Post Header text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_template_update}"')
        self.assertEqual(ws_post_page['template']['text'].replace('<p>', ''), self.text,
                         msg=f'Template text is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.plain_template_update}"')
        self.assertEqual(ws_post_page['template']['yellowHeaderText'], self.yellowHeaderText,
                         msg=f'Post yellowHeaderText is incorrect in websocket call, web socket call "{ws_post_page}" and CMS data "{self.updated_spotlight_template_name}"')
