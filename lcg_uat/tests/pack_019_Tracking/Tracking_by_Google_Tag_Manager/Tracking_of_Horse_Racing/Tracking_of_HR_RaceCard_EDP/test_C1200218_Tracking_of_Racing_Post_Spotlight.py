import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1200218_Tracking_of_Racing_Post_Spotlight(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1200218
    NAME: Tracking of Racing Post 'Spotlight'
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of click on 'Show more' link in Racing Post 'Spotlight'
    PRECONDITIONS: 1. Test case should be run on Mobile
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_navigate_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")

    def test_003_navigate_to_the_event_details_page_where_horse_additional_info_is_present_silks_number_etc(self):
        """
        DESCRIPTION: Navigate to the event details page where horse additional info is present (silks, number, etc)
        EXPECTED: Event details page is opened
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find any sections')
        events = sections.get(vec.Racing.UK_AND_IRE_TYPE_NAME.upper())
        event_names = events.items_as_ordered_dict
        self.assertTrue(event_names, msg='Event_names is not displayed')
        event_name = list(event_names.keys())[0]
        meetings = event_names.get(event_name).items_as_ordered_dict
        self.assertTrue(meetings, msg='Meetings is not displayed')
        meeting = list(meetings.keys())[4]
        self.__class__.event_id = meetings[meeting].event_id
        self.__class__.type_id = self.ss_req.ss_event_to_outcome_for_event(self.event_id)[0]['event']['typeId']
        meetings[meeting].click()

    def test_004_click_on_the_show_more_link_to_expend_racing_post_spotlight(self):
        """
        DESCRIPTION: Click on the 'Show More' link to expend Racing Post 'Spotlight'
        EXPECTED: Racing Post 'Spotlight' is shown expanded
        """
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found on page')
        section_name, section = list(sections.items())[0]
        self.assertTrue(sections, msg='No one section was found on page')
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Can not find outcomes')
        for outcome_name, outcome in list(outcomes.items()):
            if outcome_name != 'Unnamed Favourite':
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'Outcome of "{outcome_name}" doesn\'t have show summary toggle')
                outcome.show_summary_toggle.click()
                if self.brand != 'ladbrokes':
                    if outcome.expanded_summary.spotlight_info.has_show_summary_button():
                        outcome.expanded_summary.spotlight_info.show_summary_button.click()
                        break
                    else:
                        continue
            break

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'race card',
        EXPECTED: 'eventLabel' : 'details'
        EXPECTED: })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='show more')
        expected_response = {'event': 'trackEvent', 'eventAction': 'race card', 'eventCategory': 'horse racing', 'eventLabel': 'show more', 'categoryID': '21', 'typeID': int(self.type_id), 'eventID': int(self.event_id)}
        self.compare_json_response(actual_response, expected_response)

    def test_006_repeat_steps_1_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Logged In user
        EXPECTED:
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.login()
        self.test_002_navigate_to_the_horse_racing_page()
        self.test_003_navigate_to_the_event_details_page_where_horse_additional_info_is_present_silks_number_etc()
        self.test_004_click_on_the_show_more_link_to_expend_racing_post_spotlight()
        self.test_005_type_in_browser_console_datalayer_and_tap_enter()
