import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C659006_CMS_configuration_of_Quick_Bet_functionality(Common):
    """
    TR_ID: C659006
    NAME: CMS configuration of Quick Bet functionality
    DESCRIPTION: This test case verifies CMS configuration of Quick Bet functionality
    PRECONDITIONS: 1. To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_system_configuration_section___quickbet_item___notifications_option(self):
        """
        DESCRIPTION: Go to 'System Configuration' section -> 'QUICKBET' item -> 'Notifications' option
        EXPECTED: 
        """
        pass

    def test_003_select_notifications_option_and_save_changes(self):
        """
        DESCRIPTION: Select 'Notifications' option and save changes
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'Quick Bet' functionality is enabled within Oxygen app
        """
        pass

    def test_004_load_oxygen_app_and_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Load Oxygen app and add one selection to Betslip
        EXPECTED: 'Quick Bet' section is displayed at the bottom of page
        """
        pass

    def test_005_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip
        EXPECTED: 'Quick Bet' section is not displayed anymore
        """
        pass

    def test_006_login_and_repeat_steps_4_5(self):
        """
        DESCRIPTION: Login and repeat steps #4-5
        EXPECTED: 
        """
        pass

    def test_007_go_to_right_menu___setting_item(self):
        """
        DESCRIPTION: Go to Right Menu -> 'Setting' item
        EXPECTED: * 'Preferences' page is displayed
        EXPECTED: * 'Allow Quick Bet' option is displayed within 'Preferences' page
        """
        pass

    def test_008_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_3_but_on_step_3_deselect_notifications_option(self):
        """
        DESCRIPTION: Repeat steps #1-3, but on step #3 deselect 'Notifications' option
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'Quick Bet' functionality is disabled within Oxygen app
        """
        pass

    def test_010_go_to_oxygen_app_and_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Go to Oxygen app and add one selection to Betslip
        EXPECTED: Quick Bet is NOT displayed at the bottom of page
        """
        pass

    def test_011_login_and_repeat_step_10(self):
        """
        DESCRIPTION: Login and repeat step #10
        EXPECTED: 
        """
        pass

    def test_012_go_to_right_menu___setting_option(self):
        """
        DESCRIPTION: Go to Right Menu -> 'Setting' option
        EXPECTED: * 'Preferences' page is displayed
        EXPECTED: * 'Allow Quick Bet' option is NOT displayed within 'Preferences' page
        """
        pass
