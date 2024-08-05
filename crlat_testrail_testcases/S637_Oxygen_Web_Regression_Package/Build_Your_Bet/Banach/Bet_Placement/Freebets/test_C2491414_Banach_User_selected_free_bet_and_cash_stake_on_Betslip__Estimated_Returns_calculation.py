import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2491414_Banach_User_selected_free_bet_and_cash_stake_on_Betslip__Estimated_Returns_calculation(Common):
    """
    TR_ID: C2491414
    NAME: Banach. User selected free bet and cash stake on Betslip - Estimated Returns calculation
    DESCRIPTION: Test case verifies Estimated Returns calculation on Banach Betslip when user combines free bet and and cash stake
    PRECONDITIONS: Banach free bets tokens - a standard offer with default sportsbook token reward should be configured and active, with all channels ticked- it will include new Banach OB channels. Ahhoc tokens with default offer ID will not work for Banach bets. Only adhoc tokens created with associated Banach offer as mentioned above.
    PRECONDITIONS: [To add freebet to user account][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **User has Banach free bets**
    PRECONDITIONS: **User has added Banach selections to dashboard**
    """
    keep_browser_open = True

    def test_001_tap_on_odds_area(self):
        """
        DESCRIPTION: Tap on odds area
        EXPECTED: - Betslip with price field, numeric keyboard and freebets dropdown appears
        """
        pass

    def test_002_select_free_bet_from_dropdown(self):
        """
        DESCRIPTION: Select Free bet from dropdown
        EXPECTED: Total Stake and Estimated Returned are populated with the values
        EXPECTED: - Total Stake - amount of freebet
        EXPECTED: - Estimated Returns - calculated based on Odds value:
        EXPECTED: (odds + 1)*freebet - freebet
        """
        pass

    def test_003_enter_cash_stake_in_a_stake_box(self):
        """
        DESCRIPTION: Enter cash stake in a Stake box
        EXPECTED: total Stake and Estimated Returned values are updated
        EXPECTED: - Total Stake: cash stake + freebet (further Total Stake)
        EXPECTED: - Estimated Returns: (odds +1)*Total Stake - freebet
        """
        pass
