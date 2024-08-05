import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64658686_Verify_the_display_of_Markets_with_Standard_WW_Template(Common):
    """
    TR_ID: C64658686
    NAME: Verify the display of Markets with Standard WW Template
    DESCRIPTION: This test case verifies display of market templet for ww
    PRECONDITIONS: Ex:WW
    PRECONDITIONS: ![](index.php?/attachments/get/95ffe34e-cd76-40ac-b4fe-a1cdef6064ec)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes__coral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes / Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: User should be able to navigate to EDP page
        """
        pass

    def test_003_validate_the_market_header_and_the_optionslabelsprice_button(self):
        """
        DESCRIPTION: Validate the Market Header and the options(Labels,Price Button)
        EXPECTED: Market for ww should be as below in Both Brands
        EXPECTED: 1.Option 1 Label and Option 1 Price Button
        EXPECTED: 2.Option 2 Label and Option 2 Price Button
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/f8d06654-ac80-431a-82d1-7ff8eeff52cf)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/b5a50ca2-d03a-4e55-b461-d864d22ac12e)
        """
        pass

    def test_004_verify_css_styles_for_all_labels_and_buttons_with_zeplin(self):
        """
        DESCRIPTION: Verify CSS styles for all labels and buttons with Zeplin
        EXPECTED: All Styles should be matched with Zephlin
        """
        pass

    def test_005_add_one_selection_to_betslip_or_quickbet_from_ww_market_and_place_bet(self):
        """
        DESCRIPTION: Add one selection to Betslip or Quickbet from WW market and Place Bet
        EXPECTED: Bet should be placed successfully
        """
        pass
