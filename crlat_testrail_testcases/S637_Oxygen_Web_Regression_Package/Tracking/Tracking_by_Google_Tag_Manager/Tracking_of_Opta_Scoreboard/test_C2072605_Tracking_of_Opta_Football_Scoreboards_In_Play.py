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
class Test_C2072605_Tracking_of_Opta_Football_Scoreboards_In_Play(Common):
    """
    TR_ID: C2072605
    NAME: Tracking of Opta Football Scoreboards (In-Play)
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Football In-Play Opta Scoreboards data
    PRECONDITIONS: Note: All data layer content is provided by third party team (Opta Scoreboard team)
    PRECONDITIONS: 1. Opta scoreboard visualization is mapped to the football event
    PRECONDITIONS: 2. User is logged in the app
    """
    keep_browser_open = True

    def test_001_open_football_in_play_event_with_mapped_pre_match_opta_scoreboard(self):
        """
        DESCRIPTION: Open Football In-Play event with mapped Pre-Match Opta Scoreboard
        EXPECTED: - EDP is opened;
        EXPECTED: - In-Play Opta Scoreboards is shown;
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'display',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>'
        EXPECTED: });
        """
        pass

    def test_003_click_on_the_season_stats_icon_in_the_footer(self):
        """
        DESCRIPTION: Click on the 'Season Stats' icon in the footer
        EXPECTED: 'Team Stats' overlay is opened
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'team stats',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>',
        EXPECTED: });
        """
        pass

    def test_005_click_on_the_lineups_icon_in_the_footer(self):
        """
        DESCRIPTION: Click on the 'Lineups' icon in the footer
        EXPECTED: - 'Line Ups' overlay is opened
        EXPECTED: - Line-ups data is shown
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'team lineup',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>'
        EXPECTED: });
        """
        pass

    def test_007_scroll_to_the_second_page_of_in_play_opta_scoreboard_and_click_on_total_shoots_chevron(self):
        """
        DESCRIPTION: Scroll to the second page of In-Play Opta Scoreboard and click on 'Total Shoots' chevron
        EXPECTED: 'Player Stats' overlay is opened
        """
        pass

    def test_008_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'scoreboard',
        EXPECTED: 'eventAction' : 'in play',
        EXPECTED: 'eventLabel' : 'player stats',
        EXPECTED: 'eventID' : '<< EVENT ID >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'competitionID' : '<< COMPETITION ID >>',
        EXPECTED: });
        """
        pass
