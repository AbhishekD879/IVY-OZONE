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
class Test_C14742520_Verify_Profit_Loss_calculations_for_All_Betting_Gaming_All_Sports_view(Common):
    """
    TR_ID: C14742520
    NAME: Verify Profit/Loss calculations for 'All Betting & Gaming'/'All Sports' view.
    DESCRIPTION: Test case verifies that the 'All Betting & Gaming'/'All Sports' button switcher is working as expected.
    PRECONDITIONS: - To see what CMS and TI is in use type “devlog” over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have a few processed bets (WON and LOST) on SPORT, LOTTO and POOLS tabs including Gaming bets. There is no separate 'Gaming' tab, but stakes are included in Profit/Loss as well.
    PRECONDITIONS: - User should be logged in.
    PRECONDITIONS: - Go to Home page > My Bets > Settled Bets > Sport, Lotto and Pools tabs (for mobile)
    PRECONDITIONS: - Go to Landing page > My Bets > Settled Bets > Sport, Lotto and Pools tabs (for desktop)
    """
    keep_browser_open = True

    def test_001_expand_profit__loss_section_and_take_a_look_at_the_profit__loss_total_stakes_and_total_returns_values(self):
        """
        DESCRIPTION: Expand 'Profit / Loss' section and take a look at the 'Profit / Loss', 'Total Stakes' and 'Total Returns' values.
        EXPECTED: 'Profit / Loss' value should be equal to ('Total Returnes') - ('Total Stakes') for just one tab that is currently active (Sports, Lotto or Pools)
        EXPECTED: Data on the UI should match the data in 'wss://openapi-tst2.egalacoral.com/socket.io/1/websocket/e5f8e166-a24a-418b-bf35-06299eb6765b' web socket, 'pagerResponse{}, walletTransactions'/'Summary' section (totalBets, totalWins, totalDeposit etc.)
        EXPECTED: * To know if the information is valid for Total Stakes filed you should simply add all stakes information of the events below the profit/loss section.
        EXPECTED: * To know if the information is valid for Total Returns filed you should simply add all returns information of the events below the profit/loss section.
        """
        pass

    def test_002_clicktap_all_betting__gaming_button_for_the_specified_period_of_time_and_take_a_look_at_the_profit__loss_total_stakes_and_total_returns_values(self):
        """
        DESCRIPTION: Click/Tap 'All Betting & Gaming' button for the specified period of time and take a look at the 'Profit / Loss', 'Total Stakes' and 'Total Returns' values.
        EXPECTED: 'Profit / Loss' value should be equal to ('Total Returns') - ('Total Stakes') for all betting and gaming values (Sports, Lotto and Pools in total)
        EXPECTED: All numbers should match data in 'wss://openapi-tst2.egalacoral.com/socket.io/1/websocket/e5f8e166-a24a-418b-bf35-06299eb6765b' web socket, 'pagerResponse{}, walletTransactions'/'Summary' section (totalBets, totalWins, totalDeposit etc.)
        EXPECTED: * To know if the information is valid for Total Stakes filed you should simply add all stakes information of the events below the profit/loss section.
        EXPECTED: * To know if the information is valid for Total Returns filed you should simply add all returns information of the events below the profit/loss section.
        """
        pass
