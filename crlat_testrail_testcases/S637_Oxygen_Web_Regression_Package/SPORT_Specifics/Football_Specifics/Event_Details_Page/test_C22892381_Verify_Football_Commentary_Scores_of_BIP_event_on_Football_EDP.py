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
class Test_C22892381_Verify_Football_Commentary_Scores_of_BIP_event_on_Football_EDP(Common):
    """
    TR_ID: C22892381
    NAME: Verify Football Commentary Scores of BIP event on Football EDP
    DESCRIPTION: This test case verifies Football Commentary Scores of BIP event on Football EDP.
    PRECONDITIONS: Use https://confluence.egalacoral.com/display/SPI/Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 1) In order to have a Scores Football event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **participant_id** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **period_code**='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: *   **period_code**='FIRST_HALF/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF'** - to look at the scorers for the specific time
    PRECONDITIONS: *   **code**='SCORE'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    """
    keep_browser_open = True
