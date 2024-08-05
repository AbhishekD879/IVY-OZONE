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
class Test_C14640163_Big_Competition_displaying_events_with_different_markets_within_Knokout_tab(Common):
    """
    TR_ID: C14640163
    NAME: Big Competition: displaying events with different markets within 'Knokout' tab
    DESCRIPTION: This test case verifies that events with markets from 'Match Betting', 'Match Result', 'To Qualify' market templates are displayed in a Big Competition > Knokout tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 3 events: 1) With market from 'Match Betting' market template; 2) With market from 'Match Result' market template; 3) With market from 'To Qualify' market template.
    PRECONDITIONS: - You should have configured Big Competition > Knokout tab to display events above
    """
    keep_browser_open = True

    def test_001___go_to_configured_big_competition_eg_champions_league__knokout_tab__verify_displaying_of_events_from_preconditions(self):
        """
        DESCRIPTION: - Go to configured Big Competition (e.g. Champions League) > Knokout tab
        DESCRIPTION: - Verify displaying of events from preconditions
        EXPECTED: 3 events with  'Match Betting',  'Match Result', 'To Qualify' market template names are displayed
        """
        pass
