import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870334_Verify_push_updates_for_the_In_Play_events_over_the_site_app(Common):
    """
    TR_ID: C44870334
    NAME: Verify push updates for the In-Play events over the site/app
    DESCRIPTION: Verify push updates in the in-play modules, EDP and anywhere on site/app where they are reflected.
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    PRECONDITIONS: There are events in In Play
    """
    keep_browser_open = True

    def test_001_user_navigates_to_home_page_highlights_tabverify_that_in_highlights_for_any_ongoing_events_in_in_play_section_pushes_work_fine__scoreboard_is_updated__selections_are_live_updated_as_price_suspension_na__events_appear_respectively_drop_down_when_event_starts_or_finish__timing_and_data_related_to_matches_ht_quarter_innings_etc_should_be_displayed_as_per_sport_specific__verify_that_any_event_going_live_drop_off_from_upcoming_section_and_shows_on_in_play_section_in_the_right_time_displaying_live_features__number_of_in_play_events_is_correct_after_all_in_play_events_drop_of_the_header_drops_off__the_pushes_work_in_highlights_carousel_and_surface_bet_section_with_respect_of_the_each_sport_characteristics_mentioned_above__if_the_hrgh_section_is_available_in_highlights_pushes_must_be_checked__the_right_number_of_events_displayed_as_per_settings__they_are_coming_on_frontend_synchronized_in_time_and_by_the_timing_order_showing_start_time_suspending_and_dropping_off_on_event_start__selection_are_updated_by_push_prices_suspension_na_the_previous_prices(self):
        """
        DESCRIPTION: User navigates to Home page, Highlights Tab:
        DESCRIPTION: Verify that in Highlights, for any ongoing events in In-Play section pushes work fine:
        DESCRIPTION: - scoreboard is updated,
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - events appear respectively drop down when event starts or finish
        DESCRIPTION: - timing and data related to matches (HT, Quarter, Innings, etc) should be displayed as per sport specific
        DESCRIPTION: - verify that any event going live drop off from Upcoming section and shows on In-Play section in the right time, displaying live features.
        DESCRIPTION: - number of In-Play events is correct, after all In-Play events drop of, the header drops off
        DESCRIPTION: - the pushes work in Highlights Carousel and Surface Bet section with respect of the each sport characteristics mentioned above.
        DESCRIPTION: - If the HR/GH section is available in Highlights pushes must be checked:
        DESCRIPTION: (- the right number of events displayed as per settings)
        DESCRIPTION: (- they are coming on frontend, synchronized, in time and by the timing order, showing start time, suspending and dropping off on event start)
        DESCRIPTION: (- selection are updated by push (prices, suspension, NA, the previous prices)
        EXPECTED: in Highlights, for any ongoing events in In-Play section pushes work fine
        """
        pass

    def test_002_user_navigates_to_home_page_in_play_tabverify_that_in_inplay_page_the_pushes_works_fine_for_every_sport_category__scoreboard_is_updated__selections_are_live_updated_as_price_suspension_na__events_appear_respectively_drop_down_when_event_starts_or_finish__timing_and_data_related_to_matches_ht_quarter_innings_etc_should_be_displayed_as_per_sport_specific__number_of_in_play_events_is_correct_after_all_in_play_events_drop_of_the_header_drops_off(self):
        """
        DESCRIPTION: User navigates to Home page, In-Play Tab:
        DESCRIPTION: Verify that in Inplay page the Pushes works fine for every sport (category):
        DESCRIPTION: - scoreboard is updated,
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - events appear respectively drop down when event starts or finish
        DESCRIPTION: - timing and data related to matches (HT, Quarter, Innings, etc) should be displayed as per sport specific
        DESCRIPTION: - number of In-Play events is correct, after all In-Play events drop of, the header drops off
        EXPECTED: In Inplay page the Pushes works fine for:
        EXPECTED: - Football
        EXPECTED: - Tennis
        EXPECTED: - Basketball
        EXPECTED: - Cricket
        EXPECTED: - Any other In Play sport events
        """
        pass

    def test_003_user_navigates_to_home_page_next_races_tabverify_that_in_next_races_pushes_work_fine__the_right_number_of_events_are_displayed_as_per_settings__they_are_coming_on_frontend_synchronized_in_time_and_by_the_timing_order_showing_start_time_suspending_and_dropping_off_on_event_start__selection_are_updated_by_push_prices_suspension_na_the_previous_prices(self):
        """
        DESCRIPTION: User navigates to Home page, Next Races Tab:
        DESCRIPTION: Verify that in Next Races pushes work fine:
        DESCRIPTION: - the right number of events are displayed as per settings
        DESCRIPTION: - they are coming on frontend, synchronized in time and by the timing order, showing start time, suspending and dropping off on event start
        DESCRIPTION: - selection are updated by push (prices, suspension, NA, the previous prices),
        EXPECTED: In Next Reaces tab the Pushes works fine for HR events.
        """
        pass

    def test_004_user_navigates_to_home_page_live_stream_tabverify_that_in_live_stream_tab_there_are_two_tabs_live_now_and_upcoming__only_the_events_that_have_live_stream_are_displayed__the_events_are_displayed_in_the_right_tab_in_play_and_upcoming_drop_off_and_display_happens_synchronized_in_time_in_each_tabpushes_works_fine_for_every_sport_category__scoreboard_is_updated__selections_are_live_updated_as_price_suspension_na__timing_and_data_related_to_matches_ht_quarter_innings_etc_should_be_displayed_as_per_sport_specific(self):
        """
        DESCRIPTION: User navigates to Home page, Live Stream Tab:
        DESCRIPTION: Verify that in Live Stream Tab there are two tabs, Live now and Upcoming
        DESCRIPTION: - only the events that have Live stream are displayed
        DESCRIPTION: - the events are displayed in the right tab (in-play and upcoming), drop off and display happens synchronized in time (in each tab)
        DESCRIPTION: Pushes works fine for every sport (category):
        DESCRIPTION: - scoreboard is updated,
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - timing and data related to matches (HT, Quarter, Innings, etc) should be displayed as per sport specific
        EXPECTED: In Live Stream Page, the Pushes works fine for every event.
        """
        pass

    def test_005_user_navigates_to_football_landing_page_matches_tabverify_that_in_matches_page__events_are_displayed_as_in_play_at_the_right_time_and_drop_off_when_endingpushes_works_fine_for_every_event__scoreboard_is_updated__selections_are_live_updated_as_price_suspension_na__events_appear_respectively_drop_down_when_event_starts_or_finish__timing_and_data_status_related_to_matches_ht_timing_etc_to_be_displayed__number_of_in_play_events_is_correct_after_all_in_play_events_drop_of_the_header_drops_off(self):
        """
        DESCRIPTION: User navigates to Football landing page, Matches Tab:
        DESCRIPTION: Verify that in Matches page
        DESCRIPTION: - events are displayed as in Play at the right time and drop off when ending
        DESCRIPTION: Pushes works fine for every event:
        DESCRIPTION: - scoreboard is updated,
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - events appear respectively drop down when event starts or finish
        DESCRIPTION: - timing and data status related to matches (HT, timing, etc) to be displayed
        DESCRIPTION: - number of In-Play events is correct, after all In-Play events drop of, the header drops off
        EXPECTED: In Football landing page, Matches tab, Pushes must work fine
        """
        pass

    def test_006_user_is_in_football_landing_pagenavigate_to_in_play_tab_and_verify_that_pushes_work_fine___there_are_two_sections_live_now_and_upcoming_each_event_is_displayed_as_per_status_in_each_section__the_events_from_upcoming_drop_off_and_shows_on_in_play_section_at_the_right_time_and_the_events_that_end_drop_offpushes_works_fine_for_every_event__scoreboard_is_updatedthe_right_market_with_the_respective_header_is_displayed__selections_are_live_updated_as_price_suspension_na__timing_and_data_related_to_matches_ht_should_be_displayed(self):
        """
        DESCRIPTION: User is in Football landing page.
        DESCRIPTION: Navigate to In-Play tab and verify that Pushes work fine :
        DESCRIPTION: - there are two sections, Live now and Upcoming, each event is displayed as per status in each section
        DESCRIPTION: - the events from upcoming drop off and shows on In-Play section at the right time, and the events that end drop off.
        DESCRIPTION: Pushes works fine for every event:
        DESCRIPTION: - scoreboard is updated,
        DESCRIPTION: the right market with the respective header is displayed
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - timing and data related to matches (HT) should be displayed
        EXPECTED: In Football landing page, In-Play tab, Pushes must work fine
        """
        pass

    def test_007_user_is_in_football___accas_navigate_to_coupons_and_verify_that_pushes_work_fine___today_coupons_which_are_ended_drop_off__selections_are_live_updated_as_price_suspension_na__verify_market_selector(self):
        """
        DESCRIPTION: User is in Football - Accas, navigate to Coupons and verify that Pushes work fine :
        DESCRIPTION: - Today Coupons which are ended drop off
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - verify market selector
        EXPECTED: n Football - Accas - Coupons detail page, Pushes work fine :
        """
        pass

    def test_008_user_is_in_football_landing_page_navigate_to_edp_of_an_in_play_event_and_verify_that_pushes_work_fine___scoreboard_is_updated_with_all_the_details_scores_timing_status_etc__all_the_markets_appearing_and_dropping_off_as_specific__selections_are_live_updated_as_price_suspension_na(self):
        """
        DESCRIPTION: User is in Football landing page, navigate to EDP of an In Play event and verify that Pushes work fine :
        DESCRIPTION: - scoreboard is updated with all the details (scores, timing, status, etc.)
        DESCRIPTION: - all the markets appearing and dropping off as specific
        DESCRIPTION: - selections are live updated as price, suspension, NA
        EXPECTED: In Football ED Pages Pushes work fine
        """
        pass

    def test_009_user_navigates_to_tennis_landing_pagenavigate_to_in_play_tab_and_verify_that_pushes_work_fine___there_are_two_sections_live_now_and_upcoming_each_event_is_displayed_as_per_status_in_each_section__the_events_from_upcoming_drop_off_and_shows_on_in_play_section_at_the_right_time_and_the_events_that_end_drop_offpushes_works_fine_for_every_event__scoreboard_is_updated_the_ball_is_indicated_correct_playerteamthe_right_market_with_the_respective_header_is_displayed__selections_are_live_updated_as_price_suspension_na__timing_and_data_related_to_matches_set_number_should_be_displayed(self):
        """
        DESCRIPTION: User navigates to Tennis landing page.
        DESCRIPTION: Navigate to In-Play tab and verify that Pushes work fine :
        DESCRIPTION: - there are two sections, Live now and Upcoming, each event is displayed as per status in each section
        DESCRIPTION: - the events from upcoming drop off and shows on In-Play section at the right time, and the events that end drop off.
        DESCRIPTION: Pushes works fine for every event:
        DESCRIPTION: - scoreboard is updated, the ball is indicated correct player/team
        DESCRIPTION: the right market with the respective header is displayed
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - timing and data related to matches (Set Number) should be displayed
        EXPECTED: In Tennis landing page, In-Play tab, Pushes must work fine
        """
        pass

    def test_010_in_tennis_landing_page_user_navigates_to_matches_pageverify_that_pushes_work_fine_for_all_the_in_play_events__events_are_displayed_as_in_play_at_the_right_tile_and_drop_off_when_endingpushes_works_fine_for_every_event__scoreboard_is_updated_the_ball_is_indicated_correct_playerteamthe_right_market_with_the_respective_header_is_displayed__selections_are_live_updated_as_price_suspension_na__timing_and_data_related_to_matches_set_number_should_be_displayed(self):
        """
        DESCRIPTION: In Tennis landing page user navigates to Matches page
        DESCRIPTION: Verify that Pushes work fine for all the In Play events:
        DESCRIPTION: - events are displayed as in Play at the right tile and drop off when ending
        DESCRIPTION: Pushes works fine for every event:
        DESCRIPTION: - scoreboard is updated, the ball is indicated correct player/team
        DESCRIPTION: the right market with the respective header is displayed
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: - timing and data related to matches (Set Number) should be displayed
        EXPECTED: In Tennis landing page, Matches tab, Pushes must work fine
        """
        pass

    def test_011_in_tennis_landing_page_user_navigates_to_an_event_detail_pageverify_pushes__scoreboard_must_be_updated_all_data__including_time_scores_ball_keeper_etc__selections_are_live_updated_as_price_suspension_na_for_all_markets__all_the_markets_appearing_and_dropping_off_as_specific_in_any_market_collection(self):
        """
        DESCRIPTION: In Tennis landing page user navigates to an Event Detail Page
        DESCRIPTION: Verify Pushes
        DESCRIPTION: - Scoreboard must be updated (all data  including time, scores, ball keeper, etc)
        DESCRIPTION: - selections are live updated as price, suspension, NA for all markets
        DESCRIPTION: - all the markets appearing and dropping off as specific in any Market collection
        EXPECTED: In any EDP Tennis, Pushes must work fine
        """
        pass

    def test_012_navigate_to_each_sport_landing_page_that_have_in_play_events_and_verify_that_pushes_work_fine_considering_the_specificity_of_each_sport_asketball_cricket_golf_rugby_etc__each_event_is_displayed_as_per_status_in_in_play_section__the_events_from_upcoming_drop_off_and_shows_on_in_play_section_at_the_right_time_and_the_events_that_end_drop_off__scoreboard_is_updated_timing_and_data_related_to_match_status_is_displayed__selections_are_live_updated_as_price_suspension_nanavigate_to_an_edp_and_check_that__scoreboard_is_updated_all_data__including_time_scores_etc__selections_are_live_updated_as_price_suspension_na_for_all_markets__all_the_markets_appearing_and_dropping_off_as_specific_in_any_market_collection(self):
        """
        DESCRIPTION: Navigate to each Sport Landing page that have In Play events and verify that Pushes work fine considering the specificity of each sport (asketball, Cricket, Golf, Rugby, etc.):
        DESCRIPTION: - each event is displayed as per status in In-Play section,
        DESCRIPTION: - the events from upcoming drop off and shows on In-Play section at the right time, and the events that end drop off.
        DESCRIPTION: - scoreboard is updated, timing and data related to match status is displayed
        DESCRIPTION: - selections are live updated as price, suspension, NA
        DESCRIPTION: Navigate to an EDP and check that:
        DESCRIPTION: - Scoreboard is updated (all data  including time, scores, etc)
        DESCRIPTION: - selections are live updated as price, suspension, NA for all markets
        DESCRIPTION: - all the markets appearing and dropping off as specific in any Market collection
        EXPECTED: In any sport landing pages and EDP, Pushes must work fine
        """
        pass
