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
class Test_C1990085_Banach_Markets_with_1_switcher_90min_1st_2nd_Half_Multiple_Selections(Common):
    """
    TR_ID: C1990085
    NAME: Banach. Markets with 1 switcher (90min, 1st, 2nd Half) & Multiple Selections
    DESCRIPTION: This test case verifies the display and selection rule of markets with multiple selections and switcher (90min, 1st, 2nd Half)
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Scope of markets with multiple selections with switcher. Select available for testing**
    PRECONDITIONS: TOTAL GOALS
    PRECONDITIONS: PARTICIPANT_1 TOTAL GOALS
    PRECONDITIONS: PARTICIPANT_2 TOTAL GOALS
    PRECONDITIONS: TOTAL CORNERS
    PRECONDITIONS: PARTICIPANT_1 TOTAL CORNERS
    PRECONDITIONS: PARTICIPANT_2 TOTAL CORNERS
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet (Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True

    def test_001_expand__collapse_market_accordion_of_market_without_switcher_provided_in_the_pre_conditions(self):
        """
        DESCRIPTION: Expand / collapse market accordion of market without switcher provided in the pre-conditions
        EXPECTED: - Switcher is displayed having 3 tabs (90min, 1st, 2nd Half)
        EXPECTED: - '90 mins' selected by default
        """
        pass

    def test_002_switch_between_90min_1st_2nd_half_tabs(self):
        """
        DESCRIPTION: Switch between 90min, 1st, 2nd Half tabs
        EXPECTED: - Within each tab there are selections displayed in 2 columns as per **selections**  request e.g.:
        EXPECTED: Over 0.5 Goals / Under 0.5 Goals
        EXPECTED: Over 1.5 Goals / Under 1.5 Goals
        EXPECTED: - A maximum of 3 rows are displayed with the 'Show More' link in the footer when # of rows&gt;3
        """
        pass

    def test_003_on_the_90_mins_tab_tap_on_show_more_link_in_the_footer_if_selections_rowsgt3(self):
        """
        DESCRIPTION: On the #90 mins' tab tap on 'Show More' link in the footer if selections rows&gt;3
        EXPECTED: The full list of all available selections is displayed with a 'Show Less' link at the bottom of the list
        """
        pass

    def test_004_tap_show_less_link(self):
        """
        DESCRIPTION: Tap 'Show Less' link
        EXPECTED: A maximum of 3 rows are displayed again with the 'Show More' link in the footer.
        """
        pass

    def test_005_tap_on_1_selection_eg_over_15_goals_from_90_mins_switcher_tab(self):
        """
        DESCRIPTION: Tap on 1 selection (e.g. 'Over 1.5 Goals') from "90 mins" switcher tab
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection is added to the dashboard
        """
        pass

    def test_006_tap_on_2_selection_eg_over_25_goals_from_the_same_tab(self):
        """
        DESCRIPTION: Tap on 2 selection (e.g. 'Over 2.5 Goals') from the same tab
        EXPECTED: - Fist selection is deselected and removed from the dashboard
        EXPECTED: - Second selection is selected inside accordion and is in the dashboard
        """
        pass

    def test_007_switch_to_1st_half_tab_and_tap_on_selection(self):
        """
        DESCRIPTION: Switch to "1st half" tab and tap on selection
        EXPECTED: 2 selections is dashboard:
        EXPECTED: - Selection form "1st half" tab is highlighted inside accordion
        EXPECTED: - Selection "1st half" tab has been added to the dashboard
        """
        pass
