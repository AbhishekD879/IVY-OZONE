import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732076_Verify_quiz_transition_from_Live_to_Previous(Common):
    """
    TR_ID: C57732076
    NAME: Verify quiz transition from Live to Previous
    DESCRIPTION: This test case verifies quiz transition from Live to Previous
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user is played Live quiz
    """
    keep_browser_open = True

    def test_001___open_cmsconfigure_live_game_with__display_to_date_in_past__save_changes(self):
        """
        DESCRIPTION: - Open CMS
        DESCRIPTION: Configure Live game with:
        DESCRIPTION: - Display To Date **in past**
        DESCRIPTION: - Save changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002___open_correct_4__tap_on_previous_tab(self):
        """
        DESCRIPTION: - Open Correct 4
        DESCRIPTION: - Tap on Previous Tab
        EXPECTED: - Previous Tab succssefuly opened
        EXPECTED: - Live quiz now displayed on the Previous Tab with correct information
        """
        pass
