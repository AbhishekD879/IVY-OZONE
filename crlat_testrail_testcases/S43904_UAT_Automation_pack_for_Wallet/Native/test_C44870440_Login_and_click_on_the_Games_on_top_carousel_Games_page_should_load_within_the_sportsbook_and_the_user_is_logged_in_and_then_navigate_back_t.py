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
class Test_C44870440_Login_and_click_on_the_Games_on_top_carousel_Games_page_should_load_within_the_sportsbook_and_the_user_is_logged_in_and_then_navigate_back_to_sports_From_Coral__Verify_navigation_from_Sport_to_the_Gaming(Common):
    """
    TR_ID: C44870440
    NAME: Login and click on the Games on top carousel > Games page should load within the sportsbook and the user is logged in and then navigate back to sports. From Coral -  Verify navigation from Sport to the Gaming
    DESCRIPTION: Login and click on the Games on top carousel > Games page should load within the sportsbook and the user is logged in and then navigate back to sports. From Coral -  Verify navigation from Sport to the Gaming
    PRECONDITIONS: 
    """
    keep_browser_open = True
