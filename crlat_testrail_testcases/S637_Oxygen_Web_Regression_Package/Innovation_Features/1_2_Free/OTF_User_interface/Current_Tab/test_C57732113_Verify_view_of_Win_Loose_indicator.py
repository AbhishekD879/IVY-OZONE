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
class Test_C57732113_Verify_view_of_Win_Loose_indicator(Common):
    """
    TR_ID: C57732113
    NAME: Verify view of Win/Loose indicator
    DESCRIPTION: This test case verifies displaying of Win/Loose indicator
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. Game with Win and Loose events exist
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Win' indicator displayed for Win events
        EXPECTED: - 'Loose' indicator displayed for Loosed events
        EXPECTED: - 'Win' string and scores has a **Green** color
        EXPECTED: - 'Loose' string and scores has a **Red** color
        EXPECTED: Styled according to screenshot:
        EXPECTED: ![](index.php?/attachments/get/26466)
        """
        pass
