import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C58669560_Betslip_is_expanded_with_selections_added_to_bet_slip(Common):
    """
    TR_ID: C58669560
    NAME: Betslip is expanded with selections added to bet slip
    DESCRIPTION: This case verifies Bottom Bar Behaviour in the case when Betslip is expanded
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: Design
    PRECONDITIONS: https://zpl.io/blkQB8G - Ladbrokes
    PRECONDITIONS: https://zpl.io/bWmlDxj - Coral
    PRECONDITIONS: !!! Design is not updated for the Bottom Bar view of expanded Betslip
    """
    keep_browser_open = True

    def test_001_add_1_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 1 selection to the Bet Slip
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_002_slide_bet_slip_upwards(self):
        """
        DESCRIPTION: Slide Bet Slip upwards
        EXPECTED: - The Bet slip is expanded
        EXPECTED: - Bottom bar is displayed
        """
        pass

    def test_003_collapse_bet_slip(self):
        """
        DESCRIPTION: Collapse bet slip
        EXPECTED: Bet slip is collapsed
        """
        pass

    def test_004_add_one_more_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one more selection to the Betslip
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_005_slide_bet_slip_upwards(self):
        """
        DESCRIPTION: Slide Bet Slip upwards
        EXPECTED: - The Bet slip is expanded
        EXPECTED: - Bottom bar is displayed
        """
        pass

    def test_006_tap_on_any_menu_item_on_the_bottom_bar(self):
        """
        DESCRIPTION: Tap on any menu item on the Bottom Bar
        EXPECTED: - Bet slip is collapsed
        EXPECTED: - User directed to the relevant page
        """
        pass

    def test_007_slide_bet_slip_upwards(self):
        """
        DESCRIPTION: Slide Bet Slip upwards
        EXPECTED: The Bet slip is expanded
        """
        pass

    def test_008_tap_on_app_logo_or_header_menu(self):
        """
        DESCRIPTION: Tap on app Logo or Header menu
        EXPECTED: Bet slip is collapsed
        """
        pass
