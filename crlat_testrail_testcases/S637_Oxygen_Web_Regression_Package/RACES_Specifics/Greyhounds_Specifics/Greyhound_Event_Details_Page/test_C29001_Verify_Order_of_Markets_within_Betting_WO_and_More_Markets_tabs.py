import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C29001_Verify_Order_of_Markets_within_Betting_WO_and_More_Markets_tabs(Common):
    """
    TR_ID: C29001
    NAME: Verify Order of Markets within 'Betting WO' and 'More Markets' tabs
    DESCRIPTION: This test case verifies order of markets within 'Betting WO' and 'More Markets' tabs
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 - Racecard Layout Update - Markets and Selections area
    PRECONDITIONS: Make sure that there are more than one market within 'Betting WO' and 'More Markets' tabs
    PRECONDITIONS: To retrieve an information from Site Server use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: See attributes:
    PRECONDITIONS: 'displayOrder' attribute in market level to define market order
    PRECONDITIONS: 'name' attribute in the market level to see market name
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_tap_betting_wo_tab(self):
        """
        DESCRIPTION: Tap 'Betting WO' tab
        EXPECTED: 'Betting WO' tab is selected and highlighted
        EXPECTED: The list of all available markets is shown
        """
        pass

    def test_005_verify_order_of_markets(self):
        """
        DESCRIPTION: Verify order of markets
        EXPECTED: Markets are ordered by:
        EXPECTED: *   **'displayOrder'** in ascending - in the first instance​
        EXPECTED: *   **'name'** - if displayOrder attribute is the same
        """
        pass

    def test_006_tap_more_markets_tab(self):
        """
        DESCRIPTION: Tap 'More Markets' tab
        EXPECTED: 'More Markets' tab is selected and highlighted
        EXPECTED: The list of all available markets is shown
        """
        pass

    def test_007_verify_order_of_markets(self):
        """
        DESCRIPTION: Verify order of markets
        EXPECTED: Markets are ordered by:
        EXPECTED: *   **'displayOrder'** in ascending - in the first instance​
        EXPECTED: *   **'name'** - if displayOrder attribute is the same
        """
        pass
