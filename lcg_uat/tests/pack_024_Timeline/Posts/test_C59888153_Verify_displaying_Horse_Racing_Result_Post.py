import pytest
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59888153_Verify_displaying_Horse_Racing_Result_Post(Common):
    """
    TR_ID: C59888153
    NAME: Verify displaying Horse Racing Result Post
    DESCRIPTION: This test case verifies displaying Horse Racing Result Post
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section ->
    PRECONDITIONS: 'Timeline System Config' item -> 'Enabled' checkbox ) and also Timeline should be turned ON in the general System configuration (CMS  -> 'System configuration' -> 'Structure' -> 'Feature Toggle'    section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS ->   'Timeline' section -> 'Timeline System Config' item -> 'Page URLs'   field )
    PRECONDITIONS: 4.User is logged in
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Ladbrokes:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_1go_to_cms___timeline___timelinecampaign___create_and_publish_postswith_the_following_configuration2results_icon_should_be_configured_intemplate3show_left_side_redblue_line_should_beconfigured_in_templateladbrokes__left_side_red_linecoral__left_side_blue_line4header_text_eg_resultsmarket_rasen_5055subheader_text_eg_queen_motherstakes6filled_text_with_position__price_maxnumber_of_positions__7__1st_horsename_odds_(self):
        """
        DESCRIPTION: "1.Go to CMS -> Timeline -> Timeline
        DESCRIPTION: Campaign -> Create and Publish Posts
        DESCRIPTION: with the following configuration:
        DESCRIPTION: 2.Results Icon (should be configured in
        DESCRIPTION: Template)
        DESCRIPTION: 3.Show Left Side Red/Blue Line (should be
        DESCRIPTION: configured in Template)
        DESCRIPTION: Ladbrokes- Left Side Red Line
        DESCRIPTION: Coral- Left Side Blue Line
        DESCRIPTION: 4.Header Text: e.g. RESULTS:
        DESCRIPTION: MARKET RASEN (5.05)
        DESCRIPTION: 5.Subheader Text: e.g. Queen Mother
        DESCRIPTION: Stakes
        DESCRIPTION: 6.Filled Text with Position & price (max
        DESCRIPTION: number of positions = 7) : 1st: Horse
        DESCRIPTION: name (odds/) "
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
        self.__class__.selection_ID = list(selection_ids.values())[0]
        odds_prices = {i['outcome']['name']: (i['outcome']['children'][0]['price']['priceNum'] + '/' + i['outcome']['children'][0]['price']['priceDen']) for i in outcomes}
        self.__class__.odds_price = list(odds_prices.values())[0]
        faker = Faker()
        template_name = f'New_LoggedInText_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")

        self.cms_config.update_timeline_template(template_id=timeline_template['id'],
                                                 name=template_name,
                                                 eventId=event_ID, selectionId=self.selection_ID)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text=self.post_desc,
                                                             headerText=template_name, postIconSvgId="NewTimelineHorse",
                                                             headerIconSvgId="clock-icon", showLeftSideBlueLine=True, showLeftSideRedLine=True,
                                                             subHeader="subHeader")

        self.__class__.post_name = timeline_post['template']['name']

    def test_002_load_the_app___login____navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
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

    def test_003_tap_on_the_timeline_header(self):
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

    def test_004_verify_displaying_newly_created_results_post(self):
        """
        DESCRIPTION: Verify displaying newly created results post
        EXPECTED: "Results post should be displayed as per designs:
        EXPECTED: 1.Results Icon
        EXPECTED: 2. Red Banner(Ladbrokes)
        EXPECTED: b.Blue Banner(Coral)
        EXPECTED: 3. Result time stamp should not be
        EXPECTED: displayed
        EXPECTED: 4.Title: e.g. RESULTS: MARKET
        EXPECTED: RASEN (5.05)
        EXPECTED: 5.Description: e.g. Queen Mother
        EXPECTED: Stakes
        EXPECTED: 6.Position & price (max number of
        EXPECTED: positions = 7) : 1st: Horse name
        EXPECTED: (odds/)"
        """
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} with price is not displayed')
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_icon,
                        msg=f'post icon is not displayed')
        self.assertTrue(
            self.site.timeline.timeline_campaign.post_banner_color.is_displayed(),
            msg=f'post name with color is not displayed')
        self.assertEqual(
            self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_description,
            self.post_desc, msg=f'Actual post description: "{self.post_desc}" is not equal with the Expected post desc')
        self.assertEqual(
            self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button.text,
            self.odds_price,
            msg=f'Actual post selection_id: "{self.odds_price}" is not equal with the Expected post desc')
