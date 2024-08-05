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
class Test_C60068845_Verify_displaying_of_Odds_change_in_collapsed_Betslip(Common):
    """
    TR_ID: C60068845
    NAME: Verify  displaying of Odds change in  collapsed Betslip
    DESCRIPTION: Test case verifies displaying of Odds change in  collapsed Betslip
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Native app installed and opened
    PRECONDITIONS: User added 1 selection to betslip
    PRECONDITIONS: betslip collapsed
    """
    keep_browser_open = True

    def test_001__trigger_odds_change_for_current_selection(self):
        """
        DESCRIPTION: * Trigger Odds change for current selection.
        EXPECTED: * Odds change triggered
        EXPECTED: * bet slip remains collapsed
        EXPECTED: * Odds must alter the colour  according to UX guidelines including animation
        EXPECTED: * after 3 seconds the colour will change back to the original colour
        EXPECTED: Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/121800638)
        EXPECTED: Coral/Ladbrokes:(Light theme):
        EXPECTED: ![](index.php?/attachments/get/121800639) ![](index.php?/attachments/get/121800640)
        """
        pass

    def test_002__enable_dark_theme_on_tested_device_settings___display__brightness___select_dark_theme(self):
        """
        DESCRIPTION: * Enable Dark Theme on tested device (Settings -> Display & Brightness -> Select "Dark" theme)
        EXPECTED: * Dark Theme was enabled
        """
        pass

    def test_003__trigger_odds_change_for_current_selection(self):
        """
        DESCRIPTION: * Trigger Odds change for current selection.
        EXPECTED: * Odds change triggered
        EXPECTED: * bet slip remains collapsed
        EXPECTED: * Odds must alter the colour  according to UX (Dark theme)guidelines including animation
        EXPECTED: * after 3 seconds the colour will change back to the original colour
        EXPECTED: Dark theme Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/121800656) ![](index.php?/attachments/get/121800657)
        """
        pass
