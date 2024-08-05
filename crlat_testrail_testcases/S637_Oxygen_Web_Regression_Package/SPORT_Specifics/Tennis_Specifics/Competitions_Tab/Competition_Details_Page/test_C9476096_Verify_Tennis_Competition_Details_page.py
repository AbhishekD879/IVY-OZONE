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
class Test_C9476096_Verify_Tennis_Competition_Details_page(Common):
    """
    TR_ID: C9476096
    NAME: Verify Tennis Competition Details page
    DESCRIPTION: This test case verifies Tennis competitions details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tennis landing page > Competitions tab
    """
    keep_browser_open = True

    def test_001_select_any_type_eg_wimbledon___mens_single(self):
        """
        DESCRIPTION: Select any type e.g. Wimbledon - Men's Single
        EXPECTED: Competition details page is opened
        """
        pass

    def test_002_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'COMPETITIONS' label next to the 'back' ('<') button
        EXPECTED: * Competition header with competition name and 'Change Competition' selector
        EXPECTED: * 2 tabs: 'Matches', 'Outrights'
        EXPECTED: * 'Matches' tab is selected by default and events from the league are shown
        """
        pass

    def test_003_navigate_between_the_tabs(self):
        """
        DESCRIPTION: Navigate between the tabs
        EXPECTED: * User is able to navigate between the tabs
        EXPECTED: * Relevant information is shown in each case
        """
        pass

    def test_004_tap_the_back__button(self):
        """
        DESCRIPTION: Tap the back ('<') button
        EXPECTED: User is taken to the 'Competitions' tab on the Tennis Landing page
        """
        pass

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: User is taken to the selected competition details page
        """
        pass

    def test_006_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Competition header and 'Change Competition' selector are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches' and 'Outrights' switcher are hidden
        """
        pass

    def test_007_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * Competition header and 'Change Competition' selector  are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches' and 'Outrights' switchers are hidden
        EXPECTED: * After the page is scrolled all the way up, user sees switchers
        """
        pass

    def test_008_scroll_the_page_down_and_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Scroll the page down and click on 'Change Competition' selector
        EXPECTED: 'Change Competition' selector is clickable and displays available competitions
        """
        pass
