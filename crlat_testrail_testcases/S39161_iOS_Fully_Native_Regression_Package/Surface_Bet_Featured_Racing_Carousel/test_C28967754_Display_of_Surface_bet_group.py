import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C28967754_Display_of_Surface_bet_group(Common):
    """
    TR_ID: C28967754
    NAME: Display of Surface bet group
    DESCRIPTION: This test case verifies Surface Bet Carousel when there are more than 1 surface bet to be displayed
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. the surface bet  is available (bet has been configured in CMS for this page)
    PRECONDITIONS: 3. there are more than 1 surface bet to be displayed
    """
    keep_browser_open = True

    def test_001_navigate_to_homepage_on_featured_tab(self):
        """
        DESCRIPTION: navigate to homepage on featured tab
        EXPECTED: homepage is displayed with featured tab
        EXPECTED: The surface bet carousel with more than 1 surface bet is displayed  as per design
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3077390)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/3077391)
        """
        pass

    def test_002_swipe_the_surface_bet_carousel(self):
        """
        DESCRIPTION: swipe the surface bet carousel
        EXPECTED: the carousel is swiped
        EXPECTED: 2nd surface bet is displayed in the middle (part of 1st and 3rd surface bets are displayed on the edge of the screen)
        """
        pass
