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
class Test_C64569609_Verify_by_default_All_Markets_filter_is_selected(Common):
    """
    TR_ID: C64569609
    NAME: Verify by default 'All Markets' filter is selected
    DESCRIPTION: This test case verifies the display of All Markets filter selected by default
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

    def test_004_validate_the_display_of_all_markets(self):
        """
        DESCRIPTION: Validate the display of All Markets
        EXPECTED: * Four Filters should be displayed
        EXPECTED: * All Markets , Popular Markets, Player Bets, Team Bets
        EXPECTED: * All Markets should be displayed by default
        EXPECTED: * First two markets should be expanded by default
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/d01c4a09-7b5c-4d0f-b50d-4731723e4da2)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/90752670-bdaa-48e8-b823-095ececda13c)
        """
        pass

    def test_005_validate_the_css_styles(self):
        """
        DESCRIPTION: Validate the CSS styles
        EXPECTED: * CSS styles should be as per Zeplin
        EXPECTED: https://app.zeplin.io/project/610ba4fa9f2dc2bf673ee8d5/dashboard?sid=61717295eb76ea9f87269469
        """
        pass
