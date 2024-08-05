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
class Test_C14742517_TO_BE_EDITEDVerify_data_in_Profit_Loss_section(Common):
    """
    TR_ID: C14742517
    NAME: [TO BE EDITED]Verify data in Profit/Loss section
    DESCRIPTION: This case needs to be edited according to the latest changes - including Vanilla.
    DESCRIPTION: This test case verifies the Profit/Loss section data (it's displayed for logged in user only).
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have a few processed bets (Won and Lost) on SPORT, LOTTO and POOLS tab and also Gaming bets.
    PRECONDITIONS: - The user should be logged in.
    PRECONDITIONS: - Go to Home page > My Bets > Settled Bets > Sport, Lotto and Pools tabs (for mobile)
    PRECONDITIONS: - Go to Landing page > My Bets > Settled Bets > Sport, Lotto and Pools tabs (for desktop)
    """
    keep_browser_open = True

    def test_001_for_mobiletabletgo_to_home_page__my_bets__settled_bets__sports_lotto_and_pools_tabsfor_desktoplanding_page__my_bets__settled_bets__sports_lotto_and_pools_tabs(self):
        """
        DESCRIPTION: **For Mobile/Tablet**
        DESCRIPTION: Go to Home page > My Bets > Settled Bets > Sports, Lotto and Pools tabs
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Landing page > My Bets > Settled Bets > Sports, Lotto and Pools tabs
        EXPECTED: Profit/Loss section is displayed and it's collapsed by default.
        """
        pass

    def test_002_expand_profitloss_section_in_sports_lotto_and_pools_tabs(self):
        """
        DESCRIPTION: Expand Profit/Loss section in Sports, Lotto and Pools tabs.
        EXPECTED: Profit/Loss section contains the following elements:
        EXPECTED: - Profit/Loss value: £x.xx
        EXPECTED: - Grey 'Sports'/'Lotto'/'Pools' text label is displayed (depending on the currently selected tab):
        EXPECTED: 'Sports' tab
        EXPECTED: 'Lotto' tab
        EXPECTED: 'Pools' tab
        EXPECTED: - 'Total Stakes: £x.xx' (shows amount of all Stakes for the specified period of time)
        EXPECTED: - 'Total Returns: £x.xx' (shows amount of all Returns for the specified period of time)
        EXPECTED: - Red / Green arrow indicator for Loss or Profit respectively (Profit: Right & up; Loss: Right & down)
        EXPECTED: - Clickable 'All Betting & Gaming' button that is switched to 'All Sports' and vice versa
        EXPECTED: - All numbers should match data in 'wss://openapi-tst2.egalacoral.com/socket.io/1/websocket/e5f8e166-a24a-418b-bf35-06299eb6765b' web socket, 'pagerResponse{}, walletTransactions'/'Summary' section (totalBets, totalWins, totalDeposit etc.)
        """
        pass
