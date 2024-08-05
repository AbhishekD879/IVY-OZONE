import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C10700385_Verify_adding_selection_to_Betslip_with_slow_network_connection(Common):
    """
    TR_ID: C10700385
    NAME: Verify adding selection to Betslip with slow network connection
    DESCRIPTION: This test case verifies adding selection to Betslip with a slow network connection
    PRECONDITIONS: 1. Load app
    PRECONDITIONS: 2. Go to any <Sport>/<Race> page
    PRECONDITIONS: 3. Turn on slow 3G network connection
    """
    keep_browser_open = True

    def test_001_tap_any_sportrace_price_odds_button(self):
        """
        DESCRIPTION: Tap any <Sport>/<Race> price odds button
        EXPECTED: * Selection is marked in green
        EXPECTED: * Bet counter increases by 1
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * Added selection is present with valid data set
        EXPECTED: * All icons are present within Betslip (e.g rabish bin, '+'/'-' sign)
        """
        pass

    def test_003_make_a_few_different_sportrace_selections(self):
        """
        DESCRIPTION: Make a few different <Sport>/<Race> selections
        EXPECTED: * All selections are marked in green
        EXPECTED: * Bet counter increases by the added selections number
        """
        pass

    def test_004_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * Added selections are present with valid data set
        EXPECTED: * All icons are present within Betslip (e.g rabish bin, '+'/'-' sign)
        """
        pass

    def test_005_unselect_a_few_selections_from_sportrace_page(self):
        """
        DESCRIPTION: Unselect a few selections from <Sport>/<Race> page
        EXPECTED: * Selections are no more market in green
        EXPECTED: * Bet counter decreases by the unselected selections number
        EXPECTED: * Selections are removed from Betslip
        """
        pass

    def test_006_add_the_same_selections_to_betslip(self):
        """
        DESCRIPTION: Add the same selections to Betslip
        EXPECTED: * All selections are marked in green
        EXPECTED: * Bet counter increases by the added selections number
        EXPECTED: * Added selections are present in Betslip
        """
        pass
