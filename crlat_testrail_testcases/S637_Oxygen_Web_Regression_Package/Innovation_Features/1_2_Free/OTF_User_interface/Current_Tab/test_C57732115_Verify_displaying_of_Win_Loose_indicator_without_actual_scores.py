import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732115_Verify_displaying_of_Win_Loose_indicator_without_actual_scores(Common):
    """
    TR_ID: C57732115
    NAME: Verify displaying of Win/Loose indicator without actual scores
    DESCRIPTION: This test case verifies displaying of Win/Loose indicator without actual scores
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. Game with any actual scores exist (event isn't resulted yet)
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: 'Loose'/'Win' indicators NOT displayed
        """
        pass
