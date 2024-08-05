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
class Test_C869698_To_edit_Verify_Bet_Receipt_for_Forecast__Tricast_Bets(Common):
    """
    TR_ID: C869698
    NAME: [To edit] Verify Bet Receipt for Forecast / Tricast Bets
    DESCRIPTION: This test case verifies bet receipt which is shown for forecast / tricast bets when such bet was placed
    DESCRIPTION: for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_virtual_racing_event_details_page(self):
        """
        DESCRIPTION: Go to the <Virtual Racing> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_several_selections_from_the_same_market(self):
        """
        DESCRIPTION: Add several selections from the same market
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip_forecast__tricast_section(self):
        """
        DESCRIPTION: Open Bet Slip, 'Forecast / Tricast' section
        EXPECTED: Section is shown
        """
        pass

    def test_005_enter_stakes_in_a_stake_field_for_any_forecast__tricast_bet(self):
        """
        DESCRIPTION: Enter stakes in a 'Stake" field for any forecast / tricast bet
        EXPECTED: Stakes are entered
        """
        pass

    def test_006_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: User balance is decreased by the 'Total Stake' value
        EXPECTED: Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_007_verify_header(self):
        """
        DESCRIPTION: Verify header
        EXPECTED: Bet Receipt header and back button are present
        EXPECTED: Forecasts and Tricasts appear in "Singles" section of the bet receipt
        """
        pass

    def test_008_verify_forecast__tricast_information(self):
        """
        DESCRIPTION: Verify forecast / tricast information
        EXPECTED: Bet Receipt contains information about just placed forecast / tricast bets:
        EXPECTED: *   The selections made by the customer and which are included in the forecast / tricast bet
        EXPECTED: *   the market type user has bet on - i.e. Win or Each Way
        EXPECTED: *   the event name which outcomes belong to
        EXPECTED: *   the Bet ID i.e. "O/0123828/0000155"
        EXPECTED: *   Stake
        EXPECTED: *   Est. Returns
        EXPECTED: All information is displayed according to the latest designs
        """
        pass

    def test_009_verify_total_stake_and_total_est_returns_fields(self):
        """
        DESCRIPTION: Verify 'Total Stake' and 'Total Est. Returns' fields
        EXPECTED: 'Total Stake' and 'Totals Est. Returns' are shown corresponding to the values on the Bet Slip
        """
        pass

    def test_010_verify_back_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Verify Back button on Bet Receipt page
        EXPECTED: User gets back to the previous page
        EXPECTED: Empty Bet Slip page is opened
        """
        pass

    def test_011_verify_reuse_selection_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Verify 'Reuse Selection' button on Bet Receipt page
        EXPECTED: User is returned to the Betslip to initiate bet placement again on the same selections
        """
        pass

    def test_012_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: User is returned to the apropriate <Race> landing page
        """
        pass
