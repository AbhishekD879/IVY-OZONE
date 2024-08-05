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
class Test_C44870185_Click_on_All_sports_menu_and_verify_Top_Sports_carousel_navigations(Common):
    """
    TR_ID: C44870185
    NAME: Click on 'All sports' menu and verify 'Top Sports' carousel navigations
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_tap_on_all_sports_icon_on_quick_carousel(self):
        """
        DESCRIPTION: Tap on 'All Sports' icon on Quick Carousel
        EXPECTED: 'All Sports' page opens with 'Top Sports' followed by 'A-Z Sports' Sections.
        """
        pass

    def test_002_verify_top_sports_carousel(self):
        """
        DESCRIPTION: Verify Top Sports carousel
        EXPECTED: Top sports (eg : Football, Tennis, Horses) are listed in this section along with 'In-Play'. User should be able to tap on any of the menu items and corresponding sports page should load.
        """
        pass

    def test_003_tap_on_in_play(self):
        """
        DESCRIPTION: Tap on In-Play
        EXPECTED: User should land on In-Play page
        """
        pass

    def test_004_tap_on_any_other_sport__race_from_the_list(self):
        """
        DESCRIPTION: Tap on any other sport / Race from the list
        EXPECTED: User should land on respective sport/race landing page
        """
        pass

    def test_005_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All Sports' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        pass
