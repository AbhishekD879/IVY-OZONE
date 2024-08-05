import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.helpers import get_matching_response_url, do_request
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.adhoc_suite
@pytest.mark.my_stable
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C66037542_Verify_the_GA_tracking_for_various_actions_performed_on_the_My_Stable_Onboarding_tutorial(
    BaseDataLayerTest):
    """
    TR_ID: C66037542
    NAME: Verify the GA tracking for various actions performed on the My Stable  Onboarding tutorial.
    DESCRIPTION: This test case evaluates the GA tracking for various actions performed on the My Stable Onboarding tutorial pop up.
    PRECONDITIONS: CMS configurations
    PRECONDITIONS: My Stable Menu item
    PRECONDITIONS: My Stable Configurations
    PRECONDITIONS: Checkbox against ‘Active Mystable’ - Should be checked in
    PRECONDITIONS: Checkbox against ‘Mystable Horses Running Today Carousel’ - Should be checked in
    PRECONDITIONS: Checkbox against ‘Active Antepost’ - Should be checked in
    PRECONDITIONS: Checkbox against ‘Active My Bets’ (Phase 2)
    PRECONDITIONS: My Stable Entry Point
    PRECONDITIONS: Entry Point SVG Icon - (Mystable-Entry-Point-White)
    PRECONDITIONS: Entry Point Label  - Ladbrokes (Stable Mates)/ Coral (My Stable)
    PRECONDITIONS: Edit Or Save My Stable
    PRECONDITIONS: Edit Stable Svg Icon - (Mystable-Entry-Point-Dark)
    PRECONDITIONS: Edit Stable Label - (Edit Stable)
    PRECONDITIONS: Save Stable Svg Icon - ( Mystable-Entry-Point-White)
    PRECONDITIONS: Save Stable Label -(Done)
    PRECONDITIONS: Edit Note Svg Icon - (Mystable-Edit-Note)
    PRECONDITIONS: Bookmark Svg Icon -(bookmarkfill)
    PRECONDITIONS: InProgress Bookmark Svg icon -(Mystable-Inprogress-Bookmark)
    PRECONDITIONS: Unbookmark Svg Icon -(bookmark)
    PRECONDITIONS: Empty My Stable
    PRECONDITIONS: Empty Stable Sag Icon - Mystable-Stable-Signposting
    PRECONDITIONS: Empty Stable Header Label - Empty Stable
    PRECONDITIONS: Empty Stable Message Label - Tap on ‘Edit Stable’ on the Race Card to add a horse
    PRECONDITIONS: Empty Stable CTA Label - View my horses
    PRECONDITIONS: My Stable Signposting
    PRECONDITIONS: Signposting Svg Icon - Mystable-Stable-Signposting
    PRECONDITIONS: Notes Signposting Svg Icon-Mystable-Note-Signposting
    PRECONDITIONS: Your Horses Running Today Carousel
    PRECONDITIONS: Carousel Icon - Mystable-Entry-Point-Dark
    PRECONDITIONS: Carousel Name - Your horses running today!
    PRECONDITIONS: Error Message Popups
    PRECONDITIONS: Maximum Horses Exceed Message - Maximum number of  selections reached. To add more, remove horses from your stable.
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def navigate_to_horse_racing_uk_irish_races_edp(self):
        """
        Navigates to the 'horse-racing' page
        Selects the 'MEETINGS' or 'FEATURED' tab based on the brand,
        and clicks on a specific Meeting's event.
        """
        # Navigate to the Horse Racing SLP page
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        # Selects the 'MEETINGS' or 'FEATURED' tab based on the brand
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        tab = next((tab for name, tab in tabs.items() if (name.upper() == 'MEETINGS' and self.brand != 'bma') or (
                name.upper() == 'FEATURED' and self.brand == 'bma')), None)
        tab.click()

        # Getting a specific Meeting
        uk_irish_races = list(self.site.horse_racing.tab_content.accordions_list.get_items(
            name=vec.racing.UK_AND_IRE_TYPE_NAME.upper()).values())[0]
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

        # click on the Meeting's event time
        meeting = list(uk_irish_races.get_items(number=1).values())[0]
        events = meeting.items_as_ordered_dict
        event = next(iter(events.values()))
        event.scroll_to_we()
        event.click()
        self.site.wait_content_state(state_name='RACINGEVENTDETAILS')

    def get_event_data(self):
        event_id = None
        parts = self.device.get_current_url().split('/')
        for part in reversed(parts):
            if part.isnumeric():
                event_id = str(part)
                break
        response_url = get_matching_response_url(self, urls=['EventToOutcomeForEvent', event_id])
        self.assertTrue(response_url, msg='EventToOutcomeForEvent data is not received.')
        response = do_request(method='GET', url=response_url)
        self.assertTrue(response, msg='No response received for the "EventToOutcomeForEvent" call')

        self.__class__.event_data = response["SSResponse"]["children"][0]["event"]

    def close_stream_and_bet_overlay_and_get_event_data(self):
        self.get_event_data()

        try:
            if self.site.wait_for_stream_and_bet_overlay(timeout=10):
                overlay = self.site.stream_and_bet_overlay
                if overlay and overlay.is_displayed():
                    overlay.close_button.click()
        except:
            pass

        events = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        event = list(events.values())[len(events) - 1]
        event.click()
        self.site.wait_content_state_changed()
        self.get_event_data()

        self.assertTrue(self.site.wait_for_my_stable_onboarding_overlay())

    def test_000_precondition(self):
        """
        PRECONDITIONS: Verify if My stable Page is active in CMS or not.
        """
        my_stable_status_in_cms = self.cms_config.get_my_stable_config().get('active')
        if not my_stable_status_in_cms:
            raise CmsClientException('My stable Page is not active in CMS')

    def test_001_verify_the_ga_tracking_when_user_gets_the_my_stable_onboarding_tutorialuser_should_be_logged_in_and_navigate_to_the_horse_racing_event_details_page_win_or_each_way_market_tab(
            self):
        """
        DESCRIPTION: Verify the GA tracking when user gets the My Stable Onboarding tutorial.(User should be logged in and navigate to the Horse racing event details page (Win or Each Way market tab).
        EXPECTED: User should be able to view the My Stable Onboarding tutorial in the FE.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'contentView',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'load',
        EXPECTED: component.PositionEvent: 'welcome to my stable overlay',
        EXPECTED: component.LocationEvent:'{selected race}',//ex: when user
        EXPECTED: selects fontwell race then LocationEvent : '12:16 fontwell' . Example values
        EXPECTED: are {'kempton','chepstow',..}
        EXPECTED: component.EventDetails: 'welcome to my stable overlay',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_horse_racing_uk_irish_races_edp()
        self.close_stream_and_bet_overlay_and_get_event_data()

        expected_response = {
            'component.ActionEvent': 'load',
            'component.CategoryEvent': self.event_data['categoryName'].lower(),
            'component.ContentPosition': 'not applicable',
            'component.EventDetails': 'welcome to my stable overlay',
            'component.LabelEvent': 'my stable',
            'component.LocationEvent': self.event_data['name'],
            'component.PositionEvent': 'welcome to my stable overlay',
            'component.URLClicked': 'not applicable',
            'event': 'contentView'
        }
        actual_response = self.get_data_layer_specific_object(object_key='component.LabelEvent',
                                                              object_value='my stable')
        self.compare_json_response(actual_response, expected_response)

    def test_002_when_the_user_clicks_on_ok_thanks_button_in_the_my_stable_onboarding_tutorial_pop_up(self):
        """
        DESCRIPTION: When the user clicks on "Ok Thanks" button in the My Stable Onboarding tutorial pop up.
        EXPECTED: The action of clicking the "Ok Thanks" button should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'welcome to my stable overlay',
        EXPECTED: component.LocationEvent:'{selected race}',//ex: when user
        EXPECTED: selects fontwell race then LocationEvent : '12:16 fontwell' . Example values
        EXPECTED: are {'kempton','chepstow',..}
        EXPECTED: component.EventDetails: 'ok thanks',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.my_stable_onboarding_overlay.ok_thanks.click()
        expected_response = {
            "event": "Event.Tracking",
            'component.CategoryEvent': self.event_data['categoryName'].lower(),
            'component.LabelEvent': 'my stable',
            'component.ActionEvent': 'click',
            'component.PositionEvent': 'welcome to my stable overlay',
            'component.LocationEvent': self.event_data['name'],
            'component.EventDetails': 'ok thanks',
            'component.URLClicked': 'not applicable',
            'component.ContentPosition': 'not applicable'
        }
        actual_response = self.get_data_layer_specific_object(object_key='component.LabelEvent',
                                                              object_value='my stable')
        self.compare_json_response(actual_response, expected_response)

    def test_003_when_user_clicks_on_close_option_in_the_my_stable_onboarding_tutorial_pop_up(self):
        """
        DESCRIPTION: When User clicks on "Close" option in the My Stable Onboarding tutorial pop up.
        EXPECTED: The action of clicking the "Close" button should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'close',
        EXPECTED: component.PositionEvent: 'welcome to my stable overlay',
        EXPECTED: component.LocationEvent:'{selected race}',//ex: when user
        EXPECTED: selects fontwell race then LocationEvent : '12:16 fontwell' . Example values
        EXPECTED: are {'kempton','chepstow',..}
        EXPECTED: component.EventDetails: 'welcome to my stable overlay',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.delete_cookies()
        self.navigate_to_page('/')
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_horse_racing_uk_irish_races_edp()
        self.close_stream_and_bet_overlay_and_get_event_data()
        self.site.my_stable_onboarding_overlay.close_button.click()
        expected_response = {
            "event": "Event.Tracking",
            'component.CategoryEvent': self.event_data['categoryName'].lower(),
            'component.LabelEvent': 'my stable',
            'component.ActionEvent': 'close',
            'component.PositionEvent': 'welcome to my stable overlay',
            'component.LocationEvent': self.event_data['name'],
            'component.EventDetails': 'welcome to my stable overlay',
            'component.URLClicked': 'not applicable',
            'component.ContentPosition': 'not applicable'
        }
        actual_response = self.get_data_layer_specific_object(object_key='component.LabelEvent',
                                                              object_value='my stable')
        self.compare_json_response(actual_response, expected_response)
