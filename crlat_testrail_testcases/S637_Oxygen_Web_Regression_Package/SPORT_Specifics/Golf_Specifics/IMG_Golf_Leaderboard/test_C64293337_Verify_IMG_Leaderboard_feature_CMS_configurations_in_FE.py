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
class Test_C64293337_Verify_IMG_Leaderboard_feature_CMS_configurations_in_FE(Common):
    """
    TR_ID: C64293337
    NAME: Verify IMG Leaderboard feature CMS configurations in FE
    DESCRIPTION: This tc verifies IMG LB CMS configurations in FE
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User logged in.
    PRECONDITIONS: 5. Navigate to GOLF inplay event with IMG LB
    """
    keep_browser_open = True

    def test_001_enable_lb_toggle_in_the_cms(self):
        """
        DESCRIPTION: Enable LB toggle in the CMS.
        EXPECTED: LB should be is displayed in the FE.
        """
        pass

    def test_002_disable_lb_toggle_in_the_cms(self):
        """
        DESCRIPTION: Disable LB toggle in the CMS.
        EXPECTED: LB is not displayed in the FE.
        """
        pass
