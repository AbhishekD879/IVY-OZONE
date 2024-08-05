import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C9647727_Verify_blocking_of_access_to_GH_HR_for_In_play_page_widget(Common):
    """
    TR_ID: C9647727
    NAME: Verify blocking of access to GH & HR for In-play page/widget
    DESCRIPTION: This test case verifies that German user doesn't have access to Greyhound (GH) and Horse Racing (HR) in In-play tab/module
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile [C18745055]
    DESCRIPTION: Desktop [C20737723]
    PRECONDITIONS: * 'In-Play' module should be enabled in CMS > System configuration > Structure > In-Play module
    PRECONDITIONS: * 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: * Some positive value should to be set for 'In-Play Event Count' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: * 'In-Play' module configuration to display module in needed menus:
    PRECONDITIONS: CMS > Sport Pages > Sport Categories > Find 'In-Play' > General Sport Configuration > Check off needed areas (e.g., 'Show in Sports Ribbon') OR
    PRECONDITIONS: CMS > Menus > Create menu in Menu (e.g., Header Menus > Create Header Menu > Fill in 'Link Title' with ''In-Play'' and 'Target Uri' with 'in-play' > Save)
    PRECONDITIONS: * 'Show In Play' should be checked off for HR and GH, to show these sports events in In-play: CMS > Sports Pages > Sports Categories > Tap needed category (e.g., Horse Racing) > tap 'General Sport Configuration' > Tick 'Show In Play' check-box > Save changes (https://confluence.egalacoral.com/display/SPI/Sportsbook+Configuration+Guide)
    PRECONDITIONS: ____________
    PRECONDITIONS: * Ensure that there are GH and HR available for not German user in In-play page/widget.
    PRECONDITIONS: * German user is logged in
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
    PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True

    def test_001_open_in_play_pagemobiletablettap_in_play_icon_on_the_sports_menu_ribbon_on_the_homepagedesktopclick_in_play_icon_on_the_header_menussubheader_menus(self):
        """
        DESCRIPTION: Open 'In-Play' Page:
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon on the homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'In-Play' icon on the Header Menus/SubHeader Menus
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_002_mobiletabletopen_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'Upcoming' tab in 'In-Play' module
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_003_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage.
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * 'View all in-play [racing]' button is not displayed
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_004_mobiletabletfooter_menu__menu_item__tap_on_in_playor_sports_menu_ribbon__all_sports__in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Footer menu > 'Menu' item > Tap on 'In Play'
        DESCRIPTION: OR Sports Menu Ribbon > All sports > 'In Play'
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports except racing are available
        """
        pass
