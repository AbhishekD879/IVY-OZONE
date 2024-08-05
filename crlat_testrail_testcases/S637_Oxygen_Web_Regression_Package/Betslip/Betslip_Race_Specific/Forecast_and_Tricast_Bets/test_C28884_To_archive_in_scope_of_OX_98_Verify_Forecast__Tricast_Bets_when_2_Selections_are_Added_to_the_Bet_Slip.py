import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C28884_To_archive_in_scope_of_OX_98_Verify_Forecast__Tricast_Bets_when_2_Selections_are_Added_to_the_Bet_Slip(Common):
    """
    TR_ID: C28884
    NAME: [To archive in scope of OX 98] Verify 'Forecast / Tricast' Bets when 2 Selections are Added to the Bet Slip
    DESCRIPTION: This test case verifies 'Forecast' and 'Reverse Forecast' bet options when <Race> selections are added to the Bet Slip
    DESCRIPTION: NOTE, User Story **BMA-3607**
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_race_event_details_page(self):
        """
        DESCRIPTION: Go to the <Race> event details page
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
        EXPECTED: 'Forecast / Tricasts ' section is shown
        EXPECTED: Section header is 'Forecast / Tricast (2)'
        EXPECTED: Section consists of two fields: **'Forecast (1)'** and **'Reverse Forecast (2)'**
        """
        pass

    def test_006_verify_forecast_1_section(self):
        """
        DESCRIPTION: Verify **'Forecast (1)'** section
        EXPECTED: 'Forecast(1)' section is shown
        EXPECTED: 'Stake' field is shown below the section header
        """
        pass

    def test_007_verify_reverse_forecast_2_field(self):
        """
        DESCRIPTION: Verify **'Reverse Forecast (2)'** field
        EXPECTED: 'Reverse Forecast (2)' section is shown
        EXPECTED: 'Stake' field is shown below the section header
        """
        pass
