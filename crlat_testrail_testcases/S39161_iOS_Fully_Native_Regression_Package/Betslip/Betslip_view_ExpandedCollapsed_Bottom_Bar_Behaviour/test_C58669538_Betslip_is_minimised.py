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
class Test_C58669538_Betslip_is_minimised(Common):
    """
    TR_ID: C58669538
    NAME: Betslip is minimised
    DESCRIPTION: This case verifies Bottom Bar Behaviour in the case when the Betslip is minimized
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: Design
    PRECONDITIONS: https://zpl.io/blkQB8G - Ladbrokes
    PRECONDITIONS: https://zpl.io/bWmlDxj - Coral
    """
    keep_browser_open = True

    def test_001_add_1_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 1 selection to the Bet Slip
        EXPECTED: - Selection is added to the Betslip
        EXPECTED: - Collapsed Bet Slip view with Bottom Bar displayed
        """
        pass

    def test_002_add_one_more_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one more selection to the Betslip
        EXPECTED: - Selection is added to the Betslip
        EXPECTED: - Collapsed Bet Slip view with Bottom Bar displayed
        """
        pass

    def test_003_tap_on_any_menu_item_on_the_bottom_bar(self):
        """
        DESCRIPTION: Tap on any menu item on the Bottom Bar
        EXPECTED: - Bet slip remains in collapsed view
        EXPECTED: - User directed to the relevant page
        """
        pass
