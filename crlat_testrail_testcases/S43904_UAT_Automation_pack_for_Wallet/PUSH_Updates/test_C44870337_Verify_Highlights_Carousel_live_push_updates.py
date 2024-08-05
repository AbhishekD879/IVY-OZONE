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
class Test_C44870337_Verify_Highlights_Carousel_live_push_updates(Common):
    """
    TR_ID: C44870337
    NAME: Verify Highlights Carousel live push updates
    DESCRIPTION: Verify Highlights Carousel live push updates
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    PRECONDITIONS: There are events in In-Play
    PRECONDITIONS: Highlights Carousel is enabled and populated with In-Play events.
    """
    keep_browser_open = True

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
        pass
