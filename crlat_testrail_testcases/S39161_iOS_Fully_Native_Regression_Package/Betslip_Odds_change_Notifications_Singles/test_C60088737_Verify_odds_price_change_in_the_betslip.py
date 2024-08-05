import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C60088737_Verify_odds_price_change_in_the_betslip(Common):
    """
    TR_ID: C60088737
    NAME: Verify odds price change in the betslip
    DESCRIPTION: This test case verifies odds price change in the betslip
    PRECONDITIONS: * Ladbrokes
    PRECONDITIONS: * Coral
    PRECONDITIONS: Install and launch the app.
    """
    keep_browser_open = True

    def test_001_tap_on_any_odd(self):
        """
        DESCRIPTION: Tap on any odd
        EXPECTED: Odd is selected
        """
        pass

    def test_002_expand_the_betslip(self):
        """
        DESCRIPTION: Expand the betslip.
        EXPECTED: Betslip is expanded.
        """
        pass

    def test_003_wait_until_the_price_will_be_changed(self):
        """
        DESCRIPTION: Wait until the price will be changed.
        EXPECTED: * Price is changed in the following way -  Price changed from X/X to X/X
        EXPECTED: * Coral
        EXPECTED: ![](index.php?/attachments/get/122187937)
        EXPECTED: * Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/122187940)
        """
        pass

    def test_004_repeat_1_3_steps_with_dark_mode(self):
        """
        DESCRIPTION: Repeat 1-3 steps with Dark mode.
        EXPECTED: * Coral:
        EXPECTED: ![](index.php?/attachments/get/122187939)
        EXPECTED: * Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/122187938)
        """
        pass
