import pytest
from tests.base_test import vtest
from tests.Common import Common
from faker import Faker
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2
# @pytest.mark.stg2 #Not configured in tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.mobile_only
@vtest
class Test_C59918215_Verify_placing_bet_from_Timeline_for_first_selection(Common):
    """
    TR_ID: C59918215
    NAME: Verify placing bet from Timeline for first selection
    DESCRIPTION: This test case verifies placing bet from Timeline for the first selection
    PRECONDITIONS: "
    PRECONDITIONS: Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts (TBD)
    PRECONDITIONS: 1.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 2.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 3.Timeline posts with prices are created and published
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -User Balance is positive
    PRECONDITIONS: -Betslip is empty
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_000_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        timeline_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle']['Timeline']
        if not timeline_enable:
            self.cms_config.update_system_configuration_structure(config_item='Feature Toggle', field_name='Timeline',
                                                                  field_value=True)
        timeline_system_config = self.cms_config.get_timeline_system_configuration()
        if not timeline_system_config["enabled"]:
            self.assertTrue(self.cms_config.update_timeline_system_config(), "Timeline system config is not enabled")
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
                                                             poststatus='PUBLISHED', text='test',
                                                             headerText=template_name)

        self.__class__.post_name = timeline_post['template']['name']
        self.site.login()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg="Timeline bubble is not displayed")
        actual_title = self.site.timeline.title
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')

    def test_001_tap_on_the_timeline_header(self):
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

    def test_002_tap_on_the_price_button(self):
        """
        DESCRIPTION: Tap on the price button
        EXPECTED: - Quick bet overlay is opened over the top of the timeline
        """
        self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_003_enter_stake_and_click_place_bet(self):
        """
        DESCRIPTION: Enter stake and click 'Place Bet'
        EXPECTED: - Bet is placed successfully with correct date and time
        EXPECTED: - Bet Receipt is displayed
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = "0.10"
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

    def test_004_close_bet_receipt(self):
        """
        DESCRIPTION: Close 'Bet Receipt'
        EXPECTED: - 'Bet Receipt' is closed
        EXPECTED: - Expanded Timeline is displayed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
