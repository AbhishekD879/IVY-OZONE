import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62799659_Verify_displaying_no_message_self_exclusion_in_betslip_for_not_login(Common):
    """
    TR_ID: C62799659
    NAME: Verify displaying no message self-exclusion in betslip  for not login
    DESCRIPTION: This test case verifies no Self exclusion message
    PRECONDITIONS: No User should be logged in to application
    """
    keep_browser_open = True

    def test_001_navigate_to_application(self):
        """
        DESCRIPTION: Navigate to application
        EXPECTED: No user is logged in
        """
        pass

    def test_002_navigate_to_any_sport_and_add_selection_to_betslip(self):
        """
        DESCRIPTION: Navigate to any sport and add selection to betslip
        EXPECTED: Selection is added to betslip ,no message component should be displayed in betslip
        """
        pass
