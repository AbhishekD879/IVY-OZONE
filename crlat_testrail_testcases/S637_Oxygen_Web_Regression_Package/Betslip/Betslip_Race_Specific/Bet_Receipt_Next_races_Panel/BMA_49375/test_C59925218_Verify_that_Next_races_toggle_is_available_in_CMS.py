import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59925218_Verify_that_Next_races_toggle_is_available_in_CMS(Common):
    """
    TR_ID: C59925218
    NAME: Verify that Next races toggle is available in CMS
    DESCRIPTION: This test case verifies the display of Next races toggle in CMS and as CMS admin User - User can either enable or disable Next races Panel display in Bet receipt
    PRECONDITIONS: 1: User should have CMS admin access
    PRECONDITIONS: 2: Racing Post Tip should not be available and displayed
    PRECONDITIONS: Note: Racing post tip & Next Races should never be displayed at the same time.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin(self):
        """
        DESCRIPTION: Login to CMS as admin
        EXPECTED: User should be able to login successfully into CMS
        """
        pass

    def test_002_navigate_to_system_configuration_from_the_left_menu(self):
        """
        DESCRIPTION: Navigate to System Configuration from the left menu
        EXPECTED: User should be able to click on System configuration
        """
        pass

    def test_003_click_on_structure_and_search_for_next_races_toggle(self):
        """
        DESCRIPTION: Click on Structure and search for Next races toggle
        EXPECTED: Next races toggle should be displayed
        """
        pass

    def test_004_enable_next_races_and_save(self):
        """
        DESCRIPTION: Enable Next races and save
        EXPECTED: User should be able to save changes successfully
        """
        pass

    def test_005_validate_the_display_of_next_races_in_ladbrokes_coral(self):
        """
        DESCRIPTION: Validate the display of Next races in Ladbrokes /Coral
        EXPECTED: Next races Panel should be displayed
        """
        pass

    def test_006_disable_next_races_and_save(self):
        """
        DESCRIPTION: Disable Next races and save
        EXPECTED: User should be able to save changes successfully
        """
        pass

    def test_007_validate_the_display_of_next_races_in_ladbrokescoral(self):
        """
        DESCRIPTION: Validate the display of Next races in Ladbrokes/Coral
        EXPECTED: Next races panel should NOT be displayed
        """
        pass
