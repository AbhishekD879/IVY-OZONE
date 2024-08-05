import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569669_Verify_the_display_of_Match_Booking_Template(Common):
    """
    TR_ID: C64569669
    NAME: Verify the display of Match Booking Template
    DESCRIPTION: This Test case verifies the display of Match Booking Template
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: Football EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_validate_the_display_of_match_booking_points_template_in_bybbb_markets(self):
        """
        DESCRIPTION: Validate the display of Match Booking Points template in BYB/BB Markets
        EXPECTED: * Time Period should be displayed with selections below
        EXPECTED: * Points should be displayed with Over and Under selections below
        EXPECTED: * Increment should be displayed with decimals 0.5,1.5...
        EXPECTED: ![](index.php?/attachments/get/5cd7db72-5f18-450f-bc3f-a651481bf252)
        """
        pass

    def test_004_validate_add_to_bet_builderadd_to_bet_slip_cta(self):
        """
        DESCRIPTION: Validate ADD TO BET BUILDER/ADD TO BET SLIP CTA
        EXPECTED: * ADD TO BET BUILDER/BETSLIP is disabled when anyone or both Time Period and Points are not selected
        EXPECTED: ![](index.php?/attachments/get/be111bc3-f2b6-487e-8e0e-405b54a240cc)
        EXPECTED: * ADD TO BET BUILDER/BETSLIP is enabled when both Time Period and Points are selected
        EXPECTED: ![](index.php?/attachments/get/daa48bf6-5236-44f9-9f63-63cbf3aa8598)
        """
        pass

    def test_005_click_on_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * Selection should be added BYB/BB Betslip
        EXPECTED: * ADDED should be displayed
        EXPECTED: ![](index.php?/attachments/get/762d6d9d-3923-4184-b8b7-4d2331775bfd)
        """
        pass
