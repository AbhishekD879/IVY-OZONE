import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.virtual_sports
@vtest
class Test_C16378872_Verify_adding_1st_2nd_3rd_and_ANY_selections_from_Tricast_tab_to_the_Bet_Slip_and_bet_placement(Common):
    """
    TR_ID: C16378872
    NAME: Verify adding 1st, 2nd, 3rd and ANY selections from Tricast tab to the Bet Slip and bet placement
    DESCRIPTION: This test case verifies adding 1st, 2nd, 3rd and ANY selections from Tricast tab to the Bet Slip and bet placement.
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C22901030](https://ladbrokescoral.testrail.com/index.php?/cases/view/22901030)
    DESCRIPTION: Desktop - [C23276348](https://ladbrokescoral.testrail.com/index.php?/cases/view/23276348)
    PRECONDITIONS: 1. Tricast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling. Note: Tricast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is logged in, has positive balance and located on Virtual Sports page.
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True

    def test_001_tap_virtual_sport_from_preconditions_where_tricast_market_is_configured(self):
        """
        DESCRIPTION: Tap Virtual Sport from preconditions where Tricast market is configured
        EXPECTED: Separate Tricast tabs is displayed.
        """
        pass

    def test_002_tap_tricast_tabtap_1st_2nd_and_3rd_selections_for_some_runnerstap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap Tricast tab
        DESCRIPTION: Tap 1st, 2nd and 3rd selections for some runners
        DESCRIPTION: Tap Add to Betslip button
        EXPECTED: - Selected selections were successfully added to the BetSlip;
        EXPECTED: - 'Tricast' market is displayed below added selections;
        EXPECTED: - Time, place and date is displayed below 'Tricast' market (e.g. - 15:20 Cartmel);
        EXPECTED: - Stake field is empty;
        EXPECTED: - Est. Returns field is populated by 'N/A'.
        """
        pass

    def test_003_enter_some_valid_stake_into_stake_fieldtap_place_bet_button(self):
        """
        DESCRIPTION: Enter some valid stake into Stake field
        DESCRIPTION: Tap Place Bet button
        EXPECTED: - Bet was placed successfully;
        EXPECTED: - All information regarding the bet is correct (bet - type, price, market, time and date, selections, stake, total stake, potential returns) on the Bet Receipt;
        EXPECTED: - User balance has decreased on the correct number based on stake.
        """
        pass

    def test_004_go_back_to_the_tricast_tabadd_three_any_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go back to the Tricast tab
        DESCRIPTION: Add three ANY selections to the BetSlip
        EXPECTED: - Selected selections were successfully added to the BetSlip;
        EXPECTED: - 'Combination Tricast 6' market is displayed below added selections;
        EXPECTED: - Time, place and date is displayed below 'Combination Tricast 6' market (e.g. - 15:20 Cartmel);
        EXPECTED: - Stake field is empty;
        EXPECTED: - Est. Returns field is populated by 'N/A'.
        """
        pass

    def test_005_enter_some_valid_stake_into_stake_fieldtap_place_bet_button(self):
        """
        DESCRIPTION: Enter some valid stake into Stake field
        DESCRIPTION: Tap Place Bet button
        EXPECTED: - Bet was placed successfully;
        EXPECTED: - All information regarding the bet is correct (bet - type, price, market, time and date, selections, stake, total stake, potential returns) on the Bet Receipt;
        EXPECTED: - User balance has decreased on the correct number based on stake.
        """
        pass

    def test_006_go_to_the_my_accountsmy_betsopen_betsregular_tab(self):
        """
        DESCRIPTION: Go to the My Accounts/My Bets/Open Bets/Regular tab
        EXPECTED: Bets, placed on the previous steps are displayed with the correct information on Open Bets/Regular tab.
        """
        pass
