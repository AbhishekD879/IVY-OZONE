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
class Test_C60445370_Fall_back_Score_for_Darts_Sets__Legs(Common):
    """
    TR_ID: C60445370
    NAME: Fall back Score for Darts Sets / Legs
    DESCRIPTION: List of pages to be checked:
    DESCRIPTION: In-play Home Page https://sports.coral.co.uk/home/in-play
    DESCRIPTION: In-play /All Sports https://sports.coral.co.uk/in-play/watchlive
    DESCRIPTION: In-Play/Sports https://sports.coral.co.uk/in-play/cricket
    DESCRIPTION: Sports - Matches Tab https://sports.coral.co.uk/sport/football/matches/today
    DESCRIPTION: Sports -In-play Tab https://sports.coral.co.uk/sport/football/live
    DESCRIPTION: Note : CMS changes should be present as per below Document.
    DESCRIPTION: https://coralracing-my.sharepoint.com/:w:/g/personal/animisha_uppuluri_ivycomptech_com/EX9s5-XmNhREhoyRIoN1VYcBVWRHVPpI3MMVhZ4u4UOkiw?email=Animisha.Uppuluri%40ivycomptech.com&e=4%3A0LdMbH&at=9&CID=AC96F282-B011-45FF-AAE0-76C75E7EE4BB&wdLOR=c6B47E59E-DA9E-428D-BAD5-983F641BFDB1
    PRECONDITIONS: This template will apply to any event where there is not an Opta / Bwin fed scoreboard where the string in the event name appears as
    PRECONDITIONS: Player A* (1) 0-0 (0) Player B
    PRECONDITIONS: Sets score is represented by the bracket x bracket within this string. and the Legs are taken from the x-x format within the middle of the string.
    PRECONDITIONS: If no score is passed within the event name or removed from the event name then the scoreboard layout should be removed.
    PRECONDITIONS: Serve Indicators - The serve indicator should be shown as per the GD. The indicator of serve (if applicable) is passed in the string and will show as an * against the Player/Team name
    PRECONDITIONS: Team/Player A* (0) 0-3 (1) Team/Player B
    """
    keep_browser_open = True

    def test_001_verify_that_darts_basic_score_board_with_no_serve_indicator(self):
        """
        DESCRIPTION: Verify that Darts basic Score Board With No Serve Indicator
        EXPECTED: String should be Team/Player A (0) 0-3 (1) Team/Player B without serve indicator
        """
        pass

    def test_002_verify_that_darts_basic_score_board_with_serve_indicator_with_legs(self):
        """
        DESCRIPTION: Verify that Darts basic Score Board With Serve Indicator with Legs
        EXPECTED: String should be Team/Player A*  0-3  Team/Player B with serve indicator
        EXPECTED: ![](index.php?/attachments/get/122183501)
        """
        pass

    def test_003_verify_that_darts_basic_score_board_with_serve_indicator_with_sets__legs(self):
        """
        DESCRIPTION: Verify that Darts basic Score Board With Serve Indicator with Sets & Legs
        EXPECTED: String should be Team/Player A* (0) 0-3 (1) Team/Player B with serve indicator
        EXPECTED: ![](index.php?/attachments/get/122183505)
        """
        pass

    def test_004_verify_that_there_is_no_score_for_the_match(self):
        """
        DESCRIPTION: Verify that there is no score for the match
        EXPECTED: Should show:
        EXPECTED: - players name
        EXPECTED: - start and date time
        EXPECTED: ![](index.php?/attachments/get/122183499)
        """
        pass

    def test_005_verify_that_for_double_and_long_name_truncation_is_applied(self):
        """
        DESCRIPTION: Verify that for double and long name truncation is applied
        EXPECTED: K. Gerlach/J. Wachaczyk* (0) 1-1 (0) V. Heisen/K. Hobgarski
        EXPECTED: For long and doubles name truncation should applied as on scoreboards
        """
        pass
