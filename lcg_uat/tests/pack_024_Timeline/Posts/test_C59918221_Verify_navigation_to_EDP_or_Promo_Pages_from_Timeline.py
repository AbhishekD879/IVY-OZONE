import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from faker import Faker


# @pytest.mark.tst2  # Not configured for tst2
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59918221_Verify_navigation_to_EDP_or_Promo_Pages_from_Timeline(Common):
    """
    TR_ID: C59918221
    NAME: Verify navigation to EDP or Promo Pages from Timeline
    DESCRIPTION: This test case verifies navigation to EDP or Promo Pages from Timeline
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.Template is created with the following attributes:
    PRECONDITIONS: I.'Post Href' (link to EDP or Promo page)
    PRECONDITIONS: ii.Show Redirect Arrow' checkbox is checked
    PRECONDITIONS: 5.Timeline posts with additional navigation are created and published
    PRECONDITIONS: 6.Load the app
    PRECONDITIONS: 7.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True
    href_url = "https://" + tests.HOSTNAME + "/sport/football/matches"

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: "
        PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
        PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
        PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
        PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
        PRECONDITIONS: 4.Template is created with the following attributes:
        PRECONDITIONS: I.'Post Href' (link to EDP or Promo page)
        PRECONDITIONS: ii.Show Redirect Arrow' checkbox is checked
        PRECONDITIONS: 5.Timeline posts with additional navigation are created and published
        PRECONDITIONS: 6.Load the app
        PRECONDITIONS: 7.User is logged in
        PRECONDITIONS: Note:
        PRECONDITIONS: Desktop means Mobile Emulator
        PRECONDITIONS: Timeline feature is for both Brands:
        PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
        PRECONDITIONS: Coral- Coral Pulse"
        """
        self.site.login(async_close_dialogs=True)
        faker = Faker()
        template_name = f'New_LoggedInText_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text",
                                                                     postHref=self.href_url, showRedirectArrow=True)

        self.cms_config.update_timeline_template(template_id=timeline_template['id'], name=template_name,
                                                 postHref=self.href_url, showRedirectArrow=True)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text='test',
                                                             headerText=template_name)

        self.__class__.post_name = timeline_post['template']['name']

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        self.site.wait_content_state("Homepage")
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg="Timeline bubble is not displayed")
        actual_title = self.site.timeline.title
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - Post with additional navigation is displayed, Redirect Arrow is shown
        """
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is opened")
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} with price is not displayed')

    def test_003_tap_on_the_navigation_clickable_area(self):
        """
        DESCRIPTION: Tap on the navigation clickable area
        EXPECTED: - User is navigated to the target location (EDP Page; Promotions page)
        EXPECTED: (location should be the same as configured in CMS)
        EXPECTED: - Timeline widget is minimized to allow the user to view target content
        """
        self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_redirection_link.click()
        self.site.wait_content_state_changed(timeout=10)
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.href_url, msg="Timeline redirection arrow navigated to wrong page")
