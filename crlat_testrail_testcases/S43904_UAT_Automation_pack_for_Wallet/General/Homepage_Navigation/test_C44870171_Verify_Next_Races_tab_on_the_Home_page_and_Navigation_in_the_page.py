import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C44870171_Verify_Next_Races_tab_on_the_Home_page_and_Navigation_in_the_page(Common):
    """
    TR_ID: C44870171
    NAME: Verify Next Races tab on the Home page and Navigation in the page.
    DESCRIPTION: Verify next races tab page on the home page and navigation in the page. Verify New Navigation arrows Next Races Carousel.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: App is loaded and user is landed on home page
        """
        pass

    def test_002_select_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Select NEXT RACES tab on home page
        EXPECTED: Next Races page is loaded and next races are listed in start time order.
        """
        pass

    def test_003_click_on_more__of_any_meeting_from_the_list(self):
        """
        DESCRIPTION: Click on 'MORE >' of any meeting from the list
        EXPECTED: User should navigate to the corresponding meeting page.
        """
        pass
