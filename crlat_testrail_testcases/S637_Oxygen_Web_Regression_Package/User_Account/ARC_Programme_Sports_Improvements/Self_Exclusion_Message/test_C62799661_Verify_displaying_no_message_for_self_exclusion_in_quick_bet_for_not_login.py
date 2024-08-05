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
class Test_C62799661_Verify_displaying_no_message_for_self_exclusion_in_quick_bet_for_not_login(Common):
    """
    TR_ID: C62799661
    NAME: Verify displaying no message for self-exclusion in quick bet  for not login
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

    def test_002_navigate_to_any_sport_and_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Navigate to any sport and add selection to quick bet
        EXPECTED: Selection is added to quick bet,no message component should be displayed in quick bet
        """
        pass
