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
class Test_C37568645_Verify_Odds_Price_Change(Common):
    """
    TR_ID: C37568645
    NAME: Verify Odds Price Change
    DESCRIPTION: This test case verifies behavior Odds button on Greyhound event card when price selection is changed
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://zpl.io/bL16pJd
    DESCRIPTION: Coral:
    DESCRIPTION: https://zpl.io/VOpKOyj
    PRECONDITIONS: Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Featured Tab is displayed by default
    PRECONDITIONS: The Greyhound  module is present on Featured Tab
    PRECONDITIONS: The Greyhound  module includes one or more Greyhound Events
    """
    keep_browser_open = True

    def test_001_emulate_the_selection_price_change_price_up(self):
        """
        DESCRIPTION: Emulate the selection price change (Price up)
        EXPECTED: The Odds Price within Odds Button changes color as per design
        EXPECTED: (animation' duration is 2000ms)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/45687987)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/45687989)
        """
        pass

    def test_002_emulate_the_selection_price_change_down(self):
        """
        DESCRIPTION: Emulate the selection price change (Down)
        EXPECTED: The Odds Price within Odds Button changes color as per design above
        EXPECTED: (animation duration is 2000ms)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/45687993)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/45687994)
        """
        pass
