import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.my_stable
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C66037543_Verify_the_GA_tracking_for_various_actions_performed_on_the_Horse_racing_EDP_related_to_Stable(BaseDataLayerTest, BaseRacing):
    """
    TR_ID: C66037543
    NAME: Verify the GA tracking for various actions performed on the Horse racing  EDP  related to Stable.
    DESCRIPTION: This test case evaluates the various actions performed on the Horse racing EDP pages related to the My Stable functionality.
    DESCRIPTION: 1. When user clicks on My Stable.
    DESCRIPTION: 2. When user clicks on 'Edit Stable'.
    DESCRIPTION: 3. When user clicks on horse and interacted with notes.
    DESCRIPTION: 4. When user clicks on save stable.
    PRECONDITIONS: CMS configurations
    PRECONDITIONS: My Stable Menu item
    PRECONDITIONS: My Stable Configurations
    PRECONDITIONS: Checkbox against Active Mystable - Should be checked in
    PRECONDITIONS: Checkbox against Mystable Horses Running Today Carousel- Should be checked in
    PRECONDITIONS: Checkbox against Active Antepost - Should be checked in
    PRECONDITIONS: Checkbox against Active My Bets (Phase 2)
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
    PRECONDITIONS: Empty Stable Message Label - Tap on Edit Stable on the Race Card to add a horse
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
    keep_browser_open = True
    enable_bs_performance_log = True

    def verify_GA_tracking(self, EventDetails: str, LocationEvent: str, PositionEvent: str):
        expected_resp = {
            'event': "Event.Tracking",
            'component.ActionEvent': 'click',
            'component.CategoryEvent': 'horse racing',
            'component.ContentPosition': 'not applicable',
            'component.EventDetails': EventDetails,
            'component.LabelEvent': 'my stable',
            'component.LocationEvent': LocationEvent,
            'component.PositionEvent': PositionEvent,
            'component.URLClicked': 'not applicable'
        }
        actual_resp = self.get_data_layer_specific_object(object_key='event', object_value='Event.Tracking',timeout=20)
        self.compare_json_response(actual_resp, expected_resp)

    def test_000_preconditions(self):
        """
        DESCRIPTION: checking MY STABLE is enabled in CMS
        """
        my_stable = self.cms_config.get_my_stable_config().get('active')
        if not my_stable:
            raise SiteServeException('My stable Page is not active in CMS')

    def test_001_when_user_clicks_on_my_stable___entry_point_in_the_horse_racing_landing_page_or_event_details_page(self):
        """
        DESCRIPTION: When user clicks on My Stable - Entry point in the Horse racing landing page or event details page.
        EXPECTED: The action of clicking the My Stable entry point on the HR landing page or EDP page should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: '{event details page/horse racing}',
        EXPECTED: component.LocationEvent:'{selected race/not applicable}',//ex: when user
        EXPECTED: selects fontwell race then LocationEvent : 'fontwell' . Example values
        EXPECTED: are {'kempton','chepstow',..}
        EXPECTED: component.EventDetails: 'my stable',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.login()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        self.assertTrue(self.site.horse_racing.my_stable_link.is_displayed(), msg=f'My stable is not display in FE')
        self.site.horse_racing.my_stable_link.click()
        self.verify_GA_tracking(EventDetails='my stable',LocationEvent='not applicable',PositionEvent='horse racing')
        self.site.back_button.click()
        self.site.wait_content_state(state_name='HorseRacing')
        # clicking one UK & IRISH event
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(
            self.uk_and_ire_type_name)
        sections.scroll_to()
        expected_event = None
        expected_meeting_name = None
        meetings = sections.items_as_ordered_dict
        self.assertTrue(meetings, msg='No meetings found')
        for meeting_name, meeting in meetings.items():
            events = meeting.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found for meeting: "{meeting_name}"')
            for event_name, event in events.items():
                race_started = event.is_resulted or event.has_race_off()
                if not race_started:
                    expected_event = event
                    expected_meeting_name = meeting_name
                    break
            if expected_event is not None:
                break
        expected_event.click()
        self.site.wait_splash_to_hide()
        self.__class__.race_name = self.site.racing_event_details.tab_content.race_details.event_title
        actual_meeting_name = self.race_name.split(' ', 1)[1] if len(self.race_name.split(' ', 1)) > 1 else self.race_name
        self.assertIn(expected_meeting_name.lower(), actual_meeting_name.lower(),
                      msg=f'Actual meeting name "{actual_meeting_name}" '
                          f'is not same as expected meeting name "{expected_meeting_name}" ')
        self.site.racing_event_details.my_stable_link.click()
        # GA Tracking in Racing EDP page My stable
        self.verify_GA_tracking(EventDetails='my stable', LocationEvent=actual_meeting_name,PositionEvent='event details page')
        self.site.back_button.click()
        # self.site.wait_content_state(state_name='HorseRacing')

    def test_002_when_user_clicks_on_edit_stable_button_in_the_horse_racing_event_details_page(self):
        """
        DESCRIPTION: When user clicks on 'Edit Stable' button in the Horse racing event details page.
        EXPECTED: The user should be able to click the 'Edit Stable' button in the Horse Racing event details page.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'event details page',
        EXPECTED: component.LocationEvent:'{selected race - selected location}',//ex: when user
        EXPECTED: selects fontwell race under win or E/W then LocationEvent : '12:16 fontwell - win or E/W' .
        EXPECTED: component.EventDetails: 'edit stable',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        if self.device_type == 'mobile':
            if self.site.wait_for_my_stable_onboarding_overlay():
                self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.assertTrue(self.site.racing_event_details.edit_stable.is_displayed(),
                        msg=f'edit stable link is not display in FE ')
        self.site.racing_event_details.edit_stable.click()
        self.verify_GA_tracking(EventDetails='edit stable', LocationEvent=f'{self.race_name} - win or E/W', PositionEvent='event details page')

    def test_003_when_user_clicks_on_horse_and_interacted_with_notes_by_clicking_or_bookmarking_any_of_the_horses_in_the_edp_page(self):
        """
        DESCRIPTION: When user clicks on horse and interacted with notes by clicking or bookmarking any of the Horses in the EDP page.
        EXPECTED: The action of clicking the horse to bookmark and add notes in the EDP should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'notes',
        EXPECTED: component.LocationEvent:'{selected race - selected location}',//ex: when user
        EXPECTED: selects fontwell race under win or E/W then LocationEvent : '12:16 fontwell - win or E/W' .
        EXPECTED: component.EventDetails: '{selected horse-save|selected horse-close}',//ex:if user adds notes for selected horse
        EXPECTED: and clicks on save, then EventDetails is 'dazzling star-save'
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        # In phase 2 of MY STABLE, the PositionEvent: "no notes" value was changed.
        self.__class__.outcomes = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB).items_as_ordered_dict
        horse_name = str
        for outcome_name, outcome in self.outcomes.items():
            horse_name = outcome.horse_name
            outcome.my_stable_bookmark.click()
            outcome.my_stable_notes.cancel.click()
            break
        wait_for_haul(10)
        self.verify_GA_tracking(EventDetails=f'{horse_name} - close', PositionEvent='no notes',
                                LocationEvent=f'{self.race_name} - win or E/W')

    def test_004_when_user_clicks_on_save_stable_by_clicking_on_the_done_button_in_the_hr_edp_page(self):
        """
        DESCRIPTION: When user clicks on save stable by clicking on the 'Done' button in the HR EDP page.
        EXPECTED: When user clicks on the 'Done' button to save stable it should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'event details page',
        EXPECTED: component.LocationEvent:'{selected race - selected location}',//ex: when user
        EXPECTED: selects fontwell race under win or E/W then LocationEvent : '12:16 fontwell - win or E/W' .
        EXPECTED: component.EventDetails: 'save stable',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        second_horse_name = str
        for outcome_name, outcome in self.outcomes.items():
            second_horse_name = outcome.horse_name
            if not outcome.is_bookmark_filled:
                outcome.fill_bookmark(notes='MY NOTES')
                break
        wait_for_haul(10)
        self.verify_GA_tracking(EventDetails=f'{second_horse_name} - save', PositionEvent='notes',
                                    LocationEvent=f'{self.race_name} - win or E/W')
        self.site.racing_event_details.edit_stable.click()
        self.verify_GA_tracking(EventDetails='save stable',LocationEvent=f'{self.race_name} - win or E/W',PositionEvent='event details page')
