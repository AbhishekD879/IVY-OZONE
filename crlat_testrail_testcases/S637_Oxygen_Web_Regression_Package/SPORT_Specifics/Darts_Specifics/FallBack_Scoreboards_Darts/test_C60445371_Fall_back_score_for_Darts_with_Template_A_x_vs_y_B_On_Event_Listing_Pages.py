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
class Test_C60445371_Fall_back_score_for_Darts_with_Template_A_x_vs_y_B_On_Event_Listing_Pages(Common):
    """
    TR_ID: C60445371
    NAME: Fall back score for Darts with Template A <x> vs <y> B On Event Listing Pages
    DESCRIPTION: 1. To show Scores on all In-play Listing Pages for Sports Team A vs Team B (Not anything with S and P ) When we dont have score anywhere other than event name
    DESCRIPTION: In-play Listing Pages as per below
    DESCRIPTION: In-play Home Page    https://sports.coral.co.uk/home/in-play
    DESCRIPTION: In-play /All Sports (Streaming)    https://sports.coral.co.uk/in-play/watchlive
    DESCRIPTION: In-Play/Sports    https://sports.coral.co.uk/in-play/cricket
    DESCRIPTION: Sports - Matches Tab    https://sports.coral.co.uk/sport/football/matches/today
    DESCRIPTION: Sports -In-play Tab    https://sports.coral.co.uk/sport/football/live
    DESCRIPTION: Competition Landing Page    https://sports.coral.co.uk/competitions/football/football-uefa-club-competitions/uefa-champions-league
    DESCRIPTION: Note : CMS changes should be present as per below Document.
    DESCRIPTION: https://coralracing-my.sharepoint.com/:w:/g/personal/animisha_uppuluri_ivycomptech_com/EX9s5-XmNhREhoyRIoN1VYcBVWRHVPpI3MMVhZ4u4UOkiw?email=Animisha.Uppuluri%40ivycomptech.com&e=4%3A0LdMbH&at=9&CID=AC96F282-B011-45FF-AAE0-76C75E7EE4BB&wdLOR=c6B47E59E-DA9E-428D-BAD5-983F641BFDB1
    PRECONDITIONS: Player A* (1) 0-0 (0) Player B
    PRECONDITIONS: Sets score is represented by the bracket x bracket within this string. and the Legs are taken from the x-x format within the middle of the string.
    PRECONDITIONS: If no score is passed within the event name or removed from the event name then the scoreboard layout should be removed.
    PRECONDITIONS: Serve Indicators - The serve indicator should be shown as per the GD. The indicator of serve (if applicable) is passed in the string and will show as an * against the Player/Team name
    PRECONDITIONS: Team/Player A* (0) 0-3 (1) Team/Player B
    """
    keep_browser_open = True

    def test_001_verify_that_scores_are_in_team_a_x_vs_y_team_b_format(self):
        """
        DESCRIPTION: Verify that scores are in Team A <x> vs <y> Team B format
        EXPECTED: Score should be in next format
        EXPECTED: Team/Player A	2-1	Team/Player B
        EXPECTED: Team/Player A	15-28	Team/Player B
        EXPECTED: ![](index.php?/attachments/get/31356)
        EXPECTED: ![](index.php?/attachments/get/126299335)
        """
        pass

    def test_002_verify_that_no_scores_available_in_the_event_name(self):
        """
        DESCRIPTION: Verify that no scores available in the event name
        EXPECTED: Should show :
        EXPECTED: - player/team names;
        EXPECTED: - event start time;
        EXPECTED: - watch/live icon next to start time
        EXPECTED: ![](index.php?/attachments/get/31357)
        """
        pass
