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
class Test_C64569608_Verify_the_four_Filters_displayed_under_BYB_BB_tab(Common):
    """
    TR_ID: C64569608
    NAME: Verify the four Filters displayed under BYB/BB tab
    DESCRIPTION: This test case verifies the display of Filters in BYB/BB tab
    PRECONDITIONS: 1: BYB/BB markets should be available for the event
    PRECONDITIONS: 2: In CMS &gt; BYB &gt; BYB Markets - Atleast one or more Markets should be configured to Team Bets, Player Bets , Popular Markets
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
        EXPECTED: EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB tab should be displayed with all the Markets
        """
        pass

    def test_004_validate_the_display_of_filters(self):
        """
        DESCRIPTION: Validate the display of filters
        EXPECTED: * Four Filters should be displayed
        EXPECTED: * All Markets , Popular Markets, Player Bets, Team Bets
        EXPECTED: * All Markets should be displayed by default
        EXPECTED: * First two markets should be expanded by default
        EXPECTED: ![](index.php?/attachments/get/6a755d66-22bc-4db8-8a7d-d31eeaf5ec36) ![](index.php?/attachments/get/593d4b51-524c-4227-8c0f-0823cb253a04)
        """
        pass

    def test_005_validate_the_css_styles(self):
        """
        DESCRIPTION: Validate the CSS styles
        EXPECTED: * CSS styles should be as per Zeplin
        EXPECTED: https://app.zeplin.io/project/610ba4fa9f2dc2bf673ee8d5/dashboard?sid=61aa32fc874c5d901809a491
        """
        pass
