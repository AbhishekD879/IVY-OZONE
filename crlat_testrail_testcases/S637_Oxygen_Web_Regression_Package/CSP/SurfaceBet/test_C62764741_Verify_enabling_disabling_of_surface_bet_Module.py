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
class Test_C62764741_Verify_enabling_disabling_of_surface_bet_Module(Common):
    """
    TR_ID: C62764741
    NAME: Verify enabling/disabling of 'surface bet' Module
    DESCRIPTION: This test case verifies enabling/disabling of "surface bet" Module on Home page/SLP via CMS, If we disable one surface bet next available surface bet should display
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
    PRECONDITIONS: Configure multiple surface bets with different publish dates
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___surface_bet_section___open_existing_surface_bet(self):
        """
        DESCRIPTION: Go to Sports Pages -> surface bet section -> open existing surface bet
        EXPECTED: surface bet details page is opened
        """
        pass

    def test_003_validate_the_user_is_able_to_enabledisable_and_save_the_changes_successfully(self):
        """
        DESCRIPTION: Validate the User is able to enable/disable and save the changes successfully.
        EXPECTED: User should be able to enable/ disable the check box.
        """
        pass

    def test_004_set_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Set 'Active' checkbox and save changes
        EXPECTED: a)Existing surface bet is active
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_006_load_oxygen_app_and_verify_surface_bet_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify surface bet displaying
        EXPECTED: surface bet is displayed on Front End
        """
        pass

    def test_007_go_back_to_the_same_surface_bet_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same surface bet, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing surface bet is inactive
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_009_load_oxygen_app_and_verify_surface_bet_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify surface bet displaying
        EXPECTED: a) surface bet is NOT displayed on Front End
        """
        pass

    def test_010_(self):
        """
        DESCRIPTION: 
        EXPECTED: b) If we have other surface bet with valid date it should display
        """
        pass
