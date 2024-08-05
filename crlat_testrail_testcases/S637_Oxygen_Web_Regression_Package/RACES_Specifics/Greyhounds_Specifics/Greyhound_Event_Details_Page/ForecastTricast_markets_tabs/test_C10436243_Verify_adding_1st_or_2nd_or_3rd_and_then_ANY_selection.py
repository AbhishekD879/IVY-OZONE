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
class Test_C10436243_Verify_adding_1st_or_2nd_or_3rd_and_then_ANY_selection(Common):
    """
    TR_ID: C10436243
    NAME: Verify adding 1st or 2nd or 3rd and then ANY selection
    DESCRIPTION: This test case verifies adding 1st or 2nd or 3rd and then ANY selection
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

    def test_002_click_1st_or_2nd_or_3rd_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st (or 2nd or 3rd) selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * Not selected buttons for this runner become disabled
        EXPECTED: * All other 1st (or 2nd or 3rd) buttons for all other runners become disabled
        EXPECTED: * ANY buttons for all other runners remain enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        pass

    def test_003_click_any_selection_button_for_any_other_racer(self):
        """
        DESCRIPTION: Click ANY selection button for any other racer
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * Previously selected button becomes deselected and disabled
        EXPECTED: * ALL 1st, 2nd and 3rd buttons become disabled
        EXPECTED: * ALL ANY buttons become enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        pass

    def test_004_click_any_buttons_for_2_more_runners(self):
        """
        DESCRIPTION: Click ANY buttons for 2 more runners
        EXPECTED: * Selected buttons is highlighted green
        EXPECTED: * ALL other butons become disabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        pass
