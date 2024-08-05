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
class Test_C62851776_Verify_GA_tracking_capturing_all_user_interaction_as_part_of_ARC(Common):
    """
    TR_ID: C62851776
    NAME: Verify  GA tracking capturing all user interaction as part of ARC
    DESCRIPTION: This test case verifies the GA tracking for messaging
    PRECONDITIONS: User is logged FE
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral
        EXPECTED: User should be able to launch the application successfully
        """
        pass
