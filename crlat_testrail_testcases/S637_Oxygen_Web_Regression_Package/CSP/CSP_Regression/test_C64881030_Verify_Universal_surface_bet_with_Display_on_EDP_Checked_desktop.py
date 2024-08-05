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
class Test_C64881030_Verify_Universal_surface_bet_with_Display_on_EDP_Checked_desktop(Common):
    """
    TR_ID: C64881030
    NAME: Verify Universal surface bet with â€˜Display on EDPâ€™ Checked (desktop)
    DESCRIPTION: This test case verifies Universal surface bet with â€˜Display on EDPâ€™ (desktop)
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page>Surfacebet
    PRECONDITIONS: 2.Create universal Surfacebet record with Event ID and 'Display in EDP' checked
    PRECONDITIONS: 3..Create Segmented Surfacebet record with Event ID and 'Display in EDP' checked
    PRECONDITIONS: (User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_before_loginverify_surfacebet_in_home_page_which_is_created_as_per_preconditions_2(self):
        """
        DESCRIPTION: (Before login)Verify Surfacebet in Home Page which is created as per preconditions 2
        EXPECTED: Surfacebet should display in home page
        """
        pass

    def test_003_navigate_to_edp_for_surface_bet_configured_event(self):
        """
        DESCRIPTION: Navigate to EDP for surface bet configured event
        EXPECTED: Universal surface bet should display in EDP for desktop
        """
        pass

    def test_004_after_loginverify_surfacebet_in_home_page_which_is_created_as_per_preconditions_2(self):
        """
        DESCRIPTION: (After login)Verify Surfacebet in Home Page which is created as per preconditions 2
        EXPECTED: Surfacebet should display in home page
        """
        pass

    def test_005_navigate_to_edp_for_surface_bet_configured_event(self):
        """
        DESCRIPTION: Navigate to EDP for surface bet configured event
        EXPECTED: Universal surface bet should display in EDP for desktop
        """
        pass

    def test_006_login_with_segemented_user__verify_surfacebet_in_home_page_which_is_created_as_per_preconditions_3(self):
        """
        DESCRIPTION: (Login with segemented user ) Verify Surfacebet in Home Page which is created as per preconditions 3
        EXPECTED: Segmented surface bet should not display in EDP ,as CSP implementation is not applicable for EDP.
        """
        pass
