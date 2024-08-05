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
class Test_C64749875_Verify_if_the_user_able_to_remove_the_BG_image_from_the_SB_when_its_active(Common):
    """
    TR_ID: C64749875
    NAME: Verify if the user able to remove the BG 
image from the SB when its active
    DESCRIPTION: Testcase verifies if user is able to remove the BG image from SB
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

    def test_002_go_to_particular_surfacebet_and_remove_uploaded_background_image_in_cms_for_the_active_surface_bet_and_verify_the_surface_bet_in_fe(self):
        """
        DESCRIPTION: Go to particular surfacebet and remove uploaded background image in CMS for the active surface Bet and verify the surface bet in FE.
        EXPECTED: Background image should be removed successfully and should not be shown in FE
        """
        pass
