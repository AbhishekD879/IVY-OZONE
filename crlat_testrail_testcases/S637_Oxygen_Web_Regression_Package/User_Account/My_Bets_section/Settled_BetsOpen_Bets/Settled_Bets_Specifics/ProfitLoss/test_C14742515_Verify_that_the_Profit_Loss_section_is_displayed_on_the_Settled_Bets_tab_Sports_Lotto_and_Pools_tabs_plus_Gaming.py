import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C14742515_Verify_that_the_Profit_Loss_section_is_displayed_on_the_Settled_Bets_tab_Sports_Lotto_and_Pools_tabs_plus_Gaming(Common):
    """
    TR_ID: C14742515
    NAME: Verify that the Profit/Loss section is displayed on the Settled Bets tab (Sports, Lotto and Pools tabs plus Gaming)
    DESCRIPTION: Test case verifies that the Profit/Loss section is displayed for logged in user.
    PRECONDITIONS: - To see what CMS and TI is in use type “devlog” over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have a few processed bets (Won and Lost) on SPORT, LOTTO and POOLS tab. Also, Gaming stakes should be placed and processed since they are included here as well.
    PRECONDITIONS: - User should be logged in.
    PRECONDITIONS: - Go to Home page > My Bets > Settled Bets > Sport, Lotto and Pools tabs (for mobile)
    PRECONDITIONS: - Go to Landing page > My Bets > Settled Bets > Sport, Lotto and Pools tabs (for desktop)
    """
    keep_browser_open = True

    def test_001_verify_that_the_profitloss_section_is_displayed_on_the_settled_bets_tab_sports_lotto_and_pools_sub_tabs(self):
        """
        DESCRIPTION: Verify that the Profit/Loss section is displayed on the Settled Bets tab, Sports, Lotto and Pools sub-tabs.
        EXPECTED: - Profit/Loss section is displayed on the Settled Bets tab, Sports, Lotto and Pools sub-tabs
        EXPECTED: - Profit/Loss section is collapsed by default
        """
        pass
