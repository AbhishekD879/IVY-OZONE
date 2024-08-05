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
class Test_C3019573_Verify_Navigation_to_Competition_Page_through_See_all_link_on_Tier_2_Sport_Landing_page(Common):
    """
    TR_ID: C3019573
    NAME: Verify Navigation to Competition Page through 'See all' link on Tier 2 Sport Landing page
    DESCRIPTION: This test case verifies navigation from Matches tab of sport landing page to Competitions page when user clicks on 'SEE ALL (#)' link in the type header within the section with upcoming events.
    DESCRIPTION: The list of sports that are tier I/II/III is available here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    PRECONDITIONS: 1) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value '00:00 AM Current Date' + 23H:55M
    PRECONDITIONS: 2) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value '00:00 AM Current Date' + 47H:55M
    PRECONDITIONS: 3) All aforementioned events should be created under the same league (type)
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: Upcoming events are available for the chosen TIER_2_SPORT
    """
    keep_browser_open = True

    def test_001_click_on_the_chosen_tier_2_sport_icon_in_menu_ribbon(self):
        """
        DESCRIPTION: Click on the chosen TIER_2_SPORT icon in menu ribbon
        EXPECTED: Sport landing page loads
        """
        pass

    def test_002_click_on_a_see_all_link_for_the_league_within_the_leagues_section_with_upcoming_events(self):
        """
        DESCRIPTION: Click on a 'SEE ALL' link for the League within the League(s) section with upcoming events
        EXPECTED: User is redirected to a Competitions page with a content related to a clicked league:
        EXPECTED: https://#ENVIRONMENT/competitions/#TIER_2_SPORT/#TIER_2_SPORT/#LEAGUE_NAME
        EXPECTED: 'Matches' tab loads by default
        EXPECTED: Tab should contain only upcoming events, divided into lists with Event card(s) header with league date (i.e. Today/Tomorrow/##_Month) and selection names (i.e. home/draw/away)
        """
        pass
