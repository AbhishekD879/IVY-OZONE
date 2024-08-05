import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C1931603_Banach_User_selected_free_bet_on_Betslip__Estimated_Returns_calculation(Common):
    """
    TR_ID: C1931603
    NAME: Banach. User selected free bet on Betslip - Estimated Returns calculation
    DESCRIPTION: Test case verifies successful Banach bet placement using freebets only
    DESCRIPTION: AUTOTEST [C2592702]
    PRECONDITIONS: Banach free bets tokens - a standard offer with default sportsbook token reward should be configured and active, with all channels ticked- it will include new Banach OB channels
    PRECONDITIONS: [To add freebet to user account][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To retrieve Banach Odds value check Network tab : price request
    PRECONDITIONS: **User has Banach free bets**
    PRECONDITIONS: **Banach selections are added to the dashboard**
    """
    keep_browser_open = True

    def test_001_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place bet" button
        EXPECTED: - Betslip with price field and freebets dropdown appears
        """
        pass

    def test_002_select_freebet_from_the_dropdown(self):
        """
        DESCRIPTION: Select freebet from the dropdown
        EXPECTED: total Stake and Estimated Returned are populated with the values
        EXPECTED: - Total Stake - amount of freebet
        EXPECTED: - Estimated Returns - calculated based on Odds value: (odds + 1)*freebet - freebet
        """
        pass
