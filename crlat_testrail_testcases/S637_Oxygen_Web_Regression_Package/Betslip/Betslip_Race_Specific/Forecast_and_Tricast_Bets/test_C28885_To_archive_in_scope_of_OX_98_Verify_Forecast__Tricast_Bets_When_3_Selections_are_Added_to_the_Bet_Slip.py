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
class Test_C28885_To_archive_in_scope_of_OX_98_Verify_Forecast__Tricast_Bets_When_3_Selections_are_Added_to_the_Bet_Slip(Common):
    """
    TR_ID: C28885
    NAME: [To archive in scope of OX 98] Verify 'Forecast / Tricast' Bets When 3 Selections are Added to the Bet Slip
    DESCRIPTION: This test case verifies the 'Forecast / Tricast' section when 3 selections are added to the Bet Slip
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
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_three_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add three selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open 'Bet Slip'
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_verify_forecast__tricast_section_when_both_forecast_and_tricast_bets_are_available(self):
        """
        DESCRIPTION: Verify 'Forecast / Tricast' section when both forecast and tricast bets are available
        EXPECTED: 'Forecast / Tricast ' section is shown
        EXPECTED: Section header is 'Forecast / Tricast (3)'
        EXPECTED: Section consists of three fields: **'Tricast (1)'** ,**'Combination Tricast (6)'** and **'Combination Forecast (6)'**
        """
        pass

    def test_006_verify_tricast_1_field(self):
        """
        DESCRIPTION: Verify **'Tricast (1)'** field
        EXPECTED: 'Tricast (1)' section is shown
        EXPECTED: 'Stake' field is shown under the section name
        """
        pass

    def test_007_verify_combination_tricast_6_field(self):
        """
        DESCRIPTION: Verify **'Combination Tricast (6)'** field
        EXPECTED: 'Combination Tricast (6)' section is shown
        EXPECTED: 'Stake' field is shown under the section name
        """
        pass

    def test_008_verify_combination_forecast_6_section(self):
        """
        DESCRIPTION: Verify **'Combination Forecast (6)'** section
        EXPECTED: 'Combination Forecast (6)' section is shown
        EXPECTED: 'Stake' field is shown under the section name
        """
        pass
