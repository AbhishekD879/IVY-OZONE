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
class Test_C2552913_Banach_Odd_Event_markets_with_switcher(Common):
    """
    TR_ID: C2552913
    NAME: Banach. Odd/Event markets with switcher
    DESCRIPTION: Test case verifies display and selection rule of markets Odd/Even markets having 2 alternative selections and switcher
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check such markets availability in Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: **Example of market**
    PRECONDITIONS: TOTAL GOALS ODD/EVEN
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True

    def test_001_expand__collapse_market_accordion_of_market_with_a_switcher_provided_in_the_pre_conditions(self):
        """
        DESCRIPTION: Expand / collapse market accordion of market with a switcher provided in the pre-conditions
        EXPECTED: - Accordion is expandable/collapsable
        EXPECTED: - Switchers "90 mins", "1st half", "2nd half" are present
        """
        pass

    def test_002_switch_between_90_mins_1st_half_2nd_half_tabs(self):
        """
        DESCRIPTION: Switch between "90 mins", "1st half", "2nd half" tabs
        EXPECTED: - Each switcher tab contains selections "Odd", "Even" as per **selections** request
        """
        pass

    def test_003_tap_on_the_first_selection_inside_90_mins_switcher(self):
        """
        DESCRIPTION: Tap on the first selection inside 90 mins switcher
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection has been added to the dashboard
        """
        pass

    def test_004_tap_on_the_second_selection_inside_90_mins_switcher(self):
        """
        DESCRIPTION: Tap on the second selection inside 90 mins switcher
        EXPECTED: 1 selection is dashboard:
        EXPECTED: - First selection is deselected inside accordion and removed from the dashboard
        EXPECTED: - Second selection is selected inside accordion and is in the dashboard
        """
        pass

    def test_005_switch_to_1st_half_tab_and_tap_on_the_first_selection(self):
        """
        DESCRIPTION: Switch to "1st half" tab and tap on the first selection
        EXPECTED: 2 selections in dashboard:
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection has been added to the dashboard
        """
        pass

    def test_006_tap_on_the_second_selection_inside_1st_half_tab(self):
        """
        DESCRIPTION: Tap on the second selection inside "1st half" tab
        EXPECTED: 2 selections in dashboard:
        EXPECTED: - First selection of "1st half" tab is deselected inside accordion and removed from the dashboard
        EXPECTED: - Second selection of "1st half" tab is selected inside accordion and is in the dashboard
        """
        pass
