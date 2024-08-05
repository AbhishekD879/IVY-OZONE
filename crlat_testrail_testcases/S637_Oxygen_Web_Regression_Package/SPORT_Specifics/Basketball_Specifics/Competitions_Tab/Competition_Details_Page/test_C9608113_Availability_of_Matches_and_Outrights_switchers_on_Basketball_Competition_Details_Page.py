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
class Test_C9608113_Availability_of_Matches_and_Outrights_switchers_on_Basketball_Competition_Details_Page(Common):
    """
    TR_ID: C9608113
    NAME: Availability of 'Matches' and 'Outrights' switchers on Basketball Competition Details Page
    DESCRIPTION: This test case verify cases when 'Matches' and 'Outrights' switchers are shown or hidden on Basketball Competition Details Page
    PRECONDITIONS: 3 different Basketball types should be configured in the following way:
    PRECONDITIONS: 1 type - has both matches ad outright events
    PRECONDITIONS: 2 type - has only matches
    PRECONDITIONS: 3 type - has only outrights
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Basketball landing page > Competitions tab
    PRECONDITIONS: 3. Expand class accordion under test
    """
    keep_browser_open = True

    def test_001_tap_on_1st_type_under_test_see_preconditions(self):
        """
        DESCRIPTION: Tap on 1st type under test (see preconditions)
        EXPECTED: * Respective Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed
        EXPECTED: * 'Matches' is selected by default
        """
        pass

    def test_002_tap_on_change_competition_selector_and_select_2nd_type_under_test(self):
        """
        DESCRIPTION: Tap on 'Change Competition' selector and select 2nd type under test
        EXPECTED: * Respective Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are hidden
        EXPECTED: * Events are shown
        """
        pass

    def test_003_tap_on_change_competition_selector_and_select_3rd_type_under_test(self):
        """
        DESCRIPTION: Tap on 'Change Competition' selector and select 3rd type under test
        EXPECTED: * Respective Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are hidden
        EXPECTED: * Outright events are shown
        """
        pass
