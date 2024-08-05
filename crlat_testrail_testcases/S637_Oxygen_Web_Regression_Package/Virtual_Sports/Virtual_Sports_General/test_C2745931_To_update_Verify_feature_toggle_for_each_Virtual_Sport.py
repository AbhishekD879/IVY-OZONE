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
class Test_C2745931_To_update_Verify_feature_toggle_for_each_Virtual_Sport(Common):
    """
    TR_ID: C2745931
    NAME: [To update] Verify feature toggle for each Virtual Sport
    DESCRIPTION: System Config is no longer used, this test case needs to be updated
    DESCRIPTION: This test case verifies Feature toggle work for each Virtual Sport
    PRECONDITIONS: 1. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 2. Log in to CMS
    PRECONDITIONS: 2. System config "Virtual Sports" is created in CMS > System Configuration > Config Tab
    PRECONDITIONS: 3. Virtual Sports are configured in TI.
    PRECONDITIONS: 4. List of Virtual Sports:
    PRECONDITIONS: 1. virtual-horse-racing
    PRECONDITIONS: 2. virtual-greyhounds
    PRECONDITIONS: 3. virtual-football
    PRECONDITIONS: 4. virtual-darts
    PRECONDITIONS: 5. virtual-boxing
    PRECONDITIONS: 6. virtual-motorsports
    PRECONDITIONS: 7. virtual-cycling
    PRECONDITIONS: 8. virtual-speedway
    PRECONDITIONS: 9. virtual-tennis
    PRECONDITIONS: 10. virtual-basketball
    PRECONDITIONS: 11. virtual-horse-racing-jumps
    PRECONDITIONS: 12. virtual-grand-national
    """
    keep_browser_open = True

    def test_001_go_to_cms__system_configuration__config_tabfind_virtual_sports_group(self):
        """
        DESCRIPTION: Go to CMS > System Configuration > 'Config' Tab
        DESCRIPTION: Find 'Virtual Sports' Group
        EXPECTED: * 'Config' tab > 'Virtual Sports' is opened
        EXPECTED: * 'Initial Data' checkbox is not selected by default near to 'VirtualSports' config
        EXPECTED: * The response contains 'The initialDataConfig: false'
        EXPECTED: ![](index.php?/attachments/get/107709282)
        """
        pass

    def test_002_switch_to_structure_tab__find_virtual_sportsenable_all_checkboxes_for_all_sports_and_save_changes(self):
        """
        DESCRIPTION: Switch to 'Structure' Tab > Find 'Virtual Sports'
        DESCRIPTION: Enable all checkboxes for all Sports and Save changes
        EXPECTED: Changes are saved > all checkboxes for all Sports are enabled
        EXPECTED: ![](index.php?/attachments/get/107709283)
        """
        pass

    def test_003_in_app_open_virtual_sports_page_and_verify_virtual_sports_displaying(self):
        """
        DESCRIPTION: In App: open Virtual Sports page and verify Virtual Sports displaying
        EXPECTED: * All Virtual Sports are displayed in ribbon
        EXPECTED: * User can open each Sport Page
        EXPECTED: * GET /{brand}/system-configurations/virtual-sports request is sent to CMS to retrieve config:
        EXPECTED: ![](index.php?/attachments/get/107709284)
        """
        pass

    def test_004_in_cms__system_configuration__structure_tab__virtual_sportsdisable_virtual_horse_racing_and_save_changes(self):
        """
        DESCRIPTION: In CMS > System Configuration > 'Structure' Tab > Virtual Sports
        DESCRIPTION: Disable virtual-horse-racing and Save Changes
        EXPECTED: Changes are saved > virtual-horse-racing is disabled
        EXPECTED: ![](index.php?/attachments/get/107709285)
        """
        pass

    def test_005_in_app_open_virtual_sports_page_and_verify_virtual_horse_racing_displaying(self):
        """
        DESCRIPTION: In App: open Virtual Sports page and verify Virtual Horse Racing displaying
        EXPECTED: * Virtual Horse Racing is NOT displayed in ribbon
        EXPECTED: * GET /{brand}/system-configurations/virtual-sports request is sent to CMS to retrieve config:
        EXPECTED: ![](index.php?/attachments/get/107709287)
        """
        pass

    def test_006_repeat_steps_4_5_for_all_other_virtual_sports_available2_virtual_greyhounds3_virtual_football4_virtual_darts5_virtual_boxing6_virtual_motorsports7_virtual_cycling8_virtual_speedway9_virtual_tennis10_virtual_basketball11_virtual_horse_racing_jumps12_virtual_grand_national(self):
        """
        DESCRIPTION: Repeat Steps 4-5 for all other Virtual Sports available:
        DESCRIPTION: 2. virtual-greyhounds
        DESCRIPTION: 3. virtual-football
        DESCRIPTION: 4. virtual-darts
        DESCRIPTION: 5. virtual-boxing
        DESCRIPTION: 6. virtual-motorsports
        DESCRIPTION: 7. virtual-cycling
        DESCRIPTION: 8. virtual-speedway
        DESCRIPTION: 9. virtual-tennis
        DESCRIPTION: 10. virtual-basketball
        DESCRIPTION: 11. virtual-horse-racing-jumps
        DESCRIPTION: 12. virtual-grand-national
        EXPECTED: * Virtual <Sport> is not displayed in ribbon
        EXPECTED: * GET /{brand}/system-configurations/virtual-sports request is sent to CMS to retrieve config
        """
        pass
