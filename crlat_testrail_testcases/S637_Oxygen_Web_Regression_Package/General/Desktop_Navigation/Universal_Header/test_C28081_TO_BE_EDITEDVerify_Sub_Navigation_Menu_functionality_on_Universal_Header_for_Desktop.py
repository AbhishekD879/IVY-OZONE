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
class Test_C28081_TO_BE_EDITEDVerify_Sub_Navigation_Menu_functionality_on_Universal_Header_for_Desktop(Common):
    """
    TR_ID: C28081
    NAME: [TO BE EDITED]Verify Sub Navigation Menu functionality on Universal Header for Desktop
    DESCRIPTION: This test case needs to be edited according to the latest changes.
    DESCRIPTION: This test case verifies Sub Navigation Menu functionality on Universal Header for Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: 1. To open CMS use the next links:
    PRECONDITIONS: DEV: https://invictus.coral.co.uk/keystone/header-menus
    PRECONDITIONS: TST2: https://bm-cms-tst2-coral.symphony-solutions.eu/keystone/header-menus
    PRECONDITIONS: STG2: https://bm-cms-stg2-coral.symphony-solutions.eu/keystone/header-menus
    PRECONDITIONS: |||:LINK TITLE|:TARGET URI
    PRECONDITIONS: || A-Z Menu |  az-sports
    PRECONDITIONS: || In-Play |  in-play
    PRECONDITIONS: || Football |  football
    PRECONDITIONS: || Horse Racing |  horseracing
    PRECONDITIONS: || #YourCall |  yourcall
    PRECONDITIONS: || BuildYourBet |  buildyourbet
    PRECONDITIONS: || Virtuals Sports |  virtual-sports
    PRECONDITIONS: || Tennis |  tennis
    PRECONDITIONS: || Live Stream |  live-stream
    PRECONDITIONS: || News & Blog | http://news.coral.co.uk/
    PRECONDITIONS: || Coral Radio | http://commentariesv4.mediaondemand.net/?c=coral
    PRECONDITIONS: || Statistics |  http://www.stats.betradar.com/s4/?clientid=192
    PRECONDITIONS: For TST2 urls will be like: http://www-tst2.coral.co.uk/casino/top-games
    PRECONDITIONS: For STG:  http://www-stg1.coral.co.uk/casino/top-games
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_check_sub_navigation_menu(self):
        """
        DESCRIPTION: Check 'Sub Navigation' menu
        EXPECTED: 'Sub Navigation' menu consists of tabs, that are CMS configurable:
        EXPECTED: * A-Z Menu
        EXPECTED: * In-Play
        EXPECTED: * Football
        EXPECTED: * Horse Racing
        EXPECTED: * Build Your Bet (for Coral) / Bet Builder (for Ladbrokes)
        EXPECTED: * Virtual Sports
        EXPECTED: * Tennis
        EXPECTED: * Live Stream
        EXPECTED: * News Blog
        EXPECTED: * Coral Radio
        EXPECTED: * Statistics
        """
        pass

    def test_003_verify_that_none_tab_is_not_selected_by_default(self):
        """
        DESCRIPTION: Verify that none tab is not selected by default
        EXPECTED: * Homepage is opened
        EXPECTED: * None tab is not selected by default
        """
        pass

    def test_004_hover_the_mouse_over_the_tabs_in_sub_navigation_menu(self):
        """
        DESCRIPTION: Hover the mouse over the tabs in 'Sub Navigation' menu
        EXPECTED: Text color on tabs is changed
        """
        pass

    def test_005_select_some_tab_in__sub_navigation_menu(self):
        """
        DESCRIPTION: Select some tab in ' Sub Navigation' menu
        EXPECTED: * All tabs are clickable
        EXPECTED: * Selected tab is highlighted by red line
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        """
        pass

    def test_006_verify_sub_navigation_menu_if_there_are_no_set_items(self):
        """
        DESCRIPTION: Verify 'Sub Navigation' menu if there are no set items
        EXPECTED: 'Sub Navigation' menu is not displayed anymore
        """
        pass
