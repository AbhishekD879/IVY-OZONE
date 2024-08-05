import pytest
from faker import Faker
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2  # not configured under tst2
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59918218_Verify_state_of_selection_in_App_if_it_is_already_added_to_Betslip_from_Timeline_and_vice_versa(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C59918218
    NAME: Verify state of selection in App  if it is already added to Betslip from Timeline and vice versa
    DESCRIPTION: This test case verifies the state of selection in App if it is already added to Betslip from Timeline and vice versa
    PRECONDITIONS: "Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 4.Timeline posts with prices are created and published
    PRECONDITIONS: Zeplin Design -
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -Selection from app is already added to Betslip. The same selection is configured in Timeline
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
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.event_ID = event.get('event').get('id')
        outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('No outcomes available')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_name1, self.__class__.selection_id1 = list(selection_ids.items())[0]
        selection_ID = list(selection_ids.values())[0]
        faker = Faker()
        template_name = f'New_LoggedInText_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")

        self.cms_config.update_timeline_template(template_id=timeline_template['id'],
                                                 name=template_name,
                                                 eventId=self.event_ID, selectionId=selection_ID)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text='test',
                                                             headerText=template_name)

        self.__class__.post_name = timeline_post['template']['name']
        self.site.login()
        self.navigate_to_edp(event_id=self.event_ID, sport_name='football', timeout=10)
        self.__class__.bet_button = self.get_selection_bet_button(selection_name=self.selection_name1, market_name=None)
        self.bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg="Timeline bubble is not displayed")
        actual_title = self.site.timeline.title
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - **Green 'selected' state is shown in timeline for that selection that already added to Betslip from app**
        """
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is opened")
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertTrue(post.bet_button_selected(),
                        msg=f'Bet button for post "{self.post_name.upper()}" is not selected')
        self.assertEqual(post.bet_button_bg_color, vec.colors.SELECTED_BET_BUTTON_COLOR,
                         msg=f'Actual selected bet button color: "{post.bet_button_bg_color}"'
                             f'is not the same as expected: "{vec.colors.SELECTED_BET_BUTTON_COLOR}"')

    def test_003___uncheck_this_selection__navigate_to_page_in_app_where_it_was_selected_beforeeg_edp_page(self):
        """
        DESCRIPTION: - Uncheck this selection
        DESCRIPTION: - Navigate to page in app where it was selected before,e.g. EDP page
        EXPECTED: - 'Selected' state isn't green anymore, it is displayed as an unchecked selection
        EXPECTED: - This selection is removed from Betslip
        """
        self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button.click()
        self.navigate_to_edp(event_id=self.event_ID, sport_name='football')
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertFalse(post.bet_button_selected(),
                         msg=f'Bet button for post "{self.post_name.upper()}" is selected')
        self.assertNotEqual(post.bet_button_bg_color, vec.colors.SELECTED_BET_BUTTON_COLOR,
                            msg=f'Actual selected bet button color: "{post.bet_button_bg_color}"'
                                f'is same as : "{vec.colors.SELECTED_BET_BUTTON_COLOR}"')
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_004___navigate_to_timeline_again_and__tap_on_the_price_button_and_add_to_betslip(self):
        """
        DESCRIPTION: - Navigate to Timeline again and
        DESCRIPTION: - Tap on the price button and add to Betslip
        EXPECTED: - Green 'selected' state is applied in timeline for that selection
        EXPECTED: - Selection is added to Betslip
        EXPECTED: - Betslip counter is increased by one
        """
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")
        self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.expected_betslip_counter_value = 1
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_005___minimize_timeline__navigate_to_app_where_this_selection_is_shown(self):
        """
        DESCRIPTION: - Minimize Timeline
        DESCRIPTION: - Navigate to app where this selection is shown
        EXPECTED: - **Green 'selected' state is shown in elsewhere in the app (e.g EDP)**
        """
        self.site.timeline.timeline_campaign.timeline_minimise.click()
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is still opened")
        self.navigate_to_edp(event_id=self.event_ID, sport_name='football')
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertTrue(post.bet_button_selected(),
                        msg=f'Bet button for post "{self.post_name.upper()}" is not selected')
        self.assertTrue(post.bet_button_selected(),
                        msg=f'Bet button for post "{self.post_name.upper()}" is not selected')
        self.assertEqual(post.bet_button_bg_color, vec.colors.SELECTED_BET_BUTTON_COLOR,
                         msg=f'Actual selected bet button color: "{post.bet_button_bg_color}"'
                             f'is not the same as expected: "{vec.colors.SELECTED_BET_BUTTON_COLOR}"')

    def test_006_navigate_to_the_betslip_and_remove_this_selection(self):
        """
        DESCRIPTION: Navigate to the Betslip and Remove this selection
        EXPECTED: 'Selected' state isn't green anymore, it is displayed as an unchecked selection for Timeline as well as for elsewhere in the app
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection_name1,
                         msg=f'Actual selection name: "{stake_name}"'
                             f'is not the same as expected: "{self.selection_name1}" for post "{self.post_name.upper()}"')
        stake.remove_button.click()
        self.assertFalse(self.bet_button.is_selected(timeout=2),
                         msg=f'Bet button "{self.selection_name1}" is active after selection')
        self.site.timeline.timeline_bubble.click()
        sleep(3)
        post = self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()]
        self.assertFalse(post.bet_button_selected(),
                         msg=f'Bet button for post "{self.post_name.upper()}" is selected')
        self.assertNotEqual(post.bet_button_bg_color, vec.colors.SELECTED_BET_BUTTON_COLOR,
                            msg=f'Actual selected bet button color: "{post.bet_button_bg_color}"'
                                f'is same as : "{vec.colors.SELECTED_BET_BUTTON_COLOR}"')
