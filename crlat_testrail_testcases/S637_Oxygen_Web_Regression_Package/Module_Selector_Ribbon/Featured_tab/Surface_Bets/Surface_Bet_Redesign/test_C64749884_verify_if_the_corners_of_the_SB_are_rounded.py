import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C64749884_verify_if_the_corners_of_the_SB_are_rounded(Common):
    """
    TR_ID: C64749884
    NAME: verify if the corners of the SB are rounded
    DESCRIPTION: Testcase verifies if the corners of the SB are rounded
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_create_a_new_surface_bet(self):
        """
        DESCRIPTION: Create a new surface bet.
        EXPECTED: User should see newly created SB in FE
        """
        pass

    def test_003_verify_the_surface_bet_shape_in_fe(self):
        """
        DESCRIPTION: Verify the Surface bet shape in FE
        EXPECTED: Corners of the SB should be rounded
        """
        pass
