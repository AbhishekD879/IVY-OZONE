import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869691_TO_EDIT_Verify_Forecast__Tricast_Bets_when_2_Selections_are_Added_to_the_Bet_Slip(Common):
    """
    TR_ID: C869691
    NAME: [TO EDIT] Verify 'Forecast / Tricast' Bets when 2 Selections are Added to the Bet Slip
    DESCRIPTION: This test case verifies the 'Forecast / Tricast' section when 2 selections are added to the Bet Slip for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtual Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: User is logged in
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: Need to update according to the new design in BMA-43681, BMA-42906.
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
        EXPECTED: <Race> event details page is opened
        """
        pass

    def test_003_add_two_selections_from_the_same_event_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two selections from the same event to the Bet Slip
        EXPECTED: Bet Slip counter is increased
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_verify_forecast__tricast_section(self):
        """
        DESCRIPTION: Verify 'Forecast / Tricast' section
        EXPECTED: 'Forecast / Tricast ' section is shown
        EXPECTED: Section header is 'Forecast / Tricast (2)'
        EXPECTED: Section consists of two fields: '**Forecast (1)**' and '**Reverse Forecast (2)**'
        """
        pass

    def test_006_verify_forecast_1_section(self):
        """
        DESCRIPTION: Verify '**Forecast (1)**' section
        EXPECTED: 'Forecast(1)' section is shown
        EXPECTED: 'Stake:' field is shown below the section header
        """
        pass

    def test_007_verify_reverse_forecast_2_field(self):
        """
        DESCRIPTION: Verify '**Reverse Forecast (2)**' field
        EXPECTED: 'Reverse Forecast (2)' section is shown
        EXPECTED: 'Stake:' field is shown below the section header
        """
        pass
