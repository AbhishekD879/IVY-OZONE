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
class Test_C44870374_Golf_scoreboard(Common):
    """
    TR_ID: C44870374
    NAME: Golf scoreboard
    DESCRIPTION: Check Golf scoreboard on Homepage (Highlights, In-Play, Live Stream Tabs), Golf landing page (Events, In-Play, Competitions), My Bets (Open Bets, Settled bets)
    DESCRIPTION: Check scoreboard in EDP (the scoreboard displays correct, complete data related to event, push, visualization and navigation)
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    PRECONDITIONS: There are events in In Play
    """
    keep_browser_open = True

    def test_001_verify_golf_scoreboard_on_home_pagehomepage___highlights__verify_that_each_golf_event_displays_the_right_scoreboard_configured_design_aligned_font_etc_as_per_specific_of_respective_sport__verify_that_each_scoreboard_is_updated_by_push_with_all_the_details_score_ball_animation_if_the_case_as_per_specific_of_respective_sporthomepage___in_play__verify_that_each_golf_event_displays_the_right_scoreboard_configured_design_aligned_font_etc_as_per_specific_of_respective_sport__verify_that_each_scoreboard_is_updated_by_push_with_all_the_details_score_ball_animation_if_the_case_as_per_specific_of_respective_sporthomepage___live_stream__verify_that_each_golf_event_displays_the_right_scoreboard_configured_design_aligned_font_etc_as_per_specific_of_respective_sport__verify_that_each_scoreboard_is_updated_by_push_with_all_the_details_time_score_ball_animation_if_the_case_as_per_specific_of_respective_sport(self):
        """
        DESCRIPTION: Verify Golf scoreboard on Home page:
        DESCRIPTION: Homepage - Highlights
        DESCRIPTION: - Verify that each Golf event displays the right Scoreboard, configured (design, aligned, font, etc) as per specific of respective sport
        DESCRIPTION: - Verify that each Scoreboard is updated by push with all the details (score, ball, animation if the case), as per specific of respective sport
        DESCRIPTION: Homepage - In-play
        DESCRIPTION: - Verify that each Golf event displays the right Scoreboard, configured (design, aligned, font, etc) as per specific of respective sport
        DESCRIPTION: - Verify that each Scoreboard is updated by push with all the details (score, ball, animation if the case), as per specific of respective sport
        DESCRIPTION: Homepage - Live Stream
        DESCRIPTION: - Verify that each Golf event displays the right Scoreboard, configured (design, aligned, font, etc) as per specific of respective sport
        DESCRIPTION: - Verify that each Scoreboard is updated by push with all the details (time, score, ball, animation if the case), as per specific of respective sport
        EXPECTED: Scoreboard is displayed as per GDs and is updated by push as per Golf specific
        """
        pass

    def test_002_verify_for_golf_all_the_landing_pages_events_in_play_competitions__verify_that_each_event_displays_the_right_scoreboard_configured_as_per_sport_specificdesign_aligned_font_etc__verify_that_each_scoreboard_is_updated_by_push_with_all_the_details_time_score_ball_animation_if_the_case_etc(self):
        """
        DESCRIPTION: Verify for Golf all the landing pages (Events, In-Play, Competitions):
        DESCRIPTION: - Verify that each event displays the right Scoreboard, configured as per sport specific(design, aligned, font, etc)
        DESCRIPTION: - Verify that each Scoreboard is updated by push with all the details (time, score, ball, animation if the case, etc)
        EXPECTED: Scoreboard is displayed as per GDs and is updated by push as per Golf specific
        """
        pass

    def test_003_verify_edp_for_golf_events__verify_that_the_right_scoreboard_is_displayed_and_is_configured_as_per_gds_design_aligned_font_etc__verify_that_the_scoreboard_is_updated_by_push_with_all_the_details_time_score_ball_animation_if_the_case_complete_data_related_to_event_visualization_navigation_etc(self):
        """
        DESCRIPTION: Verify EDP for Golf events:
        DESCRIPTION: - Verify that the right scoreboard is displayed, and is configured as per GD's (design, aligned, font, etc)
        DESCRIPTION: - Verify that the Scoreboard is updated by push with all the details (time, score, ball, animation if the case, complete data related to event, visualization, navigation, etc)
        EXPECTED: Scoreboard is displayed as per GDs and is updated by push as per Golf specific
        """
        pass
