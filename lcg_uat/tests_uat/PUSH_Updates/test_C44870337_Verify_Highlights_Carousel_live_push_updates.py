import pytest
from time import sleep
from datetime import datetime
from crlat_ob_client.utils.date_time import get_date_time_as_string
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
# @pytest.mark.prod - # Not allowed to create events / highlight carousels on prod
@pytest.mark.mobile_only  # Not applicable for desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.p1
@vtest
class Test_C44870337_Verify_Highlights_Carousel_live_push_updates(BaseHighlightsCarouselTest):
    """
    TR_ID: C44870337
    NAME: Verify Highlights Carousel live push updates
    DESCRIPTION: Verify Highlights Carousel live push updates
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    PRECONDITIONS: There are events in In-Play
    PRECONDITIONS: Highlights Carousel is enabled and populated with In-Play events.
    """
    keep_browser_open = True
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    increased_price = '3/1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Creating events and adding them to highlights carousel"
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.event_id = event.event_id
        self.__class__.selection_ids = event.selection_ids
        self.__class__.selection = event.team1
        self.__class__.event_name = f'{self.selection} v {event.team2}'
        event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.event_id2 = event2.event_id
        self.__class__.event_name2 = f'{event2.team1} v {event2.team2}'
        now = datetime.now()
        date_from = get_date_time_as_string(date_time_obj=now, time_format=self.time_format,
                                            url_encode=False, days=-1)[:-3] + 'Z'
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                   events=[self.event_id, self.event_id2], inplay=True,
                                                   date_from=date_from)
        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])

    def test_001_user_navigates_to_home_page_highlights_tab_and_check_the_highlights_carousel_non_race_eventsverify_that_in_highlights_carousel_for_any_ongoing_events_pushes_work_fine__selections_are_live_updated_as_price_suspension__event_shows_live_when_event_starts_respectively_drop_off_when_event_ends__timing_and_data_related_to_matches_ht_quarter_innings_etc_should_be_displayed_as_per_sport_specific__number_of_events_is_as_per_settings_after_all_in_play_events_drop_of_the_carousel_drop_off(self):
        """
        DESCRIPTION: User navigates to Home page, Highlights Tab and check the Highlights Carousel non-race events:
        DESCRIPTION: Verify that in Highlights Carousel, for any ongoing events pushes work fine:
        DESCRIPTION: - selections are live updated as price, suspension,
        DESCRIPTION: - event shows live when event starts respectively drop off when event ends.
        DESCRIPTION: - timing and data related to matches (HT, Quarter, Innings, etc) should be displayed as per sport specific
        DESCRIPTION: - number of events is as per settings, after all In-Play events drop of, the Carousel drop off
        EXPECTED: In Highlights Carousel, for any ongoing events (non-racing) pushes work fine
        """
        #  timing and data related to matches (HT, Quarter, Innings, etc) - Not in automation scope
        self.site.wait_content_state('HOMEPAGE')
        self.device.driver.delete_all_cookies()
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertTrue(highlight_carousels,
                        msg='No highlight carousels found')
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named "{self.highlights_carousel_name}"')
        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name}"')
        self.assertIn(self.event_name, highlight_carousel_events,
                      msg=f'Event "{self.event_name}" is not displayed in Carousel "{self.highlights_carousel_name}"')
        self.assertIn(self.event_name2, highlight_carousel_events,
                      msg=f'Event "{self.event_name2}" is not displayed in Carousel "{self.highlights_carousel_name}"')
        event = highlight_carousel_events[self.event_name]
        event1 = event.items_as_ordered_dict
        self.assertTrue(event.is_live_now_event, msg='event is not live')
        selection_name, selection_button = list(event1.items())[0]
        self.assertTrue(selection_button.is_displayed(), msg='Failed to display 1st team Bet button')
        #  TODO: raised bug for ladbrokes for price updation issue
        #  TODO BMA-55571
        if self.brand == 'ladbrokes':
            self.ob_config.change_price(selection_id=self.selection_ids[self.selection], price=self.increased_price)
            self.device.refresh_page()
        else:
            self.ob_config.change_price(selection_id=self.selection_ids[self.selection], price=self.increased_price)
            result = self.wait_for_price_update_from_featured_ms(event_id=self.event_id,
                                                                 selection_id=self.selection_ids[self.selection],
                                                                 timeout=60, price=self.increased_price)
            self.assertTrue(result,
                            msg=f'Price updates are not received for event "{self.event_name}", event id "{self.event_id}"')
            self.assertTrue(selection_button.is_price_changed(expected_price=self.increased_price, timeout=20),
                            msg=f'Price for Bet Button for selection "{self.selection}" did not change. '
                                f'Actual price: "{selection_button.name}", Expected price: "{self.increased_price}"')
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.selection], displayed=True,
                                              active=False)
        sleep(3)
        self.device.refresh_page()
        self.assertFalse(selection_button.is_enabled(expected_result=False, timeout=5), msg=f'{selection_name} is not suspended')
        self.ob_config.change_event_state(self.event_id, displayed=False, active=False)
        sleep(5)  # For the changed event state to reflect on highlight carousel
        self.device.refresh_page()
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named "{self.highlights_carousel_name}"')
        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name}"')
        self.assertNotIn(self.event_name, highlight_carousel_events,
                         msg=f'Event "{self.event_name}" is displayed in Carousel "{self.highlights_carousel_name}"')
        self.ob_config.change_event_state(self.event_id2, displayed=False, active=False)
        sleep(5)  # For the changed event state to reflect on highlight carousel
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name, expected_result=False, timeout=5,
                                           poll_interval=1)
