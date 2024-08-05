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
class Test_C64658687_Verify_the_display_of_Markets_with_Standard_WDW_Template(Common):
    """
    TR_ID: C64658687
    NAME: Verify the display  of Markets with Standard WDW Template
    DESCRIPTION: This test case verifies display of market templet for WDW in EDP page
    PRECONDITIONS: Ex:
    PRECONDITIONS: ![](index.php?/attachments/get/bb8ed288-1b5d-4bf8-8d4d-094fe1d850de)
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
        EXPECTED: Market for WDW should be as below
        EXPECTED: 1.Option 1 Label and Option 1 Price Button
        EXPECTED: 2.Option 2 Label and Option 2 Price Button
        EXPECTED: 3. Option 3 Label and Option 3 price button
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/5093a59a-48fa-448a-98ad-b23b71832751)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/44de445b-0828-476e-ab08-5b78b9b3c350)
        """
        pass

    def test_004_verify_css_styles_for_all_labels_and_buttons_with_zeplin(self):
        """
        DESCRIPTION: Verify CSS styles for all labels and buttons with Zeplin
        EXPECTED: All Styles should be matched with Zeplin
        """
        pass

    def test_005_add_one_selection_to_betslip_or_quickbet_from_wdw_market_and_place_bet(self):
        """
        DESCRIPTION: Add one selection to Betslip or Quickbet from WDW market and Place Bet
        EXPECTED: Bet should be placed successfully
        """
        pass
