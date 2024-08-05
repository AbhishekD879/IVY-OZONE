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
class Test_C64569685_Verify_the_Markets_displayed_under_Popular_Markets_tab(Common):
    """
    TR_ID: C64569685
    NAME: Verify the Markets displayed under Popular Markets tab
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
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/a83f0b84-6f73-433c-b1d0-31da8783e7c5)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/7f1f4fe6-f418-45ff-a4ad-bbd472761bca)
        """
        pass

    def test_007_validate_the_display_order_of_the_markets_in_popular_markets_tab(self):
        """
        DESCRIPTION: Validate the display order of the markets in Popular Markets tab
        EXPECTED: * The display order of Markets should be as per CMS
        """
        pass

    def test_008_validate_the_markets_expanded_by_default(self):
        """
        DESCRIPTION: Validate the markets expanded by default
        EXPECTED: * First Market should be expanded by default
        """
        pass

    def test_009_expandcollapse_markets(self):
        """
        DESCRIPTION: Expand/Collapse Markets
        EXPECTED: * User should be able to Expand or Collapse the Markets
        EXPECTED: * On Expansion if the Market has Market Description configured in CMS
        EXPECTED: Market Description should be displayed
        EXPECTED: * CSS styles should be as per Zeplin
        """
        pass

    def test_010_navigate_to_cms_gt_byb_gt_byb_marketsdisable_popular_markets_checkbox_for_one_of_the_markets(self):
        """
        DESCRIPTION: Navigate to CMS &gt; BYB &gt; BYB Markets
        DESCRIPTION: Disable Popular Markets checkbox for one of the Markets
        EXPECTED: User should be able to disable and save successfully
        """
        pass

    def test_011_navigate_to_ladbrokescoral_gt_football_edpvalidate_the_display_of_market_in_popular_markets_tab(self):
        """
        DESCRIPTION: Navigate to Ladbrokes/Coral &gt; Football EDP
        DESCRIPTION: Validate the display of Market in Popular Markets tab
        EXPECTED: * The Market for which Popular Markets has been disabled should NO longer be displayed in Popular Markets tab
        """
        pass
