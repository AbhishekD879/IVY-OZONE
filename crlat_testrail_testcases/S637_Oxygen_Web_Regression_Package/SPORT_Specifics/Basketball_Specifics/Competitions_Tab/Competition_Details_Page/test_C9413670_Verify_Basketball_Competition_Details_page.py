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
class Test_C9413670_Verify_Basketball_Competition_Details_page(Common):
    """
    TR_ID: C9413670
    NAME: Verify Basketball Competition Details page
    DESCRIPTION: This test case verifies Basketball competition details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Basketball landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion
    PRECONDITIONS: Note! To have classes/types displayed on frontend, put class ID's in **'InitialClassIDs' and/or 'A-ZClassIDs' fields** in **CMS>SystemConfiguration>Competitions Basketball**. Events for those classes should be present as well.
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
        EXPECTED: **Mobile/Tablet:**
        EXPECTED: * 'COMPETITIONS' label next to the 'back' ('&lt;') button
        EXPECTED: * Competition header with competition name and 'Change Competition' selector
        EXPECTED: * 'Matches' and 'Outrights' switchers (displayed only when there are both matches and outrights for selected type)
        EXPECTED: * 'Matches' switcher is selected by default and events from the league are shown
        EXPECTED: **Desktop:**
        EXPECTED: * Competition (type) name next to the 'Back' ('&lt;') button
        EXPECTED: * 'Change Competition' selector at the right side of the Competition header
        EXPECTED: * Breadcrumbs trail below the Competitions header in the next format: 'Home' &gt; 'Basketball' &gt; 'Competitions' &gt; 'Type (Competition) name'
        EXPECTED: * 'Matches' and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default and events are shown
        """
        pass

    def test_003_navigate_between_switchers(self):
        """
        DESCRIPTION: Navigate between switchers
        EXPECTED: * User is able to navigate between switchers
        EXPECTED: * Relevant information is shown in each case
        """
        pass

    def test_004_tap_the_back_lt_button(self):
        """
        DESCRIPTION: Tap the back ('&lt;') button
        EXPECTED: User is taken to the 'Competitions' tab on the Basketball Landing page
        """
        pass

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: User is taken to the selected competition details page
        """
        pass

    def test_006_on_matches_switcher_click_on_any_event_card(self):
        """
        DESCRIPTION: On 'Matches' switcher click on any event card
        EXPECTED: Respective event details page opens
        """
        pass

    def test_007_for_mobiletabletclick_lt_back_button_and_click_on_any_outright_event_on_outrights_switcher(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Click '&lt;' Back button and click on any outright event on 'Outrights' switcher
        EXPECTED: Respective Outright event details page opens
        """
        pass
