import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.connect
@vtest
class Test_C64893891_Verify_if_the_user_is_able_to_navigate_to_the_Grid_HUB_home_page_from_sports_book_page_without_login(Common):
    """
    TR_ID: C64893891
    NAME: Verify if the user is able to navigate to the  Grid HUB home page from sports book page without login.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Coral sports URL.
    PRECONDITIONS: 2.User Is not logged in with any user.
    """
    keep_browser_open = True

    def test_001_launch_coral_sports_url2_click_on_grid_tab_from_a_z_menu__carouselexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_grid_home_pageexpected_result1_1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_grid_home_page(self):
        """
        DESCRIPTION: 1. 1. 1. Launch Coral sports URL.
        DESCRIPTION: 2. Click on grid tab from A-Z menu / carousel.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the grid home page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the grid home page.
        EXPECTED: 1. 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the grid home page.
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
