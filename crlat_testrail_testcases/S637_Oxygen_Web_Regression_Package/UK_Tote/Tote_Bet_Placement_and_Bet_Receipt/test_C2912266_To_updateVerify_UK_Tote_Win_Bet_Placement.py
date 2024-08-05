import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.races
@vtest
class Test_C2912266_To_updateVerify_UK_Tote_Win_Bet_Placement(Common):
    """
    TR_ID: C2912266
    NAME: (To update)Verify UK Tote Win Bet Placement
    DESCRIPTION: (To update) Betslip redesigned
    DESCRIPTION: This test case verifies bet placement on Win UK tote
    DESCRIPTION: AUTOTEST [C2989787]
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Win pool types are available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * User should have a Win pool type open
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_select_any_runners_press_win_button_and_tap_add_to_betslip_button_on_win_tote_bet_builder(self):
        """
        DESCRIPTION: Select any runners (press Win button) and tap "ADD TO BETSLIP" button on Win tote bet builder
        EXPECTED: * Tote Win bets are added to BetSlip
        EXPECTED: * Bet builder disappears
        EXPECTED: * BetSlip is increased by 1 number indicator
        """
        pass

    def test_002_open_betslip_and_verify_the_win_tote_bet(self):
        """
        DESCRIPTION: Open BetSlip and verify the Win tote bet
        EXPECTED: * There is a "remove" button to remove the Win tote bet from the BetSlip
        EXPECTED: * 'Bet now' button is disabled
        """
        pass

    def test_003_verify_bet_details_for_win_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Win tote bet
        EXPECTED: There are the following details on Win tote bet:
        EXPECTED: * "Singles (1)" label in the section header (Coral only)
        EXPECTED: * "Win Totepool"
        EXPECTED: * "Win" bet type name
        EXPECTED: * All selections with correct order according to the selected runners
        """
        pass

    def test_004_expand_the_bet_and_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Expand the bet and verify the start date and time of the race
        EXPECTED: * Time of the race is shown when the bet is expanded
        EXPECTED: * Format is the following:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        """
        pass

    def test_005_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the BetSlip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        pass

    def test_006_verify_estimated_returns(self):
        """
        DESCRIPTION: Verify "Estimated Returns"
        EXPECTED: Estimated Returns values are "N/A" for Tote bets
        """
        pass

    def test_007_verify_total_stake_and_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Stake" and "Total Est. Returns"
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        pass

    def test_008_tap_the_remove_button(self):
        """
        DESCRIPTION: Tap the "remove" button
        EXPECTED: Bet is removed from the betslip
        """
        pass

    def test_009_add_selection_to_betslip_once_again_enter_stake_and_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Add selection to betslip once again, enter stake and tap the "Bet Now" button
        EXPECTED: * Win Tote bet is successfully placed
        EXPECTED: * Win Tote Bet Receipt is shown
        """
        pass
