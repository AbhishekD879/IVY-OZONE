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
class Test_C44870184_Verify_user_can_open_All_sports_menu_by_clicking_on_All_sports_quick_carousel_on_Home_Page(Common):
    """
    TR_ID: C44870184
    NAME: Verify user can open 'All sports' menu by clicking on 'All sports' quick carousel on Home Page
    DESCRIPTION: 
    PRECONDITIONS: BETA App should be loaded and user is on Home page
    """
    keep_browser_open = True

    def test_001_tap_on_all_sports_icon_on_quick_carousel(self):
        """
        DESCRIPTION: Tap on 'All Sports' icon on Quick Carousel
        EXPECTED: 'All Sports' page opens with 'Top Sports' followed by 'A-Z Sports' Sections. User should be able to tap on any of the menu items and corresponding page should load.
        """
        pass

    def test_002_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All Sports' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        pass
