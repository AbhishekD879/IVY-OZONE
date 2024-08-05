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
class Test_C44870326_Verify_User_sees_Live_score_updates_for_all_the_inplay_events_on_the_sports_pages(Common):
    """
    TR_ID: C44870326
    NAME: "Verify User sees Live score updates for all the inplay events on the sports pages
    DESCRIPTION: "Verify User sees Live score updates for all the inplay events on the sports pages
    DESCRIPTION: Verify user is able to click all the selections ,odds and navigational links of the event card on Sports Homepage( Pre-Match and In-Play events)
    DESCRIPTION: Verify user can  perform same actions on Competition and outrights section
    DESCRIPTION: Verify user is seen Scores on event listing pages"
    PRECONDITIONS: UserName: goldenbuild1   Password:  password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_click_on_in_play_tab_and_go_to_football(self):
        """
        DESCRIPTION: Click on In-Play tab and go to Football
        EXPECTED: In-Play tab opened with all inplay sports
        """
        pass

    def test_003_go_to_football_landing_page_and_verify_user_sees_live_score_updates_on_football__inplay_tab_and_landing_page(self):
        """
        DESCRIPTION: Go to Football landing page and Verify User sees Live score updates on football  Inplay tab and landing page
        EXPECTED: Live scores updates are displayed on both inplay tab and sports pages
        """
        pass

    def test_004_verify_user_is_able_to_click_all_the_selections_odds_and_navigational_links_of_the_event_card_on_sports_homepage_pre_match_and_in_play_events(self):
        """
        DESCRIPTION: Verify user is able to click all the selections ,odds and navigational links of the event card on Sports Homepage( Pre-Match and In-Play events)
        EXPECTED: Selections, odds and links are clickable
        """
        pass

    def test_005_verify_user_can__perform_same_above_actions_on_competition_and_outrights_section(self):
        """
        DESCRIPTION: Verify user can  perform same above actions on Competition and outrights section
        EXPECTED: Selections, odds and links are clickable
        """
        pass

    def test_006_repeat_step_2_to_5_for_all_sportseg_tennis_with_serverhandballbasketballbadmintonvolleyballbeach_volleyballbasketball(self):
        """
        DESCRIPTION: Repeat step #2 to #5 for all sports
        DESCRIPTION: eg: (Tennis (With server),Handball,Basketball
        DESCRIPTION: Badminton,Volleyball,Beach Volleyball,Basketball)
        EXPECTED: 
        """
        pass
