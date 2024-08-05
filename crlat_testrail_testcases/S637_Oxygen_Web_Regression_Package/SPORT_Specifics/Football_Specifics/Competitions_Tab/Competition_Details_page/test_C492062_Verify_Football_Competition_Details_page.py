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
class Test_C492062_Verify_Football_Competition_Details_page(Common):
    """
    TR_ID: C492062
    NAME: Verify Football Competition Details page
    DESCRIPTION: This test case verifies Football competitions details page
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile: C33082825
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion and click on any type
    PRECONDITIONS: Note! To have classes/types displayed on frontend, put class ID's in **'InitialClassIDs' and/or 'A-ZClassIDs' fields** in **CMS>SystemConfiguration>Competitions Football**. Events for those classes should be present as well.
    PRECONDITIONS: Events data on Competition Details page is received with EventToOutcomeForType request to SS which should include only markets listed in request:
    PRECONDITIONS: For example: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForType/500?simpleFilter=event.eventSortCode:notIntersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=market.templateMarketName:intersects:|Match%20Betting|,|Over/Under%20Total%20Goals|,|Both%20Teams%20to%20Score|,|To%20Qualify|,|Draw%20No%20Bet|,|First-Half%20Result|,|Next%20Team%20to%20Score|,|Extra-Time%20Result|,Match%20Betting,Over/Under%20Total%20Goals,Both%20Teams%20to%20Score,To%20Qualify,Draw%20No%20Bet,First-Half%20Result,Next%20Team%20to%20Score,Extra-Time%20Result,Match%20Result%20and%20Both%20Teams%20To%20Score,|Match%20Result%20and%20Both%20Teams%20To%20Score|&translationLang=en&responseFormat=json&prune=event&prune=market&childCount=event
    """
    keep_browser_open = True

    def test_001_select_any_competition_type_within_expanded_class(self):
        """
        DESCRIPTION: Select any competition (type) within expanded class
        EXPECTED: Competition details page is opened
        """
        pass

    def test_002_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'COMPETITIONS' label next to the 'back' ('<') button (Coral only)
        EXPECTED: * 'Favorites' (star) icon (top right corner) (Coral only)
        EXPECTED: * Competition header with competition name and 'Change Competition' selector
        EXPECTED: * 3 tabs: 'Matches', 'Outrights', 'Results' (displayed only if at least two of them have content)
        EXPECTED: * Market selector drop-down
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
        EXPECTED: User is taken to the 'Competitions' tab on the Football Landing page
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
        EXPECTED: * Competition header, 'Change Competition' selector and Market selector are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches', 'Results' and 'Outrights' switcher are hidden (if available)
        """
        pass

    def test_007_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * Competition header, 'Change Competition' selector and Market selector are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches', 'Results' and 'Outrights' switchers are hidden (if available)
        EXPECTED: * After the page is scrolled all the way up, user sees switchers
        """
        pass

    def test_008_scroll_the_page_down_and_click_on_market_selector(self):
        """
        DESCRIPTION: Scroll the page down and click on Market selector
        EXPECTED: Market selector is clickable and displays available markets
        """
        pass

    def test_009_scroll_the_page_down_and_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Scroll the page down and click on 'Change Competition' selector
        EXPECTED: 'Change Competition' selector is clickable and displays available competitions
        """
        pass
