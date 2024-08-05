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
class Test_C1056014_Verify_Competitions_Details_page_for_Desktop(Common):
    """
    TR_ID: C1056014
    NAME: Verify Competitions Details page for Desktop
    DESCRIPTION: This test case verifies Competitions Details page for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page__gt_competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt; 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        pass

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_004_verify_the_competitions_page_on_desktop(self):
        """
        DESCRIPTION: Verify the 'Competitions' page on Desktop:
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'COMPETITION NAME' inscription next to the 'Back' ('&lt;') button
        EXPECTED: * 'Change Competition' selector at the right side of the Competition header
        EXPECTED: * Breadcrumbs trail below the Competitions header in the next format: 'Home' &gt; 'Football' &gt; 'Competitions' &gt; 'Type (Competition) name'
        EXPECTED: * 'Matches' and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default and events are shown
        EXPECTED: * 'Market selector' drop-down at the same row as switchers (at the right side of row)
        """
        pass

    def test_005_click_on_the_back_lt_button(self):
        """
        DESCRIPTION: Click on the 'Back' ('&lt;') button
        EXPECTED: User is taken to the 'Competitions' tab on the Football Landing page
        """
        pass

    def test_006_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Click on 'Change Competition selector'
        EXPECTED: * 'Change Competition selector' drop-down list of countries e.g. England, Scotland, Spain is opened
        EXPECTED: * Countries items inside 'Change Competition selector' drop-down list are expandable/collapsible
        """
        pass

    def test_007_click_on_any_country_in_change_competition_selector(self):
        """
        DESCRIPTION: Click on any country in 'Change Competition selector'
        EXPECTED: * List of Competitions is contained within expanded Country item in 'Change Competition selector' drop-down list
        """
        pass

    def test_008_click_on_market_selector(self):
        """
        DESCRIPTION: Click on 'Market Selector'
        EXPECTED: * 'Market Selector' drop-down list of markets is opened
        EXPECTED: * The following items are displayed in 'Market Selector' drop-down list:
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra Time Result
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win & Both Team to Score
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        """
        pass

    def test_009_navigate_between_the_matches_and_outrights_switchers(self):
        """
        DESCRIPTION: Navigate between the 'Matches' and 'Outrights' switchers
        EXPECTED: * User is able to navigate between the switchers
        EXPECTED: * Relevant information is shown in each case
        EXPECTED: * 'Market Selector' is displayed only if 'Matches' switcher is selected
        """
        pass

    def test_010_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * 'Market selector' is NOT sticky. It becomes hidden when scrolling the page down
        EXPECTED: * 'Change Competition selector' is NOT sticky. It becomes hidden when scrolling the page down
        """
        pass

    def test_011_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * 'Market selector' is NOT sticky. It becomes visible when scrolling the page up
        EXPECTED: * 'Change Competition selector' is NOT sticky. It becomes visible when scrolling the page up
        """
        pass
