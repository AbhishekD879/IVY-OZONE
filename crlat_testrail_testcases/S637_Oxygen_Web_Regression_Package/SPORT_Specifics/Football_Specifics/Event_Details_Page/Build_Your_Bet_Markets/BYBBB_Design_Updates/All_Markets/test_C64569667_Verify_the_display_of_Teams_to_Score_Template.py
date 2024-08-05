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
class Test_C64569667_Verify_the_display_of_Teams_to_Score_Template(Common):
    """
    TR_ID: C64569667
    NAME: Verify the display of Teams to Score Template
    DESCRIPTION: This test case verifies the display of Teams to Score template
    PRECONDITIONS: 1: BYB/BB Markets should be available for any event
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: EDP page should be displayed with BYB/BB tab
        """
        pass

    def test_003_validate_the_display_of_teams_to_score_template_in_bybbb_markets(self):
        """
        DESCRIPTION: Validate the display of Teams to Score template in BYB/BB Markets
        EXPECTED: * To Score should be displayed with selections below
        EXPECTED: * Time Period should be displayed with selections below
        """
        pass

    def test_004_validate_the_display_of_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Validate the display of ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * ADD TO BET BUILDER / ADD TO BETSLIP should be disabled when no selections or any one from To Score and Time Period are not selected
        EXPECTED: ![](index.php?/attachments/get/7642c1ad-01df-4289-9a17-633b84c3558c)
        EXPECTED: * ADD TO BET BUILDER / ADD TO BETSLIP should be enabled when selections are selected from both To Score and Time period
        EXPECTED: ![](index.php?/attachments/get/1324739d-1752-43ad-979e-03cb3f33f156)
        """
        pass

    def test_005_click_on_add_to_bet_builder_add_to_betslip_when_enabled(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP (When enabled)
        EXPECTED: * Selection should be added to the BYB/BB betslip
        EXPECTED: * ADDED should be displayed
        EXPECTED: ![](index.php?/attachments/get/a72d1d45-52fa-4090-86c0-6a67d8ec147c)
        """
        pass
