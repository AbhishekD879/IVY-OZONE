import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2513212_Verify_Toggling_of_Connect_section_in_menus(Common):
    """
    TR_ID: C2513212
    NAME: Verify Toggling of 'Connect' section in menus
    DESCRIPTION: This test case verify that section 'Connect' in A-Z/Right menu and on Connect landing page can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> menu
    DESCRIPTION: 'Connect' Section contains List of Connect features which are CMS configurable:
    DESCRIPTION: CMS -> Menus -> Connect Menu
    PRECONDITIONS: 1. Load CMS and make sure 'Connect' section in menus is turned off: System configuration -> Connect -> menu = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in
    """
    keep_browser_open = True

    def test_001__from_the_header_ribbon_select_all_sports_verify_connect_section_presence_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section presence at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Connect' section is absent
        """
        pass

    def test_002__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * List of Connect features is empty
        """
        pass

    def test_003__load_cms_turn_menu_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'menu' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_004__from_the_header_ribbon_select_all_sports_verify_connect_section_presence_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section presence at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Connect' section is displayed at the bottom
        """
        pass

    def test_005__from_the_header_ribbon_select_connect_verify__list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify  list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * List of Connect features is displayed
        """
        pass
