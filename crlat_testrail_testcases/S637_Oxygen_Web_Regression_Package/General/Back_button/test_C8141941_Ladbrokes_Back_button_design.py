import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C8141941_Ladbrokes_Back_button_design(Common):
    """
    TR_ID: C8141941
    NAME: [Ladbrokes] Back button design
    DESCRIPTION: This test case verifies redesign of back button for Ladbrokes brand
    PRECONDITIONS: You should be on any landing or event details page
    """
    keep_browser_open = True

    def test_001_verify_back_redesign(self):
        """
        DESCRIPTION: Verify "Back" redesign
        EXPECTED: - "Back" button is moved to header
        EXPECTED: - It has "<" arrow and "Back" label
        """
        pass
