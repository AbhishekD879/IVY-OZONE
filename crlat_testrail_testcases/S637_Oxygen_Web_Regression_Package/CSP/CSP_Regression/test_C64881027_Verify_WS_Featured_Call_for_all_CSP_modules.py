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
class Test_C64881027_Verify_WS_Featured_Call_for_all_CSP_modules(Common):
    """
    TR_ID: C64881027
    NAME: Verify WS-Featured Call for all CSP modules
    DESCRIPTION: This test case verifies Featured data call for all CSP modules
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_with_segmented_user_as_per_precondtion_inspect_the_screen_and_verify_calls_in_network_tab_in_ws(self):
        """
        DESCRIPTION: Login with segmented user as per precondtion, Inspect the screen and verify calls in network tab in WS
        EXPECTED: In WS,FEATURED_STRUCTURE_CHANGED call should received after 1 min and after refresh for Super button,Footer menu and MRT
        """
        pass

    def test_003_(self):
        """
        DESCRIPTION: 
        EXPECTED: In WS,FEATURED_STRUCTURE_CHANGED call should received without refresh for all remaining modules (Surfacebet,HC,QL,Featured module)
        """
        pass

    def test_004_verify_in_fe(self):
        """
        DESCRIPTION: Verify in FE
        EXPECTED: Once we received call,data should reflect in Homepage
        """
        pass
