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
class Test_C14640164_Big_Competition_displaying_events_with_different_markets_within_Next_Games_section(Common):
    """
    TR_ID: C14640164
    NAME: Big Competition: displaying events with different markets within 'Next Games' section
    DESCRIPTION: This test case verifies that events with markets from 'Match Betting', 'Match Result', 'To Qualify' market templates are displayed in a Big Competition > Featured tab > Next Games section
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 events: 1) With market from 'Match Betting' market template; 2) With market from 'Match Result' market template.
    PRECONDITIONS: - You should have configured Big Competition > Featured tab > Next Games section to display events above
    """
    keep_browser_open = True

    def test_001___go_to_configured_big_competition_eg_champions_league__featured_tab__next_games_section__verify_displaying_of_events_from_preconditions(self):
        """
        DESCRIPTION: - Go to configured Big Competition (e.g. Champions League) > Featured tab > Next Games section
        DESCRIPTION: - Verify displaying of events from preconditions
        EXPECTED: 2 events with both market template names are displayed
        """
        pass
