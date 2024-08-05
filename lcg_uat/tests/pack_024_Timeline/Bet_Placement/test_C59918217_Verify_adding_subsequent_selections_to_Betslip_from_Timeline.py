import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from faker import Faker
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2 # qa2 setup is not present fr timeline
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.mobile_only
@vtest
class Test_C59918217_Verify_adding_subsequent_selections_to_Betslip_from_Timeline(BaseBetSlipTest):
    """
    TR_ID: C59918217
    NAME: Verify adding subsequent selections to Betslip from Timeline
    DESCRIPTION: Test case verifies adding subsequent selections to Betslip from Timeline or previously added bets
    PRECONDITIONS: "Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 4.Timeline posts with prices is created and published
    PRECONDITIONS: Zeplin Design -
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -Several Bets are already added to Betslip
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        event_ID = event.get('event').get('id')
        outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('No outcomes available')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_Name, selection_ID = list(selection_ids.items())[0]
        faker = Faker()
        template_name = f'New_LoggedInText_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")

        self.cms_config.update_timeline_template(template_id=timeline_template['id'],
                                                 name=template_name,
                                                 eventId=event_ID, selectionId=selection_ID)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text='test',
                                                             headerText=template_name)

        self.__class__.post_name = timeline_post['template']['name']
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
        EXPECTED: - Post with price is displayed
        """
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is opened")
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} with price is not displayed')
        self.assertTrue(
            self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button.text,
            msg=f'post name {self.post_name} with price is not displayed')

    def test_003_tap_on_the_price_button(self):
        """
        DESCRIPTION: Tap on the price button
        EXPECTED: - Green 'selected' state  is applied in timeline for that selection
        EXPECTED: - Selection is added to Betslip
        EXPECTED: - Betslip counter is increased by one
        EXPECTED: - Expanded Timeline is still displaying
        """
        self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline is not expanded")
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertTrue(post.bet_button_selected(), msg=f'Bet button for post "{self.post_name.upper()}" is not selected')
        self.assertEqual(post.bet_button_bg_color, vec.colors.SELECTED_BET_BUTTON_COLOR,
                         msg=f'Actual selected bet button color: "{post.bet_button_bg_color}"'
                             f'is not the same as expected: "{vec.colors.SELECTED_BET_BUTTON_COLOR}"')
        self.site.timeline.timeline_campaign.timeline_minimise.click()
        self.verify_betslip_counter_change(expected_value=1)
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection_Name,
                         msg=f'Actual selection name: "{stake_name}"'
                             f'is not the same as expected: "{self.selection_Name}" for post "{self.post_name.upper()}"')

    def test_004_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: - Selected bet from Timeline is present on Betslip
        """
        # covered in above step

    def test_005_remove_bet_that_was_added_from_timeline_andnavigate_again_to_timeline(self):
        """
        DESCRIPTION: Remove bet that was added from Timeline and
        DESCRIPTION: navigate again to Timeline
        EXPECTED: - 'Selected' state isn't green anymore, it is displayed as an unchecked selection
        """
        self.stake.remove_button.click()
        self.site.timeline.timeline_bubble.click()
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertFalse(post.bet_button_selected(),
                         msg=f'Bet button for post "{self.post_name.upper()}" is selected')
        self.assertNotEqual(post.bet_button_bg_color, vec.colors.SELECTED_BET_BUTTON_COLOR,
                            msg=f'Actual selected bet button color: "{post.bet_button_bg_color}"'
                                f'is same as : "{vec.colors.SELECTED_BET_BUTTON_COLOR}"')
