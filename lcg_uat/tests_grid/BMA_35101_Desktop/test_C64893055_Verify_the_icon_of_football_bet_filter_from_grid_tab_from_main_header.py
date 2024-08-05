import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893055_Verify_the_icon_of_football_bet_filter_from_grid_tab_from_main_header(Common):
    """
    TR_ID: C64893055
    NAME: Verify the icon of football bet filter from grid tab from main header.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_click_on_the_grid_tab_from_main_header3user_should_be_able_to_see_an_icon_for_the_football_bet_filter_itemexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_see_an_icon_for_football_bet_filter(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Click on the grid tab from main header.
        DESCRIPTION: 3.User should be able to see an icon for the football bet filter item.
        EXPECTED: 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to see an icon for football bet filter.
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        football_bet_filter = self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.FB_BET_FILTER_NAME)
        self.assertTrue(football_bet_filter.item_icon.is_displayed(), msg=f'Icon is not displayed for football bet filter')
