import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C44870178_Verify_navigations_of_A_Z_menu(Common):
    """
    TR_ID: C44870178
    NAME: Verify navigations of A-Z menu
    DESCRIPTION: This test case verifies functionality of 'A-Z' page which can be opened via footer menu and via pressing the button 'All Sports' on the Sport menu ribbon
    PRECONDITIONS: 1. Sports are configured in CMS : Sports Pages > Sports Categories
    PRECONDITIONS: 2. A-Z sports is configured in CMS for some sports (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 3. Application is Loaded
    """
    keep_browser_open = True

    def test_001_tap_on_all_sports_icon_on_sports_menu_ribbon__menu_icon_on_footer_menu_bar(self):
        """
        DESCRIPTION: Tap on 'All Sports' icon on Sports menu ribbon / 'Menu' icon on Footer Menu bar
        EXPECTED: 'All Sports' page is opened
        EXPECTED: Top Sports are listed in the first section followed by A-Z Sports
        """
        pass

    def test_002_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All sports' page tap on Back button
        EXPECTED: User should navigate back to the home page
        """
        pass

    def test_003_tap_on_any_menu_item__sport_from_top_section_or_a_z_sports_on_all_sports_page(self):
        """
        DESCRIPTION: Tap on any menu item / sport from top section or A-Z Sports on All Sports page
        EXPECTED: User should navigate to the corresponding Sports Landing Page.
        """
        pass

    def test_004_verify_a_z_sports(self):
        """
        DESCRIPTION: Verify A-Z Sports
        EXPECTED: Title is 'A-Z Sports'
        EXPECTED: Sports are displayed in a list view
        EXPECTED: There are Sport name and icon
        EXPECTED: Only Sports with the CMS setting 'Show in A-Z' are shown in this section
        """
        pass

    def test_005_verify_sports_ordering_under_a_z_sports(self):
        """
        DESCRIPTION: Verify sports ordering under A-Z Sports
        EXPECTED: All sports are shown in alphabetical A-Z order
        """
        pass
