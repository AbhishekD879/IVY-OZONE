import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2855508_Vertify_Smart_Boost_module_on_Featured_tab(Common):
    """
    TR_ID: C2855508
    NAME: Vertify 'Smart Boost' module on Featured tab
    DESCRIPTION: This test case verifies the Smart Boost module and its content on featured tab
    PRECONDITIONS: 1. User is on Featured Home page
    PRECONDITIONS: 2. Smart Boost module is configured in CMS (with 'Select Events by: Selection' option while configuring) and is Active
    PRECONDITIONS: 3. Module has selections with Price Boost flags in Open Bet TI
    PRECONDITIONS: 4. Selection contains 'Was price' value in its name in brackets in Open Bet TI (in decimal format)
    """
    keep_browser_open = True

    def test_001_verify_selections_within_the_module(self):
        """
        DESCRIPTION: Verify selections within the module
        EXPECTED: Only 1 selection is present within the module with smart boost available
        """
        pass

    def test_002_verify_the_format_of_selection(self):
        """
        DESCRIPTION: Verify the format of selection
        EXPECTED: * Selection name is displayed on the left
        EXPECTED: * Price odds button is displayed opposite to the selection name (on the right)
        EXPECTED: * Previous price of selection is placed under price odds button (on the right)
        EXPECTED: * Start time/date of event is displayed under selection name (on the left)
        """
        pass

    def test_003_switch_to_fractional_format_top_right_menu__settings__odds_format(self):
        """
        DESCRIPTION: Switch to fractional format (top right menu-> Settings-> odds format)
        EXPECTED: Selection previous price remains crossed out and displayed under odd price button
        """
        pass

    def test_004_click_on_the_selection_within_the_module_on_featured_tab(self):
        """
        DESCRIPTION: Click on the selection within the module on Featured tab
        EXPECTED: User is redirected to its EDP
        """
        pass
