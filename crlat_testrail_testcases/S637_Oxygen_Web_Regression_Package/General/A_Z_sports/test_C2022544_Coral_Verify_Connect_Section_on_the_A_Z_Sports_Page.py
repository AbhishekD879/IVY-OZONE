import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2022544_Coral_Verify_Connect_Section_on_the_A_Z_Sports_Page(Common):
    """
    TR_ID: C2022544
    NAME: Coral. Verify 'Connect' Section on the 'A-Z' Sports Page
    DESCRIPTION: This test case verifies 'Сonnect' section availability on the 'A-Z' page after opening via footer menu and via pressing the button 'A - Z' on the Sports menu ribbon
    DESCRIPTION: AUTOTEST: [C2694498]
    PRECONDITIONS: Make sure Connect section in A-Z is turned on in CMS:
    PRECONDITIONS: System configuration -> Connect -> menu
    PRECONDITIONS: A user can be logged in/logged out
    PRECONDITIONS: CMS:
    PRECONDITIONS: https://CMS_ENDPOINT -> Chose 'sportsbook' channel -> 'Menus' -> 'Connect Menus'
    PRECONDITIONS: multi channel user: bluerabbit/ password
    PRECONDITIONS: in-shop user: 5000000000992144/ 1234
    """
    keep_browser_open = True

    def test_001_load_sportsbook_application_and_tap_a_z_all_sports_button_on_the_footer_menu(self):
        """
        DESCRIPTION: Load sportsbook application and tap 'A-Z All Sports' button on the footer menu
        EXPECTED: 'A-Z' Sports page is shown
        """
        pass

    def test_002_scroll_down_the_list_of_sports_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Scroll down the list of sports to the bottom of the page
        EXPECTED: * There is the section 'Connect' at the bottom of the page
        EXPECTED: * The name of the section is 'Connect'
        EXPECTED: * Section contains list of items (that corresponds to CMS configurations) (one exception: 'User connect online' item is shown only for Logged in In-Shop user)
        """
        pass

    def test_003_tap_every_icon_from_connect_section_use_connect_online_shop_exclusive_promos_shop_bet_tracker_football_bet_filter_saved_bet_filter_shop_locator(self):
        """
        DESCRIPTION: Tap every icon from 'Connect' section ('Use Connect Online', 'Shop Exclusive Promos', 'Shop Bet Tracker', 'Football Bet Filter', 'Saved Bet Filter', 'Shop Locator')
        EXPECTED: User is redirected to the appropriate page every time
        """
        pass

    def test_004_verify_connect_sections_items_ordering(self):
        """
        DESCRIPTION: Verify 'Connect' section's items ordering
        EXPECTED: 'Connect' section's items are ordered as configured in CMS:
        EXPECTED: Menu -> Connect menu
        EXPECTED: (configurations made by dragging)
        """
        pass
