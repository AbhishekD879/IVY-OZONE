import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870335_Verify_push_updates_for_the_Pre_Play_events_over_the_site_app(Common):
    """
    TR_ID: C44870335
    NAME: Verify push updates for the Pre-Play events over the site/app
    DESCRIPTION: Verify push updates in the Pre-play modules, EDP and anywhere on site/app where they are reflected.
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    PRECONDITIONS: There are events in Pre-Play
    """
    keep_browser_open = True

    def test_001_user_navigates_to_home_page_highlights_tabverify_that_in_highlights_for_events_in_pre_play_section_pushes_work_fine__date_and_time_is_displayed_and_events_drop_down_when_event_starts__verify_that_in_upcoming_odds_values_are_updated_by_push_for_price_increase_green_font_decrease_font_red_suspended_greyed_out_na__number_of_pre_play_events_update_correctly_after_all_pre_play_events_drop_of_the_header_drops_off__the_pushes_work_in_highlights_carousel_and_surface_bet_section_with_respect_of_the_each_sport_characteristics_mentioned_above__if_the_hrgh_section_is_available_in_highlights_pushes_must_be_checked_similar_as_in_next_races_and_the_2nd_case_steps_described_below_to_be_followed(self):
        """
        DESCRIPTION: User navigates to Home page, Highlights Tab:
        DESCRIPTION: Verify that in Highlights, for events in Pre-Play section pushes work fine:
        DESCRIPTION: - Date and time is displayed and events drop down when event starts
        DESCRIPTION: - Verify that in upcoming odds values are updated by push for price increase (green font) decrease (font red), suspended (Greyed Out), NA
        DESCRIPTION: - number of Pre-Play events update correctly, after all Pre-Play events drop of, the header drops off
        DESCRIPTION: - the pushes work in Highlights Carousel and Surface Bet section with respect of the each sport characteristics mentioned above.
        DESCRIPTION: - If the HR/GH section is available in Highlights pushes must be checked similar as in Next Races, and the 2nd case steps described below to be followed
        EXPECTED: Pushes work fine in Home page, Highlights Tab
        """
        pass

    def test_002_user_navigates_to_home_page_next_races_tabverify_that_in_next_races_pushes_work_fine__the_right_number_of_events_are_displayed_as_per_settings__they_are_coming_on_frontend_synchronized_in_time_and_by_the_timing_order_showing_start_time_suspending_and_dropping_off_on_event_start__selection_are_updated_by_push_prices_suspension_na_the_previous_prices(self):
        """
        DESCRIPTION: User navigates to Home page, Next Races Tab:
        DESCRIPTION: Verify that in Next Races pushes work fine:
        DESCRIPTION: - the right number of events are displayed as per settings
        DESCRIPTION: - they are coming on frontend, synchronized in time and by the timing order, showing start time, suspending and dropping off on event start
        DESCRIPTION: - selection are updated by push (prices, suspension, NA, the previous prices),
        EXPECTED: In Next Races tab the Pushes works fine for HR events.
        """
        pass

    def test_003_user_navigates_to_football_landing_page_matches_tabverify_that_in_matches_page__events_are_displayed_as_in_pre_play_drop_off_as_per_timedate_displayed_when_respective_event_startspushes_works_fine_for_every_event__selections_are_live_updated_as_price_suspension_na__number_of_pre_play_events_is_correct_after_all_pre_play_events_drop_of_the_header_drops_off(self):
        """
        DESCRIPTION: User navigates to Football landing page, Matches Tab:
        DESCRIPTION: Verify that in Matches page
        DESCRIPTION: - events are displayed as in Pre-Play drop off as per time/date displayed when respective event starts
        DESCRIPTION: Pushes works fine for every event:
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - number of Pre-Play events is correct, after all Pre-Play events drop of, the header drops off
        EXPECTED: In Football landing page, Matches Tab, Pre-Play events are updated by push
        """
        pass
