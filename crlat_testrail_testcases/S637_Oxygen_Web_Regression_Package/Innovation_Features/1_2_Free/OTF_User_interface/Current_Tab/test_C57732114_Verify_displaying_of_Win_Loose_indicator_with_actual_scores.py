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
class Test_C57732114_Verify_displaying_of_Win_Loose_indicator_with_actual_scores(Common):
    """
    TR_ID: C57732114
    NAME: Verify displaying of Win/Loose indicator with actual scores
    DESCRIPTION: This test case verifies displaying of Win/Loose indicator with actual scores
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User set prediction for game previously
    PRECONDITIONS: 2. One of matches finished with Win/Loose result
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Loose'/'Win' indicators displayed for finished match
        EXPECTED: - Not finished matches NOT displayed 'Loose'/'Win' indicators
        """
        pass

    def test_002_wait_till_second_match_finished(self):
        """
        DESCRIPTION: Wait till **second** match finished
        EXPECTED: - 'Loose'/'Win' indicators displayed for **second** finished match
        EXPECTED: - Not finished matches NOT displayed 'Loose'/'Win' indicators
        """
        pass

    def test_003_wait_till_third_match_finished(self):
        """
        DESCRIPTION: Wait till **third** match finished
        EXPECTED: - 'Loose'/'Win' indicators displayed for **third** finished match
        EXPECTED: - Not finished matches NOT displayed 'Loose'/'Win' indicators
        """
        pass
