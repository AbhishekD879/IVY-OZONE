import pytest
import string
import random
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2  #Not configured in tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C60006362_Verify_displaying_Racing_Post(Common):
    """
    TR_ID: C60006362
    NAME: Verify displaying Racing Post
    DESCRIPTION: This test case verifies displaying Racing Post
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.Campaign should be configured
    PRECONDITIONS: 5.'Spotlight' and 'Verdict' Templates should be configured
    PRECONDITIONS: 6.Spotlight and Verdict Posts should be created and published (CMS -> 'Timeline' section -> 'Timeline Campaign' item -> 'Spotlights' button)-> -> Insert classIds in the 'Fetch for classIds' field (e.g. 226,223)-> Click 'Refresh Events' button-> -> Click on the event time of the one event-> Click 'Create Post' in Spotlight/Verdict section)
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check timeline is status in CMS System Configuration
        """
        if not self.cms_config.get_timeline_system_configuration():
            self.cms_config.update_timeline_system_config()

    def test_001_load_the_app___login____navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Load the app -> Login ->
        DESCRIPTION: -> Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        chars = string.ascii_uppercase
        postfix = ''.join(random.choice(chars) for _ in range(3))
        self.__class__.template_name = f'Racing Post Verdict {postfix}'

        postfix = ''.join(random.choice(chars) for _ in range(3))
        self.__class__.template_name1 = f'Racing Post Spotlight {postfix}'

        self.__class__.cms_context = f'"Racing Post Verdict Description"'
        self.__class__.cms_context1 = f'"Racing Post Spotlight Description"'

        icon = 'LadsLoungeRacing' if self.brand == 'ladbrokes' else 'icn-grey-28-x-28-horse-racing'
        Live_Campaign_Id = self.get_timeline_campaign_id()

        timeline_template = self.cms_config.create_timeline_template(template_name=self.template_name,
                                                                     text="Racing Post Verdict",
                                                                     isVerdictTemplate=True)
        timeline_template1 = self.cms_config.create_timeline_template(template_name=self.template_name1,
                                                                      text="Racing Post Spotlight",
                                                                      isSpotlightTemplate=True)

        template = [timeline_template, timeline_template1]
        events = self.cms_config.spotlight_related_events(class_id=223)
        event_id = events["typeEvents"][0]["events"][0]["id"]
        spotlight_data = self.cms_config.get_spotlight_data(event_id=event_id, campaign_id=Live_Campaign_Id)
        selection_id = spotlight_data["horses"][00]["selectionId"]
        header = self.template_name
        verdict_value = True
        sl_value = False
        for temp in template:
            if temp['name'] == self.template_name1:
                self.cms_context = self.cms_context1
                header = self.template_name1
                sl_value = True
                verdict_value = False
            self.cms_config.update_timeline_template(template_id=temp['id'],
                                                     showRacingPostLogoInHeader=True,
                                                     eventId=event_id,
                                                     selectionId=selection_id,
                                                     betPromptHeader="Racing Post",
                                                     postIconSvgId=icon,
                                                     isVerdictTemplate=verdict_value,
                                                     isSpotlightTemplate=sl_value)
            self.cms_config.create_campaign_post(template_id=temp['id'],
                                                 campaign_id=Live_Campaign_Id,
                                                 poststatus='PUBLISHED',
                                                 text=self.cms_context,
                                                 headerText=header,
                                                 yellowHeaderText='')

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline is opened and displayed in the expanded state
        """
        self.site.login()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), "TimeLine Bubble not displayed on UI")
        self.assertTrue(self.site.timeline.title, "Timeline title not displayed On UI")
        self.site.timeline.timeline_bubble.click()
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        "Timeline is not maximised after bubble click")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header,
                        "Timeline header not displayed after click")

    def test_003_verify_displaying_racing_post_verdict(self):
        """
        DESCRIPTION: Verify displaying Racing Post Verdict
        EXPECTED: Racing Post post title with CMS content is displayed as per design:
        EXPECTED: - Timestamp
        EXPECTED: - Icon (for selected template)
        EXPECTED: - Race name
        EXPECTED: - Racing Post label: **Verdict**
        EXPECTED: - Content box
        EXPECTED: - Price button (if it configured)
        EXPECTED: ![](index.php?/attachments/get/120869382)
        """
        post_ui = self.site.timeline.timeline_campaign.items_as_ordered_dict[
            self.template_name.upper()]
        self.assertTrue(post_ui, f'Post Created in CMS{self.template_name.upper()} not displayed on UI')
        self.assertTrue(post_ui.post_time,
                        f'Post time for {self.template_name.upper()} not displayed on UI')
        self.assertTrue(post_ui.post_icon.is_displayed(),
                        f'Post ICON for {self.template_name.upper()} not displayed on UI')
        self.assertTrue(post_ui.post_bet_button.is_displayed(),
                        f'Post ICON for {self.template_name.upper()} not displayed on UI')
        self.assertEqual(post_ui.name, self.template_name.upper(),
                         f'Post name is {post_ui.name}'
                         f'is not same as expected {self.template_name.upper()}')
        self.assertEqual(post_ui.post_description, self.cms_context,
                         f'Post name is {post_ui.post_description}'
                         f'is not same as expected {self.cms_context}')
        self.assertEqual(post_ui.post_verdict, "VERDICT",
                         f'Post verdict for {self.template_name.upper()} not displayed on UI')

    def test_004_verify_displaying_racing_post_spotlight(self):
        """
        DESCRIPTION: Verify displaying Racing Post Spotlight
        EXPECTED: Racing Post post tile with CMS content is displayed as per design:
        EXPECTED: - Timestamp
        EXPECTED: - Icon (for selected template)
        EXPECTED: - Race name
        EXPECTED: - Racing Post label: **Spotlight**
        EXPECTED: - Content box
        EXPECTED: - Price button (if it configured)
        EXPECTED: ![](index.php?/attachments/get/120869383)
        """
        post_ui = list(self.site.timeline.timeline_campaign.items_as_ordered_dict.values())[0]
        self.assertTrue(post_ui, f'Post Created in CMS{self.template_name1.upper()} not displayed on UI')
        self.assertTrue(post_ui.post_time,
                        f'Post time for {self.template_name1.upper()} not displayed on UI')
        self.assertTrue(post_ui.post_icon.is_displayed(),
                        f'Post ICON for {self.template_name1.upper()} not displayed on UI')
        self.assertTrue(post_ui.post_bet_button.is_displayed(),
                        f'Post ICON for {self.template_name1.upper()} not displayed on UI')
        self.assertEqual(post_ui.name, self.template_name1.upper(),
                         f'Post name is {post_ui.name}'
                         f'is not same as expected {self.template_name1.upper()}')
        self.assertEqual(post_ui.post_description, self.cms_context1,
                         f'Post name is {post_ui.post_description}'
                         f'is not same as expected {self.cms_context1}')
        self.assertEqual(post_ui.post_spotlight, "SPOTLIGHT",
                         f'Post spotlight for {self.template_name1.upper()} not displayed on UI')
