import pytest
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from time import sleep


# @pytest.mark.tst2
# @pytest.mark.stg2 #not configured under tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.mobile_only
@pytest.mark.timeline
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59927329_Verify_Post_with_invalid_event_selection_ID(Common):
    """
    TR_ID: C59927329
    NAME: Verify Post with invalid event/selection ID
    DESCRIPTION: This test case verifies how post should be displayed if it contains invalid event/selection ID
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - -
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Campaign is created
    PRECONDITIONS: 2.Post with corrupted selection is available/configured
    PRECONDITIONS: 3.Post with corrupted event is available/configured
    PRECONDITIONS: 4.Post with corrupted event and selection is available/configured
    PRECONDITIONS: 5. Load the app
    PRECONDITIONS: 6. User is logged in
    PRECONDITIONS: Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes L
    """
    keep_browser_open = True

    def create_timeline_post(self, event_ID, selection_ID):
        faker = Faker()
        template_name = f'New_Template_{faker.city()}'
        Live_Campaign_Id = self.get_timeline_campaign_id()
        timeline_template = self.cms_config.create_timeline_template(template_name=template_name, text="text")
        self.cms_config.update_timeline_template(template_id=timeline_template['id'],
                                                 name=template_name,
                                                 eventId=event_ID, selectionId=selection_ID)
        timeline_post = self.cms_config.create_campaign_post(template_id=timeline_template['id'],
                                                             campaign_id=Live_Campaign_Id,
                                                             poststatus='PUBLISHED', text="text",
                                                             headerText=template_name, postIconSvgId="NewTimelineHorse",
                                                             headerIconSvgId="clock-icon", showTimestamp=True,
                                                             subHeader="subHeader")
        self.__class__.post_name = timeline_post['template']['name']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check timeline Configuration in CMS
        DESCRIPTION: Get Active event id and selection id
        """
        timeline_enable = self.cms_config.get_system_configuration_structure()['FeatureToggle']['Timeline']
        if not timeline_enable:
            self.cms_config.update_system_configuration_structure(config_item='Feature Toggle', field_name='Timeline',
                                                                  field_value=True)
        timeline_system_config = self.cms_config.get_timeline_system_configuration()
        if not timeline_system_config["enabled"]:
            self.assertTrue(self.cms_config.update_timeline_system_config(), "Timeline system config is not enabled")
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.event_ID = event.get('event').get('id')
        outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('No outcomes available')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_ID = list(selection_ids.values())[0]

    def test_001_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'POST' response is present with all fields form CMS in WS
        """
        self.site.login()
        self.assertTrue(self.site.timeline.timeline_bubble.is_displayed(), msg="Timeline bubble is not displayed")
        actual_title = self.site.timeline.title
        expected_title = "CORAL PULSE" if self.brand == 'bma' else "LADBROKES LOUNGE"
        self.assertEqual(actual_title, expected_title, msg=f'Actual title: "{actual_title}" is not equal with the'
                                                           f'Expected title: "{expected_title}"')
        self.assertTrue(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is opened")
        self.site.timeline.timeline_bubble.click()
        self.assertFalse(self.site.timeline.is_lounge_closed(), msg="Timeline bubble is closed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_minimise.is_displayed(),
                        msg="Minimise is not displayed")
        self.assertTrue(self.site.timeline.timeline_campaign.timeline_header, msg="Timeline Header is not displayed")

    def test_002_publish_post_with_invalid_selection_on_cms_and_look_on_ui_app_eg_1298140379_12981f37_1298140_frfrefrev(
            self):
        """
        DESCRIPTION: Publish post with **invalid selection** on CMS and look on UI app, e.g. 1298140379, 12981f37, 1298140, frfrefrev
        EXPECTED: Post is displayed but without price button
        """
        self.create_timeline_post(event_ID=self.eventID, selection_ID="frfrefrev")
        sleep(2)
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} is not displayed')
        self.assertFalse(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button,
                         msg=f'For post {self.post_name} price is displayed')

    def test_003_publish_post_with_invalid_event_on_cms_and_look_on_ui_app_eg_10937881_10937h8_fhury784hf(self):
        """
        DESCRIPTION: Publish post with **invalid event** on CMS and look on UI app, e.g. 10937881, 10937h8, fhury784hf
        EXPECTED: Post is displayed but without price button
        """
        self.create_timeline_post(event_ID="fhury784hf", selection_ID=self.selection_ID)
        sleep(2)
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} is not displayed')
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button,
                        msg=f'For post {self.post_name} price is displayed')

    def test_004_publish_post_with_invalid_selection_and_event_on_cms_and_look_on_ui_eg_selection_id_1298140379_12981f37_1298140_frfrefrev_event_id_10937881_10937h8_fhury784hf(
            self):
        """
        DESCRIPTION: Publish post with **invalid selection and event** on CMS and look on UI, e.g. selection ID: 1298140379, 12981f37, 1298140, frfrefrev; event ID: 10937881, 10937h8, fhury784hf
        EXPECTED: Post is displayed but without price button
        """
        self.create_timeline_post(event_ID="fhury784hf", selection_ID="frfrefrev")
        sleep(2)
        self.assertTrue(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()],
                        msg=f'post name {self.post_name} is not displayed')
        self.assertFalse(self.site.timeline.timeline_campaign.items_as_ordered_dict[self.post_name.upper()].post_bet_button,
                         msg=f'For post {self.post_name} price is displayed')
