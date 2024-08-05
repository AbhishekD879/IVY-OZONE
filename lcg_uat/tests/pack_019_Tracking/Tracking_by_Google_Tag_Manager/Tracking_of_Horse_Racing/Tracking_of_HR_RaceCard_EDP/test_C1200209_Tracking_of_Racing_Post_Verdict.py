import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.prod
@pytest.mark.lad_beta2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.google_analytics
@pytest.mark.safari
@pytest.mark.race_form
@pytest.mark.low
@pytest.mark.other
@pytest.mark.login
@pytest.mark.hl
@pytest.mark.other
@pytest.mark.reg167_fix
@vtest
class Test_C1200209_Tracking_of_Racing_Post_Verdict(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1200209
    NAME: Tracking of Racing Post 'Verdict'
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of click on Show More link in the Racing Post 'Verdict'
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("HomePage")

    def test_002_navigate_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")

    def test_003_click_on_the_event(self):
        """
        DESCRIPTION: Click on the event
        EXPECTED: 'Event details' page is opened
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find any sections')
        events = sections.get(vec.Racing.UK_AND_IRE_TYPE_NAME.upper())
        event_names = events.items_as_ordered_dict
        self.assertTrue(event_names, msg='Can not find any events')
        event_name = list(event_names.keys())[0]
        meetings = event_names.get(event_name).items_as_ordered_dict
        self.assertTrue(meetings, msg='Can not find any meetings')
        for event_name, event in meetings.items():
            race_started = event.is_resulted or event.has_race_off()
            if not race_started:
                event.click()
                self.site.wait_content_state('RacingEventDetails')
                break
        if self.site.wait_for_my_stable_onboarding_overlay():
                self.site.my_stable_onboarding_overlay.close_button.click()

    def test_004_click_on_show_more_link_to_expand_the_racing_post_verdict(self):
        """
        DESCRIPTION: Click on 'Racing Post Verdict' to expand the Racing Post 'Verdict'
        EXPECTED: Racing Post 'Verdict' is shown expanded
        """
        post_info = self.site.racing_event_details.tab_content.post_info
        self.assertTrue(post_info.logo_icon.is_displayed(),
                        msg='"Racing Post | Verdict" logo is not displayed')
        post_info.logo_icon.click()

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'horse racing',
        EXPECTED: 'eventAction': 'race card',
        EXPECTED: 'eventLabel': 'racing post verdict'
        EXPECTED: })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='racing post verdict')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': 'race card',
                             'eventLabel': 'racing post verdict',
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_006_repeat_steps_1_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Logged In user
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.login(async_close_dialogs=False)
        self.test_002_navigate_to_the_horse_racing_page()
        self.test_003_click_on_the_event()
        self.test_004_click_on_show_more_link_to_expand_the_racing_post_verdict()
        self.test_005_type_in_browser_console_datalayer_and_tap_enter()
