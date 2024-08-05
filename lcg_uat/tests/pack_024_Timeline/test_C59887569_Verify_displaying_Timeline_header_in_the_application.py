import pytest
import string
import random
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 # Not configured in tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59887569_Verify_displaying_Timeline_header_in_the_application(Common):
    """
    TR_ID: C59887569
    NAME: Verify displaying Timeline header  in the application
    DESCRIPTION: This test case verifies Timeline header in the application
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
        self.site.login()

        if not self.cms_config.get_timeline_system_configuration()['enabled']:
            self.cms_config.update_timeline_system_config()
        live_campaign_id = self.get_timeline_campaign_id()
        self.assertTrue(live_campaign_id, msg='"Live campaign " is not available.')

        chars = string.ascii_uppercase + string.digits
        postfix = ''.join(random.choice(chars) for _ in range(3))
        template_name = f'Auto Test template {postfix}'

        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text='test')
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             template_name=template_name, campaign_id=live_campaign_id,
                                                             poststatus='DRAFT', text='test')
        self.cms_config.update_campaign_post(post_id=timeline_post['id'], template_id=timeline_template['id'],
                                             template_name=template_name, campaign_id=live_campaign_id,
                                             poststatus='PUBLISHED')

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: 1.Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: 1.'Featured' tab should be opened on the Home page
        EXPECTED: 2.Timeline should be displayed a`t the bottom of the page, above Footer menu
        """
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg=f'"Timeline Bubble" is not displayed')

    def test_002_verify_timeline_header(self):
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
        self.assertTrue(self.site.timeline.title, msg=f'"Timeline Title" is not displayed')
        self.assertEqual(self.site.timeline.timeline_campaign.timeline_header.text, vec.bma.TIMELINE_TITLE,
                         msg=f'Actual header: "{self.site.timeline.timeline_campaign.timeline_header}"'
                             f'is not the same as expected: "{vec.bma.TIMELINE_TITLE}"')

        self.assertTrue(self.site.timeline.new_post_notification, msg=f'"New Post Notification" is not displayed')
        actual_dot_color = self.site.timeline.new_post_bg_color
        self.assertEqual(actual_dot_color, vec.colors.TIMELINE_NEW_POST_NOTIFICATION,
                         msg=f'Actual dot color: "{actual_dot_color}"'
                             f'is not the same as expected: "{vec.colors.TIMELINE_NEW_POST_NOTIFICATION}"')
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg=f'"Timeline Lounge" is not closed')

    def test_003_scroll_up_and_down_on_the_page(self):
        """
        DESCRIPTION: 3.Scroll up and down on the page
        EXPECTED: 1.Timeline header should be sticky to the Footer menu
        EXPECTED: 2.Timeline header should be in collapsed mode
        """
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg=f'"Timeline Bubble" is not displayed')
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg=f'"Timeline Lounge" is not closed')
        self.site.contents.scroll_to_top()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg=f'"Timeline Bubble" is not displayed')
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg=f'"Timeline Lounge" is not closed')
