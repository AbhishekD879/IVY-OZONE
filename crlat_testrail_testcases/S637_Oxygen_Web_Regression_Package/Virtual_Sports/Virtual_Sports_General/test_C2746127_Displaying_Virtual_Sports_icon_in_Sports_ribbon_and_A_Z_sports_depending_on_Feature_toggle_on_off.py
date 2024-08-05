import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C2746127_Displaying_Virtual_Sports_icon_in_Sports_ribbon_and_A_Z_sports_depending_on_Feature_toggle_on_off(Common):
    """
    TR_ID: C2746127
    NAME: Displaying Virtual Sports icon in Sports ribbon and A-Z sports depending on Feature toggle on/off
    DESCRIPTION: This test case verifies Virtual Sports icon displaying in Sports ribbon and A-Z sports depending on Feature toggle on/off
    PRECONDITIONS: 1. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 2. System config "Virtual Sports" created in CMS > System Configuration. All checkboxes are enabled.
    PRECONDITIONS: 3. Virtual Sports are configured in TI.
    """
    keep_browser_open = True

    def test_001_go_to_apps_homepage_and_verify_virtual_sports_icon_in_sports_ribbon(self):
        """
        DESCRIPTION: Go to apps Homepage and verify Virtual Sports icon in Sports ribbon
        EXPECTED: Virtual Sports icon is displayed in Sports Ribbon
        """
        pass

    def test_002_navigate_to_all_sports__a_z_section_and_virtual_sports_in_the_list(self):
        """
        DESCRIPTION: Navigate to All Sports > A-Z section and Virtual Sports in the list
        EXPECTED: Virtual Sports is in the list of available sports
        """
        pass

    def test_003_go_to_cms__system_configuration__virtual_sports_and_disable_all_checkboxes_inn_this_config_save_changes(self):
        """
        DESCRIPTION: Go to CMS > System Configuration > Virtual Sports and disable all checkboxes inn this config. Save changes.
        EXPECTED: 
        """
        pass

    def test_004_go_to_apps_homepage_and_verify_virtual_sports_icon_in_sports_ribbon(self):
        """
        DESCRIPTION: Go to apps Homepage and verify Virtual Sports icon in Sports ribbon
        EXPECTED: Virtual Sports icon is displayed in Sports Ribbon
        """
        pass

    def test_005_tap_on_virtual_sports_icon_in_sports_ribbon(self):
        """
        DESCRIPTION: Tap on Virtual Sports icon in Sports ribbon
        EXPECTED: "Sorry no Virtual Sports events are available at this time" message is shown
        """
        pass

    def test_006_navigate_to_all_sports__a_z_section_and_check_virtual_sports_in_the_list(self):
        """
        DESCRIPTION: Navigate to All Sports > A-Z section and check Virtual Sports in the list
        EXPECTED: Virtual Sports is displayed in the list of available sports
        """
        pass

    def test_007_tap_on_virtual_sports_icon_in_a_z_section(self):
        """
        DESCRIPTION: Tap on Virtual Sports icon in A-Z section
        EXPECTED: "Sorry no Virtual Sports events are available at this time" message is shown
        """
        pass
