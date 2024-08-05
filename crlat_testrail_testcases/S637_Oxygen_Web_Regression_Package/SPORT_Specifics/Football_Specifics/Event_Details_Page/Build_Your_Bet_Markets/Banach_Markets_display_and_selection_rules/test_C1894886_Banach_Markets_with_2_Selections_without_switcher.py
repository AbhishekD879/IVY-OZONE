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
class Test_C1894886_Banach_Markets_with_2_Selections_without_switcher(Common):
    """
    TR_ID: C1894886
    NAME: Banach. Markets with 2 Selections without switcher
    DESCRIPTION: Test case verifies display and selection rule of markets with 2 selections without switcher.
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Scope of markets with 2 selections without switcher. Select available for testing**
    PRECONDITIONS: RED CARD IN MATCH
    PRECONDITIONS: PARTICIPANT_1 (Home Team) RED CARD
    PRECONDITIONS: PARTICIPANT_2 (Away Team) RED CARD
    PRECONDITIONS: BOTH TEAMS TO SCORE
    PRECONDITIONS: TO WIN TO NIL
    PRECONDITIONS: TOTAL GOALS ODD/EVEN
    PRECONDITIONS: BOTH TEAMS TO SCORE IN BOTH HALVES
    PRECONDITIONS: BOTH TEAMS TO SCORE IN 1ST HALF
    PRECONDITIONS: BOTH TEAMS TO SCORE IN 2ND HALF
    PRECONDITIONS: TEAM TO SCORE IN BOTH HALVES
    PRECONDITIONS: WIN BOTH HALVES
    PRECONDITIONS: WIN EITHER HALF
    PRECONDITIONS: CLEAN SHEET
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes) tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True

    def test_001_expand__collapse_market_accordion_of_market_without_switcher_provided_in_the_pre_conditions(self):
        """
        DESCRIPTION: Expand / collapse market accordion of market without switcher provided in the pre-conditions
        EXPECTED: - Two selections are displayed as per request **selections** without switcher inside the market accordion
        EXPECTED: - Accordion is expandable
        """
        pass

    def test_002_tap_on_the_first_selection_inside_a_market(self):
        """
        DESCRIPTION: Tap on the first selection inside a market
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection has been added to the dashboard
        """
        pass

    def test_003_tap_on_the_second_selection_inside_a_market(self):
        """
        DESCRIPTION: Tap on the second selection inside a market
        EXPECTED: - Fist selection is deselected and removed from the dashboard
        EXPECTED: - Second selection is selected inside accordion and is in the dashboard
        """
        pass
