import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2072604_Tracking_of_Opta_Football_Scoreboards_Pre_Match(Common):
    """
    TR_ID: C2072604
    NAME: Tracking of Opta Football Scoreboards  (Pre-Match)
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Football Pre-Match Opta Scoreboards data
    PRECONDITIONS: Note: All data layer content is provided by third party team (Opta Scoreboard team)
    PRECONDITIONS: 1. Opta scoreboard is mapped to the football event
    PRECONDITIONS: 2. User is logged in the app
    """
    keep_browser_open = True

    def test_001_open_pre_match_football_event_with_mapped_pre_match_opta_scoreboard(self):
        """
        DESCRIPTION: Open pre-match Football event with mapped Pre-Match Opta Scoreboard
        EXPECTED: - EDP is opened;
        EXPECTED: - Opta Scoreboards pre-match is shown;
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'pre-match',
        EXPECTED: 'eventLabel' : 'display',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>'
        EXPECTED: });
        """
        pass

    def test_003_click_on_the_lineups_icon_in_the_footer(self):
        """
        DESCRIPTION: Click on the 'Lineups' icon in the footer
        EXPECTED: 'Line Ups' overlay is opened and Line-ups data is shown
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'pre-match',
        EXPECTED: 'eventLabel' : 'team lineup',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>'
        EXPECTED: });
        """
        pass

    def test_005_click_on_the_standings_icon_to_view_league_table(self):
        """
        DESCRIPTION: Click on the 'Standings' icon to view league table
        EXPECTED: 'Latest Form/Head To Head/Standings' overlay is opened
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'pre-match',
        EXPECTED: 'eventLabel' : 'league table',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>'
        EXPECTED: });
        """
        pass

    def test_007_scroll_to_the_second_page_of_pre_match_opta_scoreboard_and_click_on_the_top_goal_scorers_chevron__more_stats_button_in_the_footer(self):
        """
        DESCRIPTION: Scroll to the second page of Pre-Match Opta Scoreboard and click on the 'Top Goal Scorers' chevron / 'More Stats' button in the footer
        EXPECTED: 'Player Stats' overlay is shown
        """
        pass

    def test_008_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'pre-match',
        EXPECTED: 'eventLabel' : 'player stats',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>',
        EXPECTED: });
        """
        pass

    def test_009_scroll_to_the_third_page_of_the_pre_match_opta_scoreboard_and_click_on_the_total_overunder_goals_chevron__more_stats_button_in_the_footer(self):
        """
        DESCRIPTION: Scroll to the third page of the Pre-Match Opta Scoreboard and click on the 'Total Over/Under Goals' chevron / 'More Stats' button in the footer
        EXPECTED: 'Team Stats' overlay is shown
        """
        pass

    def test_010_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'pre-match',
        EXPECTED: 'eventLabel' : 'team stats',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>',
        EXPECTED: });
        """
        pass
