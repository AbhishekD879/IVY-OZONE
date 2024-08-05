import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C28888_To_archive_in_scope_of_OX_98_Verify_Bet_Placement_on_Forecast__Tricast_bets(Common):
    """
    TR_ID: C28888
    NAME: [To archive in scope of OX 98] Verify Bet Placement on 'Forecast' / 'Tricast' bets
    DESCRIPTION: This test case verifies bet placement of 'Forecast' / 'Tricast' bets
    DESCRIPTION: NOTE, User Story **BMA-3607**
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has sufficient funds to place bets
    """
    keep_browser_open = True

    def test_001_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_two_or_more_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open 'Bet Slip'
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_go_to_the_forecast__tricast_n_section(self):
        """
        DESCRIPTION: Go to the 'Forecast / Tricast (n)' section
        EXPECTED: 'Forecast / Tricast (n)' section is shown
        """
        pass

    def test_006_enter_stake_amount_manually_for_the_forecast__tricast_bet_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake amount manually for the 'Forecast / Tricast' bet and tap 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet receipt is shown
        EXPECTED: User balance is decreased by the value indicated in the 'Total Stake' field
        """
        pass
