import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869695_To_archive_after_OX100_Verify_Bet_Placement_on_Forecast__Tricast_bets(Common):
    """
    TR_ID: C869695
    NAME: [To archive after OX100] Verify Bet Placement on 'Forecast' / 'Tricast' bets
    DESCRIPTION: This test case verifies bet placement of 'Forecast' / 'Tricast' bets for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has sufficient funds to place bets
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_virtual_racing_event_details_page(self):
        """
        DESCRIPTION: Go to the <Virtual Racing> event details page
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

    def test_007_enter_stake_via_free_bet_option___tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake via free bet option -> tap 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet receipt is shown
        EXPECTED: User balance is NOT decreased by the value indicated in the 'Toal Stake' value
        """
        pass

    def test_008_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step #7
        EXPECTED: 
        """
        pass

    def test_009_in_the_stake_field_enter_some_value_and_select_free_bet_from_the_dropdown___tap_bet_now_button(self):
        """
        DESCRIPTION: In the 'Stake:' field enter some value and select free bet from the dropdown -> tap 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet receipt is shown
        EXPECTED: User balance is decreased by value:
        EXPECTED: **Total Stake - free-bet**
        """
        pass

    def test_010_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step #7
        EXPECTED: 
        """
        pass
