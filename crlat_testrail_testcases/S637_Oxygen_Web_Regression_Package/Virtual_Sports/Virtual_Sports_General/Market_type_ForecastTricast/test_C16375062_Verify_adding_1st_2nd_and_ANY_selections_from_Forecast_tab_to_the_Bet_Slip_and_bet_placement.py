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
class Test_C16375062_Verify_adding_1st_2nd_and_ANY_selections_from_Forecast_tab_to_the_Bet_Slip_and_bet_placement(Common):
    """
    TR_ID: C16375062
    NAME: Verify adding 1st, 2nd and ANY selections from Forecast tab to the Bet Slip and bet placement
    DESCRIPTION: This test case verifies adding 1st, 2nd and ANY selections from Forecast tab to the Bet Slip and bet placement.
    PRECONDITIONS: 1. Forecast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling.
    PRECONDITIONS: Note: Forecast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is logged in, has positive balance and located on Virtual Sports page.
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True

    def test_001_tap_virtual_sport_from_preconditions_where_forecast_market_is_configured(self):
        """
        DESCRIPTION: Tap Virtual Sport from preconditions where Forecast market is configured.
        EXPECTED: Separate Forecast tabs is displayed.
        """
        pass

    def test_002_tap_forecast_tabtap_1st_and_2nd_selections_for_some_runnerstap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap Forecast tab
        DESCRIPTION: Tap 1st and 2nd selections for some runners
        DESCRIPTION: Tap Add to Betslip button.
        EXPECTED: - Selected selections were successfully added to the BetSlip;
        EXPECTED: - 'Forecast' market is displayed below added selections;
        EXPECTED: - Time, place and date is displayed below 'Forecast' market (e.g. - 15:20 Cartmel);
        EXPECTED: - Stake field is empty;
        EXPECTED: - Est. Returns field is populated by 'N/A'.
        """
        pass

    def test_003_enter_some_valid_stake_into_stake_fieldtap_place_bet_button(self):
        """
        DESCRIPTION: Enter some valid stake into Stake field
        DESCRIPTION: Tap Place Bet button.
        EXPECTED: - Bet was placed successfully;
        EXPECTED: - All information regarding the bet is correct (bet type, price, market, time and date, selections, stake, total stake, potential returns) on the Bet Receipt;
        EXPECTED: - User balance has decreased on the correct number based on stake.
        """
        pass

    def test_004_go_back_to_the_forecast_tabadd_two_any_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go back to the Forecast tab
        DESCRIPTION: Add two ANY selections to the BetSlip.
        EXPECTED: - Selected selections were successfully added to the BetSlip;
        EXPECTED: - 'Reverse Forecast 2' market is displayed below added selections;
        EXPECTED: - Time, place and date is displayed below 'Reverse Forecast 2' market (e.g. - 15:20 Cartmel);
        EXPECTED: - Stake field is empty;
        EXPECTED: - Est. Returns field is populated by 'N/A'.
        """
        pass

    def test_005_enter_some_valid_stake_into_stake_fieldtap_place_bet_button(self):
        """
        DESCRIPTION: Enter some valid stake into Stake field
        DESCRIPTION: Tap Place Bet button.
        EXPECTED: - Bet was placed successfully;
        EXPECTED: - All information regarding the bet is correct (bet type, price, market, time and date, selections, stake, total stake, potential returns)on the Bet Receipt;
        EXPECTED: - User balance has decreased on the correct number based on stake.
        """
        pass

    def test_006_go_to_the_my_accountsmy_betsopen_betsregular_tab(self):
        """
        DESCRIPTION: Go to the My Accounts/My Bets/Open Bets/Regular tab
        EXPECTED: Bets, placed on the previous steps are displayed with the correct information on Open Bets/Regular tab.
        """
        pass
