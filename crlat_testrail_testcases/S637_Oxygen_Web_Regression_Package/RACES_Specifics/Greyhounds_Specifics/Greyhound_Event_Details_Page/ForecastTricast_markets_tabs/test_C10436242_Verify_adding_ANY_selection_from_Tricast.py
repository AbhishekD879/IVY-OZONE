import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10436242_Verify_adding_ANY_selection_from_Tricast(Common):
    """
    TR_ID: C10436242
    NAME: Verify adding ANY selection from Tricast
    DESCRIPTION: Tрis test case verifies adding ANY selection from Tricast
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def test_001_select_tricast_tab(self):
        """
        DESCRIPTION: Select Tricast tab
        EXPECTED: 
        """
        pass

    def test_002_click_any_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click ANY selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * ALL 1st, 2nd and 3rd buttons become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * 'Add to Betslip' button remains disabled
        """
        pass

    def test_003_click_any_selection_button_on_different_runner(self):
        """
        DESCRIPTION: Click ANY selection button on different runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * ALL 1st, 2nd and 3rd buttons remain disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * 'Add to Betslip' button remains disabled
        """
        pass

    def test_004_click_any_selection_button_on_different_runner(self):
        """
        DESCRIPTION: Click ANY selection button on different runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * ALL 1st, 2nd and 3rd buttons remain disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * 'Add to Betslip' button becomes enabled
        """
        pass
