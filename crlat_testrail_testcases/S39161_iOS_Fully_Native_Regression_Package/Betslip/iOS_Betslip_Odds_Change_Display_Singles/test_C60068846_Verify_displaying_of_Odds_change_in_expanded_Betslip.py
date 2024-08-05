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
class Test_C60068846_Verify_displaying_of_Odds_change_in_expanded_Betslip(Common):
    """
    TR_ID: C60068846
    NAME: Verify displaying of Odds change in expanded Betslip
    DESCRIPTION: Test case verifies Odd change UI in expanded bet slip (single)
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Native app installed and opened
    PRECONDITIONS: User added 1 selection to bet slip
    PRECONDITIONS: betslip Expanded
    """
    keep_browser_open = True

    def test_001__trigger_odds_change_for_current_selection(self):
        """
        DESCRIPTION: * Trigger Odds change for current selection.
        EXPECTED: * Odds change triggered
        EXPECTED: * bet slip remains expanded
        EXPECTED: * Odds must alter the colour according to UX guidelines
        EXPECTED: * including animation
        EXPECTED: * after 3 seconds the colour will change back to the original colour
        EXPECTED: Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/121800688) ![](index.php?/attachments/get/121800689)
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
        EXPECTED: * bet slip remains expanded
        EXPECTED: * Odds must alter the colour according to UX guidelines
        EXPECTED: * including animation
        EXPECTED: * after 3 seconds the colour will change back to the original colour
        EXPECTED: Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/121800690) ![](index.php?/attachments/get/121800691)
        """
        pass
