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
class Test_C64569686_Verify_that_Popular_Market_is_highlighted_when_clicked_on_it(Common):
    """
    TR_ID: C64569686
    NAME: Verify that Popular Market is highlighted when clicked on it
    DESCRIPTION: 
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets Popular Markets should be enabled for the below Markets
    PRECONDITIONS: To be Shown a card
    PRECONDITIONS: Anytime goal scorer
    PRECONDITIONS: Result
    PRECONDITIONS: Total Goals
    PRECONDITIONS: Player shots on target
    PRECONDITIONS: Player shots
    PRECONDITIONS: Tackles
    PRECONDITIONS: Total corners
    PRECONDITIONS: Assists
    PRECONDITIONS: Both teams to score
    PRECONDITIONS: Booking points
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the above Markets
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral Application
        EXPECTED: User should be able to Launch the Ladbrokes/Coral successfully
        """
        pass

    def test_002_navigate_to_any_event_which_has_byb_markets_gt_edp(self):
        """
        DESCRIPTION: Navigate to ANY event which has BYB markets &gt; EDP
        EXPECTED: User should be able to navigate to Football Event Details page
        """
        pass

    def test_003_click_on_build_your_bet_or_bet_builder(self):
        """
        DESCRIPTION: Click on Build Your Bet or Bet Builder
        EXPECTED: * Bet Builder/Build Your Bet tab should be opened
        """
        pass

    def test_004_validate_the_display_of_bybbb_tab(self):
        """
        DESCRIPTION: Validate the display of BYB/BB tab
        EXPECTED: * Four Filters should be displayed based on the CMS configuration
        EXPECTED: * All Markets should be selected by default
        """
        pass

    def test_005_click_on_popular_markets_tab(self):
        """
        DESCRIPTION: Click on Popular Markets tab
        EXPECTED: * Popular Markets should be displayed
        """
        pass

    def test_006_validate_the_display_of_popular_markets_tab(self):
        """
        DESCRIPTION: Validate the display of Popular Markets tab
        EXPECTED: * Popular Markets should be selected and highlighted
        EXPECTED: * Highlights should be as per Zeplin
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/faa8d309-dbb7-4e0c-9eaf-2c4d408ee53c)
        EXPECTED: Lads:
        EXPECTED: ![](index.php?/attachments/get/b895a810-a592-43a5-ac2e-7bb9ce7626b5)
        """
        pass

    def test_007_validate_the_markets_expanded_by_default(self):
        """
        DESCRIPTION: Validate the markets expanded by default
        EXPECTED: * First Market should be expanded by default
        """
        pass
