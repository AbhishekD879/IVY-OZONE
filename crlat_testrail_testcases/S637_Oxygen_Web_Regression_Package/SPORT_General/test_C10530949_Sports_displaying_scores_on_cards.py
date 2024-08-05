import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C10530949_Sports_displaying_scores_on_cards(Common):
    """
    TR_ID: C10530949
    NAME: <Sports> displaying scores on cards
    DESCRIPTION: This test case verifies displaying of scores for different sport cards
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have sports cards with scores for next sports:
    PRECONDITIONS: 1) Football
    PRECONDITIONS: 2) Tennis
    PRECONDITIONS: 3) Badminton
    PRECONDITIONS: 4) Volleyball
    PRECONDITIONS: - You should be on a <Sport> landing page > In-Play tab in application
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_card_with_scores_for_different_sports_types(self):
        """
        DESCRIPTION: Verify displaying of card with scores for different sports types
        EXPECTED: NOTE: Favorite icon is applicable to Football only
        EXPECTED: **Applicable to all cards:**
        EXPECTED: - 'Favorite' icon at the top left corner (shown if enabled in CMS > System Configuration > Structure > Favorites)
        EXPECTED: - 'WATCH' label at the top left corner next to the 'Favorite' icon (shown if stream enabled)
        EXPECTED: - 'LIVE' label at the top left corner next to the 'Favorite' icon (shown if event has started)
        EXPECTED: - 'WATCH LIVE' label at the top left corner next to the 'Favorite' icon (shown if event has started and has stream enabled)
        EXPECTED: - 'XX MORE >' markets link at the top right corner where XX - amount of all active markets-1 market that is displayed (if event has only 1 active market - link is not displayed)
        EXPECTED: - Teams names one under another are displayed at the bottom left corner
        EXPECTED: - ODDS buttons are displayed at the bottom right corner
        EXPECTED: **Football:**
        EXPECTED: - Time in live is displayed next to the 'LIVE' label
        EXPECTED: - Scores are displayed against proper team names near the first ODDS button
        EXPECTED: **Tennis:**
        EXPECTED: - Current set is displayed next to the 'LIVE' label
        EXPECTED: - S,G,P columns are displayed
        EXPECTED: - Proper scores of Sets, Games and Points are displayed against respective players near the first ODDS button
        EXPECTED: - Orange ball is displayed against attacking player near the sets value
        EXPECTED: **Badminton:**
        EXPECTED: - Current set is displayed next to the 'LIVE' label
        EXPECTED: - G,P columns are displayed
        EXPECTED: - Proper scores of Games and Points are displayed against respective players near the first ODDS button
        EXPECTED: - Orange ball is displayed against attacking player near the games value
        EXPECTED: **Volleyball:**
        EXPECTED: - S,P columns are displayed
        EXPECTED: - Proper values of Scores and Points are displayed against respective players near the first ODDS button
        """
        pass
